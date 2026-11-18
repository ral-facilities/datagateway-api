from datagateway_api.read_only_api.models.response.common import (
    BaseDataCollection,
    BaseDataPublication,
    EntityModel,
    Facility,
    User,
)
from datagateway_api.read_only_api.models.response.datafile import Datafile
from datagateway_api.read_only_api.models.response.dataset import Dataset
from datagateway_api.read_only_api.models.response.investigation import BaseInvestigation


class DataPublicationDate(EntityModel):
    date: str | None = None
    dateType: str | None = None


class DataCollectionInvestigation(EntityModel):
    investigation: BaseInvestigation | None = None


class DataCollectionDataset(EntityModel):
    dataset: Dataset | None = None


class DataCollectionDatafile(EntityModel):
    datafile: Datafile | None = None


class DataCollection(BaseDataCollection):
    dataCollectionInvestigations: list[DataCollectionInvestigation] | None = None
    dataCollectionDatasets: list[DataCollectionDataset] | None = None
    dataCollectionDatafiles: list[DataCollectionDatafile] | None = None


class RelatedItem(EntityModel):
    identifier: str | None = None
    relationType: str | None = None
    relatedItemType: str | None = None
    title: str | None = None
    fullReference: str | None = None

    publication: BaseDataPublication


class Affiliation(EntityModel):
    name: str | None = None
    pid: str | None = None
    fullReference: str | None = None


class DataPublicationUser(EntityModel):
    contributorType: str | None = None
    orderKey: str | None = None
    fullName: str | None = None
    givenName: str | None = None
    familyName: str | None = None
    email: str | None = None

    user: User | None = None
    affiliations: list[Affiliation] | None = None


class DataPublication(BaseDataPublication):
    facility: Facility | None = None
    dates: list[DataPublicationDate] | None = None
    content: DataCollection | None = None
    relatedItems: list[RelatedItem] | None = None
    users: list[DataPublicationUser] | None = None
