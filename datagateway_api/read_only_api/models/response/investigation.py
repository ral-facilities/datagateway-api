from datetime import datetime
from enum import StrEnum

from pydantic import Field

from datagateway_api.read_only_api.models.response.common import (
    BaseDataCollection,
    BaseDataPublication,
    EntityModel,
    User,
)
from datagateway_api.read_only_api.models.response.facility_cycle import FacilityCycle
from datagateway_api.read_only_api.models.response.instrument import Instrument


class InvestigationInstrument(EntityModel):
    instrument: Instrument | None = None


class InvestigationUser(EntityModel):
    role: str | None = None

    user: User | None = None


class SampleType(EntityModel):
    name: str | None = None
    molecularFormula: str | None = None
    safetyInformation: str | None = None


class Sample(EntityModel):
    name: str | None = None
    pid: str | None = None

    type_: SampleType | None = Field(default=None, alias="type")


class ParameterValueType(StrEnum):
    STRING = "STRING"
    DATE_AND_TIME = "DATE_AND_TIME"
    NUMERIC = "NUMERIC"


class ParameterType(EntityModel):
    name: str | None = None
    valueType: ParameterValueType | None = None
    units: str | None = None
    unitsFullName: str | None = None
    pid: str | None = None
    description: str | None = None
    minimumNumericValue: float | None = None
    maximumNumericValue: float | None = None
    enforced: bool | None = None
    verified: bool | None = None
    applicableToInvestigation: bool | None = None
    applicableToDataset: bool | None = None
    applicableToDatafile: bool | None = None
    applicableToSample: bool | None = None
    applicableToDataCollection: bool | None = None


class Parameter(EntityModel):
    stringValue: str | None = None
    dateTimeValue: datetime | None = None
    numericValue: float | None = None
    error: float | None = None
    rangeBottom: float | None = None
    rangeTop: float | None = None

    type_: ParameterType | None = Field(default=None, alias="type")


class Publication(EntityModel):
    fullReference: str | None = None
    doi: str | None = None
    url: str | None = None
    repository: str | None = None
    repositoryId: str | None = None


class InvestigationFacilityCycle(EntityModel):
    facilityCycle: FacilityCycle | None = None


class DataCollection(BaseDataCollection):
    dataPublications: list[BaseDataPublication] | None = None


class DataCollectionInvestigation(EntityModel):
    dataCollection: DataCollection | None = None


class BaseInvestigation(EntityModel):
    name: str | None = None
    visitId: str | None = None
    title: str | None = None
    summary: str | None = None
    doi: str | None = None
    startDate: datetime | None = None
    endDate: datetime | None = None
    releaseDate: datetime | None = None
    fileCount: int | None = None
    fileSize: int | None = None

    investigationInstruments: list[InvestigationInstrument] | None = None
    investigationUsers: list[InvestigationUser] | None = None


class Investigation(BaseInvestigation):
    samples: list[Sample] | None = None
    parameters: list[Parameter] | None = None
    publications: list[Publication] | None = None
    investigationFacilityCycles: list[InvestigationFacilityCycle] | None = None
    dataCollectionInvestigations: list[DataCollectionInvestigation] | None = None
