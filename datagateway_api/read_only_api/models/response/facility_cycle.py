from datagateway_api.read_only_api.models.response.common import DataGatewayDate, EntityModel


class FacilityCycle(EntityModel):
    name: str | None = None
    description: str | None = None
    startDate: DataGatewayDate | None = None
    endDate: DataGatewayDate | None = None
