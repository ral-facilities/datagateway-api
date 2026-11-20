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

DATAFILE_WHERE_DESCRIPTION = WHERE_DESCRIPTION.format(
    queryable_fields=(
        "'name', 'location', 'datafileCreateTime', 'datafileModTime', 'dataset.id', and "
        "'dataCollectionDatafiles.dataCollection.dataPublications.id'"
    ),
)
DATAFILE_ORDER_DESCRIPTION = ORDER_DESCRIPTION.format(
    orderable_fields="'name', 'location', 'fileSize', 'datafileCreateTime', and 'datafileModTime'",
)
DATAFILE_INCLUDE_DESCRIPTION = INCLUDE_DESCRIPTION.format(includable_paths="'parameters.type'")


class DatafileOrderEnum(StrEnum):
    ID_ASC = "id asc"
    ID_DESC = "id desc"
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


class DatafileIncludeEnum(StrEnum):
    PARAMETERS = "parameters.type"


class DatafileFindOneFilters(BaseFilters):
    where: list[DatafileIdFilters] = Field(default=[])


class DatafileCountFilters(CommonCountFilters):
    where: list[DatafileWhereFilters] = Field(default=[], description=DATAFILE_WHERE_DESCRIPTION)


class DatafileGetFilters(CommonGetFilters):
    include: list[DatafileIncludeEnum] = Field(default=[], description=DATAFILE_INCLUDE_DESCRIPTION)


class DatafileSearchFilters(DatafileCountFilters, CommonSearchFilters):
    order: list[DatafileOrderEnum] = Field(default=[], description=DATAFILE_ORDER_DESCRIPTION)
    include: list[DatafileIncludeEnum] = Field(default=[], description=DATAFILE_INCLUDE_DESCRIPTION)
