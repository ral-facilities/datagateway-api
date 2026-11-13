from enum import StrEnum

from pydantic import Field

from datagateway_api.read_only_api.models.request.common import (
    ORDER_DESCRIPTION,
    WHERE_DESCRIPTION,
    AnyFilter,
    BaseFilters,
    CommonCountFilters,
    CommonSearchFilters,
    CommonWhereFilters,
    EqualFilter,
)

DATAFILE_WHERE_DESCRIPTION = WHERE_DESCRIPTION.format(
    queryable_fields=(
        "'name', 'location', 'datafileCreateTime', 'datafileModTime', 'dataset.id', and "
        "'dataCollectionDatafiles.dataCollection.dataPublications.id'"
    ),
)
DATAFILE_ORDER_DESCRIPTION = ORDER_DESCRIPTION.format(
    orderable_fields="'name', 'location', 'fileSize', 'datafileCreateTime', and 'datafileModTime'",
)


class DatafileOrderEnum(StrEnum):
    NAME_ASC = "name asc"
    NAME_DESC = "name desc"
    LOCATION_ASC = "location asc"
    LOCATION_DESC = "location desc"
    FILE_SIZE_ASC = "fileSize asc"
    FILE_SIZE_DESC = "fileSize desc"
    DATAFILE_CREATE_TIME_ASC = "datafileCreateTime asc"
    DATAFILE_CREATE_TIME_DESC = "datafileCreateTime desc"
    DATAFILE_MOD_TIME_ASC = "datafileModTime asc"
    DATAFILE_MOD_TIME_DESC = "datafileModTime desc"


class DatafileIdFilters(CommonWhereFilters):
    dataset_id: EqualFilter | None = Field(default=None, alias="dataset.id")


class DatafileWhereFilters(DatafileIdFilters):
    data_publication_id: EqualFilter | None = Field(
        default=None,
        alias="dataCollectionDatafiles.dataCollection.dataPublications.id",
    )
    name: AnyFilter = None
    location: AnyFilter = None
    datafileCreateTime: AnyFilter = None
    datafileModTime: AnyFilter = None


class DatafileFindOneFilters(BaseFilters):
    where: list[DatafileIdFilters] = Field(default=[])


class DatafileCountFilters(CommonCountFilters):
    where: list[DatafileWhereFilters] = Field(default=[], description=DATAFILE_WHERE_DESCRIPTION)


class DatafileSearchFilters(DatafileCountFilters, CommonSearchFilters):
    order: list[DatafileOrderEnum] = Field(default=[], description=DATAFILE_ORDER_DESCRIPTION)
