from abc import ABC, abstractmethod
from datetime import datetime
import sys
from typing import Annotated, ClassVar, List, Literal, Optional, Union

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PlainSerializer,
    ValidationError,
)
from pydantic_core import ErrorDetails

from datagateway_api.src.search_api.panosc_mappings import mappings


def format_datetime(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


SearchAPIDatetime = Annotated[
    datetime,
    PlainSerializer(format_datetime, return_type=str, when_used="always"),
]


def pid_prefix(value):
    return f"pid:{value}" if isinstance(value, int) else value


SearchAPIPid = Annotated[str, BeforeValidator(pid_prefix)]

# The PaNOSC fields that map to id fields in ICAT were set to be of type StrictStr but
# because they are integers in ICAT, the creation of the PaNOSC models was failing
# because they were only accepting strings. To deal with this issue, the type of such
# PaNOSC fields were changed to str instead as this casts integers to strings but still
# throws a ValidationError if None is passed to it. To keep things consistent and less
# confusing, the types of all the other fields were made non-strict.


SearchAPIId = Annotated[
    str,
    Field(alias="id"),
]


def _is_panosc_entity_field_of_type_list(entity_field):
    entity_field_annotation = entity_field.annotation
    if hasattr(entity_field_annotation, "_name") and entity_field_annotation._name == "List":
        is_list = True  # pragma: py-37-code
    # The `_name` `outer_type_` attribute was introduced in Python 3.7 so to check
    # whether the field is of type list in Python 3.6, we are checking the type of its
    # default value. We must ensure that any new list fields that get added in future
    # are assigned a list by default.
    elif isinstance(entity_field.default, list):
        is_list = True
    else:
        is_list = False

    return is_list


def _get_icat_field_value(icat_field_name, icat_data):
    icat_field_name = icat_field_name.split(".")
    for field_name in icat_field_name:
        if isinstance(icat_data, list):
            values = []
            for data in icat_data:
                value = _get_icat_field_value(field_name, data)
                value = [value] if not isinstance(value, list) else value
                values.extend(value)
            icat_data = values
        elif isinstance(icat_data, dict):
            icat_data = icat_data[field_name]

    return icat_data


class PaNOSCAttribute(ABC, BaseModel):
    _datetime_field_names: ClassVar[List[str]] = [
        "creationDate",
        "startDate",
        "endDate",
        "releaseDate",
    ]

    model_config = ConfigDict(coerce_numbers_to_str=True)

    @classmethod
    @abstractmethod
    def from_icat(cls, icat_data, required_related_fields):  # noqa: B902, N805
        entity_fields = cls.model_fields

        entity_data = {}
        for entity_field in entity_fields:
            # Some fields have aliases so we must use them when creating a model
            # instance. If a field does not have an alias then the `alias` property
            # holds the name of the field
            field_info = cls.model_fields[entity_field]
            entity_field_alias = field_info.alias or entity_field

            entity_name, icat_field_name = mappings.get_icat_mapping(
                cls.__name__,
                entity_field_alias,
            )

            if not isinstance(icat_field_name, list):
                icat_field_name = [icat_field_name]

            field_value = None
            for field_name in icat_field_name:
                try:
                    field_value = _get_icat_field_value(field_name, icat_data)
                    if field_value:
                        break
                except KeyError:
                    # If an icat value cannot be found for the ICAT field name in the
                    # provided ICAT data then ignore the error. The field name could
                    # simply be a mapping of an optional PaNOSC entity field so ICAT
                    # may not return data for it which is fine. It could also be a list
                    # of mappings which is the case with the `value` field of the
                    # PaNOSC entity. When this is the case, ICAT only returns data for
                    # one of the mappings from the list so we can ignore the error.
                    # This also ignores errors for mandatory fields but this is not a
                    # problem because pydantic is responsible for validating whether
                    # data for mandatory fields is missing.
                    continue

            if not field_value:
                continue

            if entity_name != cls.__name__:
                # If we are here, it means that the field references another model so
                # we have to get hold of its class definition and call its `from_icat`
                # method to create an instance of itself with the ICAT data provided.
                # Doing this allows for recursion.

                if entity_field_alias not in [
                    required_related_field.split(".")[0] for required_related_field in required_related_fields
                ]:
                    # Before proceeding, check if the related entity really needs to be created.
                    # Do not attempt to create the related entity if ICAT data for it is available
                    # but the entity has not been specified to be included. In such cases, the ICAT
                    # data is likely available because the data for another entity field is
                    # retrieved via that ICAT entity. We do not want to return data for related
                    # entities unless explicitly specified to be included by the user.
                    continue

                data = [field_value] if not isinstance(field_value, list) else field_value

                required_related_fields_for_next_entity = []
                for required_related_field in required_related_fields:
                    required_related_field = required_related_field.split(".")
                    if len(required_related_field) > 1 and entity_field_alias in required_related_field:
                        required_related_fields_for_next_entity.extend(
                            required_related_field[1:],
                        )

                # Get the class of the referenced entity
                entity_attr = getattr(sys.modules[__name__], entity_name)
                field_value = [entity_attr.from_icat(d, required_related_fields_for_next_entity) for d in data]

            if not _is_panosc_entity_field_of_type_list(
                cls.model_fields[entity_field],
            ) and isinstance(field_value, list):
                # If the field does not hold list of values but `field_value`
                # is a list, then just get its first element
                field_value = field_value[0]

            entity_data[entity_field_alias] = field_value

        for required_related_field in required_related_fields:
            required_related_field = required_related_field.split(".")[0]

            if (
                required_related_field in entity_fields
                and required_related_field in cls._related_fields_with_min_cardinality_one
                and required_related_field not in entity_data
            ):
                # If we are here, it means that a related entity, which has a minimum
                # cardinality of one, has been specified to be included as part of the
                # entity but the relevant ICAT data needed for its creation cannot be
                # found in the provided ICAT response. Because of this, a
                # `ValidationError` is raised.

                raise ValidationError.from_exception_data(
                    cls.__name__,
                    [
                        ErrorDetails(
                            type="missing",
                            loc=(required_related_field,),
                            msg="Field required",
                            input=None,
                        ),
                    ],
                )

        return cls(**entity_data)


class Affiliation(PaNOSCAttribute):
    """Information about which facility a member is located at"""

    _related_fields_with_min_cardinality_one: ClassVar[List[str]] = ["members"]
    _text_operator_fields: ClassVar[List[str]] = []

    name: Optional[str] = None
    id_: Annotated[Optional[str], Field(alias="id")]
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

    members: Optional[List["Member"]] = []

    @classmethod
    def from_icat(cls, icat_data, required_related_fields):
        return super(Affiliation, cls).from_icat(icat_data, required_related_fields)


class Dataset(PaNOSCAttribute):
    """
    Information about an experimental run, including optional File, Sample, Instrument
    and Technique
    """

    _related_fields_with_min_cardinality_one: ClassVar[List[str]] = [
        "documents",
        "techniques",
    ]
    _text_operator_fields: ClassVar[List[str]] = ["title"]

    pid: SearchAPIPid
    title: str
    # Hardcoding this to True because anon user is used for querying so all data
    # returned by it is public
    is_public: Literal[True] = Field(True, alias="isPublic")
    creation_date: SearchAPIDatetime = Field(alias="creationDate")
    size: Optional[int] = None

    documents: List["Document"] = []
    techniques: List["Technique"] = []
    instrument: Optional["Instrument"] = None
    files: Optional[List["File"]] = []
    parameters: Optional[List["Parameter"]] = []
    samples: Optional[List["Sample"]] = []

    @classmethod
    def from_icat(cls, icat_data, required_related_fields):
        return super(Dataset, cls).from_icat(icat_data, required_related_fields)


class Document(PaNOSCAttribute):
    """
    Proposal which includes the dataset or published paper which references the dataset
    """

    _related_fields_with_min_cardinality_one: ClassVar[List[str]] = ["datasets"]
    _text_operator_fields: ClassVar[List[str]] = ["title", "summary"]

    pid: SearchAPIPid
    # Hardcoding this to True because anon user is used for querying so all data
    # returned by it is public
    is_public: Literal[True] = Field(True, alias="isPublic")
    type_: str = Field(alias="type")
    title: str
    summary: Optional[str] = None
    doi: Optional[str] = None
    start_date: Optional[SearchAPIDatetime] = Field(None, alias="startDate")
    end_date: Optional[SearchAPIDatetime] = Field(None, alias="endDate")
    release_date: Optional[SearchAPIDatetime] = Field(None, alias="releaseDate")
    license_: Optional[str] = Field(None, alias="license")
    keywords: Optional[List[str]] = []

    datasets: List[Dataset] = []
    members: Optional[List["Member"]] = []
    parameters: Optional[List["Parameter"]] = []

    @classmethod
    def from_icat(cls, icat_data, required_related_fields):
        return super(Document, cls).from_icat(icat_data, required_related_fields)


class File(PaNOSCAttribute):
    """Name of file and optionally location"""

    _related_fields_with_min_cardinality_one: ClassVar[List[str]] = ["dataset"]
    _text_operator_fields: ClassVar[List[str]] = ["name"]

    id_: SearchAPIId
    name: str
    path: Optional[str] = None
    size: Optional[int] = None

    dataset: Optional[Dataset] = None

    @classmethod
    def from_icat(cls, icat_data, required_related_fields):
        return super(File, cls).from_icat(icat_data, required_related_fields)


class Instrument(PaNOSCAttribute):
    """Beam line where experiment took place"""

    _related_fields_with_min_cardinality_one: ClassVar[List[str]] = []
    _text_operator_fields: ClassVar[List[str]] = ["name", "facility"]

    pid: SearchAPIPid
    name: str
    facility: str

    datasets: Optional[List[Dataset]] = []

    @classmethod
    def from_icat(cls, icat_data, required_related_fields):
        return super(Instrument, cls).from_icat(icat_data, required_related_fields)


class Member(PaNOSCAttribute):
    """Proposal team member or paper co-author"""

    _related_fields_with_min_cardinality_one: ClassVar[List[str]] = ["document"]
    _text_operator_fields: ClassVar[List[str]] = []

    id_: SearchAPIId
    role: Optional[str] = Field(None, alias="role")

    document: Optional[Document] = None
    person: Optional["Person"] = None
    affiliation: Optional[Affiliation] = None

    @classmethod
    def from_icat(cls, icat_data, required_related_fields):
        return super(Member, cls).from_icat(icat_data, required_related_fields)


class Parameter(PaNOSCAttribute):
    """
    Scalar measurement with value and units.
    Note: a parameter is either related to a dataset or a document, but not both.
    """

    _related_fields_with_min_cardinality_one: ClassVar[List[str]] = []
    _text_operator_fields: ClassVar[List[str]] = []

    id_: SearchAPIId
    name: str
    value: Union[float, int, str]
    unit: Optional[str] = None

    dataset: Optional[Dataset] = None
    document: Optional[Document] = None

    """
    Validator commented as it was decided to be disabled for the time being. The Data
    Model states that a Parameter must be related to a Dataset or Document, however
    considering that there is not a Parameter endpoint, it means that a Parameter can
    only be included via Dataset or Document. It's unclear why anyone would query for
    a Dataset or Document that includes Parameters which in turn includes a Dataset or
    Document that are the same as the top level ones. To avoid errors being raised
    as a result of Parameters not containing ICAT data for a Dataset or Document, the
    validator has been disabled.

    @root_validator(skip_on_failure=True)
    def validate_dataset_and_document(cls, values):  # noqa: B902, N805
        if values["dataset"] is None and values["document"] is None:
            raise TypeError("must have a dataset or document")

        if values["dataset"] is not None and values["document"] is not None:
            # TODO - Should an exception be raised here instead?
            values["Document"] = None

        return values
    """

    @classmethod
    def from_icat(cls, icat_data, required_related_fields):
        return super(Parameter, cls).from_icat(icat_data, required_related_fields)


class Person(PaNOSCAttribute):
    """Human who carried out experiment"""

    _related_fields_with_min_cardinality_one: ClassVar[List[str]] = []
    _text_operator_fields: ClassVar[List[str]] = []

    id_: SearchAPIId
    full_name: str = Field(alias="fullName")
    orcid: Optional[str] = None
    researcher_id: Optional[str] = Field(None, alias="researcherId")
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")

    members: Optional[List[Member]] = []

    @classmethod
    def from_icat(cls, icat_data, required_related_fields):
        return super(Person, cls).from_icat(icat_data, required_related_fields)


class Sample(PaNOSCAttribute):
    """Extract of material used in the experiment"""

    _related_fields_with_min_cardinality_one: ClassVar[List[str]] = []
    _text_operator_fields: ClassVar[List[str]] = ["name", "description"]

    name: str
    pid: SearchAPIPid
    description: Optional[str] = None

    datasets: Optional[List[Dataset]] = []

    @classmethod
    def from_icat(cls, icat_data, required_related_fields):
        return super(Sample, cls).from_icat(icat_data, required_related_fields)


class Technique(PaNOSCAttribute):
    """Common name of scientific method used"""

    _related_fields_with_min_cardinality_one: ClassVar[List[str]] = []
    _text_operator_fields: ClassVar[List[str]] = ["name"]

    pid: SearchAPIPid
    name: str

    datasets: Optional[List[Dataset]] = []

    @classmethod
    def from_icat(cls, icat_data, required_related_fields):
        return super(Technique, cls).from_icat(icat_data, required_related_fields)


class CountResponse(BaseModel):
    count: int


# The below models reference other models that may not be defined during their
# creation so their references have to manually be updated to lead to the actual
# models or else an exception will be raised. This can be done with the help of
# the postponed annotations via the future import together with the
# `model_rebuild` method, only after all related models are declared.
Affiliation.model_rebuild()
Dataset.model_rebuild()
Document.model_rebuild()
Member.model_rebuild()
