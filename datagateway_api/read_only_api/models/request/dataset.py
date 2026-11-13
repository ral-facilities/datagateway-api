from enum import StrEnum

from pydantic import Field

from datagateway_api.read_only_api.models.request.common import (
    INCLUDE_DESCRIPTION,
    ORDER_DESCRIPTION,
    WHERE_DESCRIPTION,
    AnyFilter,
    BaseFilters,
    CommonCountFilters,
    CommonGetFilters,
    CommonSearchFilters,
    CommonWhereFilters,
    EqualFilter,
)

DATASET_WHERE_DESCRIPTION = WHERE_DESCRIPTION.format(
    queryable_fields=(
        "'name', 'createTime', 'modTime', 'investigation.id', and "
        "'dataCollectionDatasets.dataCollection.dataPublications.id'"
    ),
)
DATASET_ORDER_DESCRIPTION = ORDER_DESCRIPTION.format(
    orderable_fields="'name', 'fileCount', 'fileSize', 'createTime', and 'modTime'",
)
DATASET_INCLUDE_DESCRIPTION = INCLUDE_DESCRIPTION.format(includable_paths="'type'")


class DatasetOrderEnum(StrEnum):
    NAME_ASC = "name asc"
    NAME_DESC = "name desc"
    FILE_COUNT_ASC = "fileCount asc"
    FILE_COUNT_DESC = "fileCount desc"
    FILE_SIZE_ASC = "fileSize asc"
    FILE_SIZE_DESC = "fileSize desc"
    CREATE_TIME_ASC = "createTime asc"
    CREATE_TIME_DESC = "createTime desc"
    MOD_TIME_ASC = "modTime asc"
    MOD_TIME_DESC = "modTime desc"


class DatasetIdFilters(CommonWhereFilters):
    investigation_id: EqualFilter | None = Field(default=None, alias="investigation.id")


class DatasetWhereFilter(DatasetIdFilters):
    data_publication_id: EqualFilter | None = Field(
        default=None,
        alias="dataCollectionDatasets.dataCollection.dataPublications.id",
    )
    name: AnyFilter = None
    createTime: AnyFilter = None
    modTime: AnyFilter = None


class DatasetIncludeEnum(StrEnum):
    TYPE = "type"


class DatasetFindOneFilters(BaseFilters):
    where: list[DatasetIdFilters] = Field(default=[])


class DatasetCountFilters(CommonCountFilters):
    where: list[DatasetWhereFilter] = Field(default=[], description=DATASET_WHERE_DESCRIPTION)


class DatasetGetFilters(CommonGetFilters):
    include: list[DatasetIncludeEnum] = Field(default=[], description=DATASET_INCLUDE_DESCRIPTION)


class DatasetSearchFilters(DatasetCountFilters, CommonSearchFilters):
    order: list[DatasetOrderEnum] = Field(default=[], description=DATASET_ORDER_DESCRIPTION)
    include: list[DatasetIncludeEnum] = Field(default=[], description=DATASET_INCLUDE_DESCRIPTION)
