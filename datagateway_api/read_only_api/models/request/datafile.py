from enum import StrEnum
from typing import Annotated

from pydantic import AfterValidator, Field

from datagateway_api.read_only_api.models.request.common import (
    AnyFilter,
    CommonFilters,
    CommonWhereFilter,
    order_description,
    validate_order,
    where_description,
)

DATAFILE_QUERYABLE_FIELDS = ("name", "location", "datafileCreateTime")
DATAFILE_ORDERABLE_FIELDS = ("name", "location", "fileSize", "datafileCreateTime")


class DatafileOrderEnum(StrEnum):
    NAME_ASC = "name asc"
    NAME_DESC = "name desc"
    LOCATION_ASC = "location asc"
    LOCATION_DESC = "location desc"
    FILE_SIZE_ASC = "fileSize asc"
    FILE_SIZE_DESC = "fileSize desc"
    DATAFILE_CREATE_TIME_ASC = "datafileCreateTime asc"
    DATAFILE_CREATE_TIME_DESC = "datafileCreateTime desc"


class DatafileWhereFilter(CommonWhereFilter):
    location: AnyFilter = None
    datafileCreateTime: AnyFilter = None


class DatafileFilters(CommonFilters):
    where: list[DatafileWhereFilter] = Field(default=[], description=where_description(DATAFILE_QUERYABLE_FIELDS))
    order: Annotated[list[DatafileOrderEnum], AfterValidator(validate_order)] = Field(
        default=[],
        description=order_description(DATAFILE_ORDERABLE_FIELDS),
    )
