import abc
from abc import ABC
from datetime import datetime
import sys
from typing import ClassVar, List, Optional, Union

from pydantic import (
    BaseModel,
    Field,
    root_validator,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
)

from datagateway_api.src.search_api.panosc_mappings import mappings


# TODO - Merge this with `get_icat_mapping` from src\search_api\filters.py
def _get_icat_mapping(panosc_entity_name, field_name):
    icat_mapping = mappings.mappings[panosc_entity_name][field_name]

    if isinstance(icat_mapping, str):
        # Field name
        icat_field_name = icat_mapping
    if isinstance(icat_mapping, dict):
        # Relation - JSON format: {PaNOSC entity name: ICAT related field name}
        panosc_entity_name = list(icat_mapping.keys())[0]
        icat_field_name = icat_mapping[panosc_entity_name]

    return panosc_entity_name, icat_field_name


def _get_icat_field_value(icat_field_name, icat_data):
    icat_field_name = icat_field_name.split(".")
    value = icat_data
    for f in icat_field_name:
        value = value[f]

    return value


class PaNOSCAttribute(ABC, BaseModel):
    @classmethod
    @abc.abstractmethod
    def from_icat(cls, icat_data):  # noqa: B902, N805
        model_fields = cls.__fields__

        model_data = {}
        for field in model_fields:
            # Some fields have aliases so we must use them when creating a model instance.
            # If a field does not have an alias then the `alias` property holds the name
            # of the field
            field_alias = cls.__fields__[field].alias

            panosc_entity_name, icat_field_name = _get_icat_mapping(
                cls.__name__, field_alias,
            )
            try:
                field_value = _get_icat_field_value(icat_field_name, icat_data)
            except KeyError:
                continue

            if panosc_entity_name != cls.__name__:
                # If we are here, it means that the field references another model so we
                # have to get hold of its class definition and call its `from_icat` method
                # to create an instance of itself with the ICAT data provided. Doing this
                # allows for recursion.
                data = icat_data[icat_field_name]
                if not isinstance(data, list):
                    data = [data]

                # Get the class of the referenced model
                panosc_model_attr = getattr(sys.modules[__name__], panosc_entity_name)
                field_value = [panosc_model_attr.from_icat(d) for d in data]

                field_type = cls.__fields__[field].outer_type_._name
                if field_type != "List":
                    field_value = field_value[0]

            model_data[field_alias] = field_value

        return cls(**model_data)


class Affiliation(PaNOSCAttribute):
    """Information about which facility a member is located at"""

    _text_operator_fields: ClassVar[List[str]] = []

    name: Optional[StrictStr]
    id_: Optional[StrictStr] = Field(alias="id")
    address: Optional[StrictStr]
    city: Optional[StrictStr]
    country: Optional[StrictStr]

    members: Optional[List["Member"]]

    @classmethod
    def from_icat(cls, icat_query_data):
        return super(Affiliation, cls).from_icat(icat_query_data)


class Dataset(PaNOSCAttribute):
    """
    Information about an experimental run, including optional File, Sample, Instrument
    and Technique
    """

    _text_operator_fields: ClassVar[List[str]] = ["title"]

    pid: StrictStr
    title: StrictStr
    is_public: StrictBool = Field(alias="isPublic")
    creation_date: datetime = Field(alias="creationDate")
    size: Optional[StrictInt]

    documents: List["Document"]
    techniques: List["Technique"]
    instrument: Optional["Instrument"]
    files: Optional[List["File"]]
    parameters: Optional[List["Parameter"]]
    samples: Optional[List["Sample"]]

    @classmethod
    def from_icat(cls, icat_query_data):
        return super(Dataset, cls).from_icat(icat_query_data)


class Document(PaNOSCAttribute):
    """
    Proposal which includes the dataset or published paper which references the dataset
    """

    _text_operator_fields: ClassVar[List[str]] = ["title", "summary"]

    pid: StrictStr
    is_public: StrictBool = Field(alias="isPublic")
    type_: StrictStr = Field(alias="type")
    title: StrictStr
    summary: Optional[StrictStr]
    doi: Optional[StrictStr]
    start_date: Optional[datetime] = Field(alias="startDate")
    end_date: Optional[datetime] = Field(alias="endDate")
    release_date: Optional[datetime] = Field(alias="releaseDate")
    license_: Optional[StrictStr] = Field(alias="license")
    keywords: Optional[List[StrictStr]]

    datasets: List[Dataset]
    members: Optional[List["Member"]]
    parameters: Optional[List["Parameter"]]

    @classmethod
    def from_icat(cls, icat_query_data):
        return super(Document, cls).from_icat(icat_query_data)


