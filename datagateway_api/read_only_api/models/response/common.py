from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class EntityModel(BaseModel):
    id_: int | None = Field(default=None, alias="id")
    createTime: datetime | None = None
    modTime: datetime | None = None


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
    publicationDate: datetime | None = None

    type_: DataPublicationType | None = Field(default=None, alias="type")


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
