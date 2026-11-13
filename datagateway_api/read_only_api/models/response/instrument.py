from datetime import datetime

from pydantic import Field

from datagateway_api.read_only_api.models.response.common import EntityModel, User


class InstrumentScientist(EntityModel):
    user: User | None = None


class Instrument(EntityModel):
    name: str | None = None
    fullName: str | None = None
    description: str | None = None
    type_: str | None = Field(default=None, alias="type")
    url: str | None = None
    pid: str | None = None
    startDate: datetime | None = None
    endDate: datetime | None = None

    instrumentScientists: list[InstrumentScientist] | None = None
