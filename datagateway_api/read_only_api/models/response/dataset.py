from datetime import datetime

from pydantic import Field

from datagateway_api.read_only_api.models.response.common import EntityModel


class DatasetType(EntityModel):
    name: str | None = None
    description: str | None = None


class Dataset(EntityModel):
    name: str | None = None
    location: str | None = None
    description: str | None = None
    doi: str | None = None
    startDate: datetime | None = None
    endDate: datetime | None = None
    fileCount: int | None = None
    fileSize: int | None = None
    complete: bool | None = None

    type_: DatasetType | None = Field(default=None, alias="type")
