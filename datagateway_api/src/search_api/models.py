from abc import ABC, abstractmethod
from datetime import datetime, timezone
import sys
from typing import ClassVar, List, Optional, Union

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field, ValidationError, validator
from pydantic.error_wrappers import ErrorWrapper

from datagateway_api.src.common.config import Config
from datagateway_api.src.common.date_handler import DateHandler
from datagateway_api.src.search_api.panosc_mappings import mappings


def _is_panosc_entity_field_of_type_list(entity_field):
    entity_field_outer_type = entity_field.outer_type_
    if (
        hasattr(entity_field_outer_type, "_name")
        and entity_field_outer_type._name == "List"
    ):
        is_list = True
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
    @classmethod
    @abstractmethod
    def from_icat(cls, icat_data, required_related_fields):  # noqa: B902, N805
        entity_fields = cls.__fields__

        entity_data = {}
        for entity_field in entity_fields:
            # Some fields have aliases so we must use them when creating a model
            # instance. If a field does not have an alias then the `alias` property
            # holds the name of the field
            entity_field_alias = cls.__fields__[entity_field].alias

            entity_name, icat_field_name = mappings.get_icat_mapping(
                cls.__name__, entity_field_alias,
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
                data = (
                    [field_value] if not isinstance(field_value, list) else field_value
                )

                required_related_fields_for_next_entity = []
                for required_related_field in required_related_fields:
                    required_related_field = required_related_field.split(".")
                    if (
                        len(required_related_field) > 1
                        and entity_field_alias in required_related_field
                    ):
                        required_related_fields_for_next_entity.extend(
                            required_related_field[1:],
                        )

                # Get the class of the referenced entity
                entity_attr = getattr(sys.modules[__name__], entity_name)
                field_value = [
                    entity_attr.from_icat(d, required_related_fields_for_next_entity)
                    for d in data
                ]

            if not _is_panosc_entity_field_of_type_list(
                cls.__fields__[entity_field],
            ) and isinstance(field_value, list):
                # If the field does not hold list of values but `field_value`
                # is a list, then just get its first element
                field_value = field_value[0]

            entity_data[entity_field_alias] = field_value

        for required_related_field in required_related_fields:
            required_related_field = required_related_field.split(".")[0]

            if (
                required_related_field in entity_fields
                and required_related_field
                in cls._related_fields_with_min_cardinality_one
                and required_related_field not in entity_data
            ):
                # If we are here, it means that a related entity, which has a minimum
                # cardinality of one, has been specified to be included as part of the
                # entity but the relevant ICAT data needed for its creation cannot be
                # found in the provided ICAT response. Because of this, a
                # `ValidationError` is raised.
                error_wrapper = ErrorWrapper(
                    TypeError("field required"), loc=required_related_field,
                )
                raise ValidationError(errors=[error_wrapper], model=cls)

        return cls(**entity_data)


class Affiliation(PaNOSCAttribute):
    """Information about which facility a member is located at"""

    _related_fields_with_min_cardinality_one: ClassVar[List[str]] = ["members"]
    _text_operator_fields: ClassVar[List[str]] = []

    name: Optional[str] = None
    id_: Optional[str] = Field(None, alias="id")
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

    pid: str
    title: str
    is_public: bool = Field(alias="isPublic")
    creation_date: datetime = Field(alias="creationDate")
    size: Optional[int] = None

    documents: List["Document"] = []
    techniques: List["Technique"] = []
    instrument: Optional["Instrument"] = None
    files: Optional[List["File"]] = []
    parameters: Optional[List["Parameter"]] = []
    samples: Optional[List["Sample"]] = []

    @validator("pid", pre=True, always=True)
    def set_pid(cls, value):  # noqa: B902, N805
        return f"pid:{value}" if isinstance(value, int) else value

    @validator("is_public", pre=True, always=True)
    def set_is_public(cls, value):  # noqa: B902, N805
        if not value:
            return value

        creation_date = DateHandler.str_to_datetime_object(value)
        current_datetime = datetime.now(timezone.utc)
        rd = relativedelta(
            years=Config.config.search_api.num_of_years_determining_public_data,
        )
        return creation_date < (current_datetime - rd)

    @classmethod
    def from_icat(cls, icat_data, required_related_fields):
        return super(Dataset, cls).from_icat(icat_data, required_related_fields)


class Document(PaNOSCAttribute):
    """
    Proposal which includes the dataset or published paper which references the dataset
    """

    _related_fields_with_min_cardinality_one: ClassVar[List[str]] = ["datasets"]
    _text_operator_fields: ClassVar[List[str]] = ["title", "summary"]

    pid: str
    is_public: bool = Field(alias="isPublic")
    type_: str = Field(alias="type")
    title: str
    summary: Optional[str] = None
    doi: Optional[str] = None
    start_date: Optional[datetime] = Field(None, alias="startDate")
    end_date: Optional[datetime] = Field(None, alias="endDate")
    release_date: Optional[datetime] = Field(None, alias="releaseDate")
    license_: Optional[str] = Field(None, alias="license")
    keywords: Optional[List[str]] = []

    datasets: List[Dataset] = []
    members: Optional[List["Member"]] = []
    parameters: Optional[List["Parameter"]] = []

    @validator("is_public", pre=True, always=True)
    def set_is_public(cls, value):  # noqa: B902, N805
        if not value:
            return value

        creation_date = DateHandler.str_to_datetime_object(value)
        current_datetime = datetime.now(timezone.utc)
        rd = relativedelta(
            years=Config.config.search_api.num_of_years_determining_public_data,
        )
        return creation_date < (current_datetime - rd)

    @classmethod
    def from_icat(cls, icat_data, required_related_fields):
        return super(Document, cls).from_icat(icat_data, required_related_fields)


class File(PaNOSCAttribute):
    """Name of file and optionally location"""

    _related_fields_with_min_cardinality_one: ClassVar[List[str]] = ["dataset"]
    _text_operator_fields: ClassVar[List[str]] = ["name"]

    id_: str = Field(alias="id")
    name: str
    path: Optional[str] = None
    size: Optional[int] = None

    dataset: Dataset = None

    @classmethod
    def from_icat(cls, icat_data, required_related_fields):
        return super(File, cls).from_icat(icat_data, required_related_fields)


class Instrument(PaNOSCAttribute):
    """Beam line where experiment took place"""

    _related_fields_with_min_cardinality_one: ClassVar[List[str]] = []
    _text_operator_fields: ClassVar[List[str]] = ["name", "facility"]

    pid: str
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

    id_: str = Field(alias="id")
    role: Optional[str] = Field(None, alias="role")

    document: Document = None
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

    id_: str = Field(alias="id")
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

    id_: str = Field(alias="id")
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
    pid: str
    description: Optional[str] = None

    datasets: Optional[List[Dataset]] = []

    @validator("pid", pre=True, always=True)
    def set_pid(cls, value):  # noqa: B902, N805
        return f"pid:{value}" if isinstance(value, int) else value

    @classmethod
    def from_icat(cls, icat_data, required_related_fields):
        return super(Sample, cls).from_icat(icat_data, required_related_fields)


class Technique(PaNOSCAttribute):
    """Common name of scientific method used"""

    _related_fields_with_min_cardinality_one: ClassVar[List[str]] = []
    _text_operator_fields: ClassVar[List[str]] = ["name"]

    pid: str
    name: str

    datasets: Optional[List[Dataset]] = []

    @classmethod
    def from_icat(cls, icat_data, required_related_fields):
        return super(Technique, cls).from_icat(icat_data, required_related_fields)


# The below models reference other models that may not be defined during their
# creation so their references have to manually be updated to lead to the actual
# models or else an exception will be raised. This can be done with the help of
# the postponed annotations via the future import together with the
# `update_forward_refs` method, only after all related models are declared.
Affiliation.update_forward_refs()
Dataset.update_forward_refs()
Document.update_forward_refs()
Member.update_forward_refs()
