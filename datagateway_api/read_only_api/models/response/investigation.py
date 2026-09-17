from datetime import datetime
from enum import StrEnum

from pydantic import Field

from datagateway_api.read_only_api.models.response.common import EntityModel


class Instrument(EntityModel):
    name: str | None = None
    fullName: str | None = None
    description: str | None = None
    type_: str | None = Field(default=None, alias="type")
    url: str | None = None
    pid: str | None = None
    startDate: datetime | None = None
    endDate: datetime | None = None


class InvestigationInstrument(EntityModel):
    instrument: Instrument | None = None


class User(EntityModel):
    name: str | None = None
    fullName: str | None = None
    givenName: str | None = None
    familyName: str | None = None
    email: str | None = None
    affiliation: str | None = None
    orcidId: str | None = None


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


class Investigation(EntityModel):
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
    samples: list[Sample] | None = None
    parameters: list[Parameter] | None = None
    publications: list[Publication] | None = None
