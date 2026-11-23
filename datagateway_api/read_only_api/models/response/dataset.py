from pydantic import Field

from datagateway_api.read_only_api.models.response.common import (
    BaseInvestigation,
    DataGatewayDate,
    EntityModel,
    EntityType,
)


class Dataset(EntityModel):
    name: str | None = None
    location: str | None = None
    description: str | None = None
    doi: str | None = None
    startDate: DataGatewayDate | None = None
    endDate: DataGatewayDate | None = None
    fileCount: int | None = None
    fileSize: int | None = None
    complete: bool | None = None

    type_: EntityType | None = Field(default=None, alias="type")
    investigation: BaseInvestigation | None = None
