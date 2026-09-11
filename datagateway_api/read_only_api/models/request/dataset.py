from enum import StrEnum
from typing import Annotated

from pydantic import AfterValidator, Field

from datagateway_api.read_only_api.models.request.common import (
    INCLUDE_DESCRIPTION,
    ORDER_DESCRIPTION,
    WHERE_DESCRIPTION,
    AnyFilter,
    CommonAndIncludeFilters,
    CommonWhereFilter,
    validate_order,
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


class DatasetWhereFilter(CommonWhereFilter):
    createTime: AnyFilter = None
    modTime: AnyFilter = None


class DatasetIncludeEnum(StrEnum):
    TYPE = "type"


class DatasetFilters(CommonAndIncludeFilters):
    where: list[DatasetWhereFilter] = Field(
        default=[],
        description=WHERE_DESCRIPTION.format(queryable_fields="'name', 'createTime', and 'modTime'"),
    )
    order: Annotated[list[DatasetOrderEnum], AfterValidator(validate_order)] = Field(
        default=[],
        description=ORDER_DESCRIPTION.format(
            orderable_fields="'name', 'fileCount', 'fileSize', 'createTime', and 'modTime'",
        ),
    )
    include: list[DatasetIncludeEnum] = Field(default=[], description=DATASET_INCLUDE_DESCRIPTION)
