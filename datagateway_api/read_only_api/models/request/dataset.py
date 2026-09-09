from enum import StrEnum
from typing import Annotated

from pydantic import AfterValidator, Field

from datagateway_api.read_only_api.models.request.common import (
    AnyFilter,
    CommonAndIncludeFilters,
    CommonWhereFilter,
    include_description,
    order_description,
    validate_order,
    where_description,
)

DATASET_QUERYABLE_FIELDS = ("name", "createTime", "modTime")
DATASET_ORDERABLE_FIELDS = ("name", "fileCount", "fileSize", "createTime", "modTime")
DATASET_INCLUDABLE_PATHS = ("type",)
DATASET_INCLUDE_DESCRIPTION = include_description(DATASET_INCLUDABLE_PATHS)


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


class DatasetWhereFilter(CommonWhereFilter):
    createTime: AnyFilter = None
    modTime: AnyFilter = None


class DatasetIncludeEnum(StrEnum):
    TYPE = "type"


class DatasetFilters(CommonAndIncludeFilters):
    where: list[DatasetWhereFilter] = Field(default=[], description=where_description(DATASET_QUERYABLE_FIELDS))
    order: Annotated[list[DatasetOrderEnum], AfterValidator(validate_order)] = Field(
        default=[],
        description=order_description(DATASET_ORDERABLE_FIELDS),
    )
    include: list[DatasetIncludeEnum] = Field(default=[], description=DATASET_INCLUDE_DESCRIPTION)
