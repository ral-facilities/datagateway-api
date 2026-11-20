from pydantic import Field

from datagateway_api.read_only_api.models.response.common import (
    BaseDataCollection,
    BaseDataPublication,
    BaseInvestigation,
    EntityModel,
    Parameter,
)
from datagateway_api.read_only_api.models.response.dataset import Dataset
from datagateway_api.read_only_api.models.response.facility_cycle import FacilityCycle


class SampleType(EntityModel):
    name: str | None = None
    molecularFormula: str | None = None
    safetyInformation: str | None = None


class Sample(EntityModel):
    name: str | None = None
    pid: str | None = None

    type_: SampleType | None = Field(default=None, alias="type")


class Publication(EntityModel):
    fullReference: str | None = None
    doi: str | None = None
    url: str | None = None
    repository: str | None = None
    repositoryId: str | None = None


class InvestigationFacilityCycle(EntityModel):
    facilityCycle: FacilityCycle | None = None


class DataCollection(BaseDataCollection):
    dataPublications: list[BaseDataPublication] | None = None


class DataCollectionInvestigation(EntityModel):
    dataCollection: DataCollection | None = None


class Investigation(BaseInvestigation):
    datasets: list[Dataset] | None = None
    samples: list[Sample] | None = None
    parameters: list[Parameter] | None = None
    publications: list[Publication] | None = None
    investigationFacilityCycles: list[InvestigationFacilityCycle] | None = None
    dataCollectionInvestigations: list[DataCollectionInvestigation] | None = None
