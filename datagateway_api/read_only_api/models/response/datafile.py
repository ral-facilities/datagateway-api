from datetime import datetime

from datagateway_api.read_only_api.models.response.common import EntityModel


class Datafile(EntityModel):
    name: str | None = None
    location: str | None = None
    description: str | None = None
    doi: str | None = None
    checksum: str | None = None
    datafileCreateTime: datetime | None = None
    datafileModTime: datetime | None = None
    fileSize: int | None = None
