from datagateway_api.read_only_api.models.response.common import DataGatewayDate, EntityModel, Parameter
from datagateway_api.read_only_api.models.response.dataset import Dataset


class Datafile(EntityModel):
    name: str | None = None
    location: str | None = None
    description: str | None = None
    doi: str | None = None
    checksum: str | None = None
    datafileCreateTime: DataGatewayDate | None = None
    datafileModTime: DataGatewayDate | None = None
    fileSize: int | None = None

    dataset: Dataset | None = None
    parameters: list[Parameter] | None = None
