from datetime import datetime

from pydantic import BaseModel, Field


class EntityModel(BaseModel):
    id_: int | None = Field(default=None, alias="id")


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

    type_: DataPublicationType | None = None
