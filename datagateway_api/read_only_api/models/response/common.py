from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, Field, PlainSerializer

DataGatewayDate = Annotated[datetime, PlainSerializer(lambda x: x.isoformat(" "))]


class EntityModel(BaseModel):
    id_: int | None = Field(default=None, alias="id")
    createTime: DataGatewayDate | None = None
    modTime: DataGatewayDate | None = None


class Facility(EntityModel):
    name: str | None = None
    fullName: str | None = None
    description: str | None = None
    url: str | None = None
    daysUntilRelease: int | None = None


class EntityType(EntityModel):
    name: str | None = None
    description: str | None = None


class User(EntityModel):
    name: str | None = None
    fullName: str | None = None
    givenName: str | None = None
    familyName: str | None = None
    email: str | None = None
    affiliation: str | None = None
    orcidId: str | None = None


class BaseDataCollection(EntityModel):
    doi: str | None = None


class DataPublicationType(EntityModel):
    name: str | None = None
    description: str | None = None


class BaseDataPublication(EntityModel):
    title: str | None = None
    pid: str | None = None
    description: str | None = None
    subject: str | None = None
    internalId: str | None = None
    publicationDate: DataGatewayDate | None = None

    type_: DataPublicationType | None = Field(default=None, alias="type")


class InstrumentScientist(EntityModel):
    user: User | None = None


class Instrument(EntityModel):
    name: str | None = None
    fullName: str | None = None
    description: str | None = None
    type_: str | None = Field(default=None, alias="type")
    url: str | None = None
    pid: str | None = None
    startDate: DataGatewayDate | None = None
    endDate: DataGatewayDate | None = None

    instrumentScientists: list[InstrumentScientist] | None = None


class InvestigationInstrument(EntityModel):
    instrument: Instrument | None = None


class InvestigationUser(EntityModel):
    role: str | None = None

    user: User | None = None


class BaseInvestigation(EntityModel):
    name: str | None = None
    visitId: str | None = None
    title: str | None = None
    summary: str | None = None
    doi: str | None = None
    startDate: DataGatewayDate | None = None
    endDate: DataGatewayDate | None = None
    releaseDate: DataGatewayDate | None = None
    fileCount: int | None = None
    fileSize: int | None = None

    facility: Facility | None = None
    type_: EntityType | None = Field(default=None, alias="type")
    investigationInstruments: list[InvestigationInstrument] | None = None
    investigationUsers: list[InvestigationUser] | None = None


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
    dateTimeValue: DataGatewayDate | None = None
    numericValue: float | None = None
    error: float | None = None
    rangeBottom: float | None = None
    rangeTop: float | None = None

    type_: ParameterType | None = Field(default=None, alias="type")
