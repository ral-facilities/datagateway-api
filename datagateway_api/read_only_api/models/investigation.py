from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class Instrument(BaseModel):
    name: str
    fullName: str | None = None
    description: str | None = None
    type: str | None = None
    url: str | None = None
    pid: str | None = None
    startDate: datetime | None = None
    endDate: datetime | None = None


class InvestigationInstrument(BaseModel):
    instrument: Instrument


class User(BaseModel):
    name: str
    fullName: str | None = None
    givenName: str | None = None
    familyName: str | None = None
    email: str | None = None
    affiliation: str | None = None
    orcid: str | None = None


class InvestigationUser(BaseModel):
    role: str

    user: User


class SampleType(BaseModel):
    name: str
    molecularFormula: str
    safetyInformation: str | None = None


class Sample(BaseModel):
    name: str
    pid: str | None = None

    type: SampleType


class ParameterValueType(StrEnum):
    STRING = "STRING"
    DATE_AND_TIME = "DATE_AND_TIME"
    NUMERIC = "NUMERIC"


class ParameterType(BaseModel):
    name: str
    valueType: ParameterValueType
    units: str
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


class Parameter(BaseModel):
    stringValue: str | None = None
    dateTimeValue: datetime | None = None
    numericValue: float | None = None
    error: float | None = None
    rangeBottom: float | None = None
    rangeTop: float | None = None

    type: ParameterType


class Publication(BaseModel):
    fullReference: str
    doi: str | None = None
    url: str | None = None
    repository: str | None = None
    repositoryId: str | None = None


class Investigation(BaseModel):
    name: str
    visitId: str
    title: str
    summary: str | None = None
    doi: str | None = None
    startDate: datetime | None = None
    endDate: datetime | None = None
    releaseDate: datetime | None = None
    fileCount: int | None = None
    fileSize: int | None = None

    investigationInstruments: list[InvestigationInstrument]
    investigationUsers: list[InvestigationUser] | None = None
    samples: list[Sample] | None = None
    parameters: list[Parameter] | None = None
    publications: list[Publication] | None = None
