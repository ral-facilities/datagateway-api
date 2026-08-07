from enum import StrEnum
from typing import Annotated

from pydantic import AfterValidator, Field

from datagateway_api.read_only_api.models.request.common import (
    ORDER_DESCRIPTION,
    WHERE_DESCRIPTION,
    AnyFilter,
    CommonFilters,
    CommonWhereFilter,
    validate_order,
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


class DatafileWhereFilter(CommonWhereFilter):
    location: AnyFilter = None
    datafileCreateTime: AnyFilter = None


class DatafileFilters(CommonFilters):
    where: list[DatafileWhereFilter] = Field(
        default=[],
        description=WHERE_DESCRIPTION.format(queryable_fields="'name', 'location', and 'datafileCreateTime'"),
    )
    order: Annotated[list[DatafileOrderEnum], AfterValidator(validate_order)] = Field(
        default=[],
        description=ORDER_DESCRIPTION.format(
            orderable_fields="'name', 'location', 'fileSize', and 'datafileCreateTime'",
        ),
    )
