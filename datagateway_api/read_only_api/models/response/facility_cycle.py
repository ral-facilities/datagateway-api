from datetime import datetime

from datagateway_api.read_only_api.models.response.common import EntityModel


class FacilityCycle(EntityModel):
    name: str | None = None
    description: str | None = None
    startDate: datetime | None = None
    endDate: datetime | None = None