class File(PaNOSCAttribute):
    """Name of file and optionally location"""

    _text_operator_fields: ClassVar[List[str]] = ["name"]

    id_: StrictStr = Field(alias="id")
    name: StrictStr
    path: Optional[StrictStr]
    size: Optional[StrictInt]

    dataset: Dataset

    @classmethod
    def from_icat(cls, icat_query_data):
        return super(File, cls).from_icat(icat_query_data)


class Instrument(PaNOSCAttribute):
    """Beam line where experiment took place"""

    _text_operator_fields: ClassVar[List[str]] = ["name", "facility"]

    pid: StrictStr
    name: StrictStr
    facility: StrictStr

    datasets: Optional[List[Dataset]]

    @classmethod
    def from_icat(cls, icat_query_data):
        return super(Instrument, cls).from_icat(icat_query_data)


class Member(PaNOSCAttribute):
    """Proposal team member or paper co-author"""

    _text_operator_fields: ClassVar[List[str]] = []

    id_: StrictStr = Field(alias="id")
    role: Optional[StrictStr] = Field(alias="role")

    document: Document
    person: Optional["Person"]
    affiliation: Optional[Affiliation]

    @classmethod
    def from_icat(cls, icat_query_data):
        return super(Member, cls).from_icat(icat_query_data)


class Parameter(PaNOSCAttribute):
    """
    Scalar measurement with value and units.
    Note: a parameter is either related to a dataset or a document, but not both.
    """

    _text_operator_fields: ClassVar[List[str]] = []

    id_: StrictStr = Field(alias="id")
    name: StrictStr
    value: Union[StrictFloat, StrictInt, StrictStr]
    unit: Optional[StrictStr]

    dataset: Optional[Dataset]
    document: Optional[Document]

    @root_validator(skip_on_failure=True)
    def validate_dataset_and_document(cls, values):  # noqa: B902, N805
        if values["dataset"] is None and values["document"] is None:
            raise TypeError("must have a dataset or document")

        if values["dataset"] is not None and values["document"] is not None:
            # TODO - Should an exception be raised here instead?
            values["Document"] = None

        return values

    @classmethod
    def from_icat(cls, icat_query_data):
        return super(Parameter, cls).from_icat(icat_query_data)


class Person(PaNOSCAttribute):
    """Human who carried out experiment"""

    _text_operator_fields: ClassVar[List[str]] = []

    id_: StrictStr = Field(alias="id")
    full_name: StrictStr = Field(alias="fullName")
    orcid: Optional[StrictStr]
    researcher_id: Optional[StrictStr] = Field(alias="researcherId")
    first_name: Optional[StrictStr] = Field(alias="firstName")
    last_name: Optional[StrictStr] = Field(alias="lastName")

    members: Optional[List[Member]]

    @classmethod
    def from_icat(cls, icat_query_data):
        return super(Person, cls).from_icat(icat_query_data)


class Sample(PaNOSCAttribute):
    """Extract of material used in the experiment"""

    _text_operator_fields: ClassVar[List[str]] = ["name", "description"]

    name: StrictStr
    pid: StrictStr
    description: Optional[StrictStr]

    datasets: Optional[List[Dataset]]

    @classmethod
    def from_icat(cls, icat_query_data):
        return super(Sample, cls).from_icat(icat_query_data)


class Technique(PaNOSCAttribute):
    """Common name of scientific method used"""

    _text_operator_fields: ClassVar[List[str]] = ["name"]

    pid: StrictStr
    name: StrictStr

    datasets: Optional[List[Dataset]]

    @classmethod
    def from_icat(cls, icat_query_data):
        return super(Technique, cls).from_icat(icat_query_data)


# The below models reference other models that may not be defined during their
# creation so their references have to manually be updated to lead to the actual
# models or else an exception will be raised. This can be done with the help of
# the postponed annotations via the future import together with the
# `update_forward_refs` method, only after all related models are declared.
Affiliation.update_forward_refs()
Dataset.update_forward_refs()
Document.update_forward_refs()
Member.update_forward_refs()
