from enum import StrEnum
from typing import Literal

from pydantic import Field

from datagateway_api.read_only_api.models.request.common import (
    INCLUDE_DESCRIPTION,
    ORDER_DESCRIPTION,
    WHERE_DESCRIPTION,
    AnyFilter,
    CommonCountFilters,
    CommonGetFilters,
    CommonSearchFilters,
    CommonWhereFilters,
)

INSTRUMENT_WHERE_DESCRIPTION = WHERE_DESCRIPTION.format(queryable_fields="'name', 'fullName', and 'type'")
INSTRUMENT_ORDER_DESCRIPTION = ORDER_DESCRIPTION.format(orderable_fields="'fullName' and 'type'")
INSTRUMENT_INCLUDE_DESCRIPTION = INCLUDE_DESCRIPTION.format(includable_paths="'instrumentScientists.user'")


class InstrumentOrderEnum(StrEnum):
    FULL_NAME_ASC = "fullName asc"
    FULL_NAME_DESC = "fullName desc"
    TYPE_ASC = "type asc"
    TYPE_DESC = "type desc"


class InstrumentWhereFilters(CommonWhereFilters):
    name: AnyFilter = None
    fullName: AnyFilter = None
    type_: AnyFilter = Field(default=None, alias="type")


class InstrumentCountFilters(CommonCountFilters):
    where: list[InstrumentWhereFilters] = Field(default=[], description=INSTRUMENT_WHERE_DESCRIPTION)


class InstrumentGetFilters(CommonGetFilters):
    include: list[Literal["instrumentScientists.user"]] = Field(default=[], description=INSTRUMENT_INCLUDE_DESCRIPTION)


class InstrumentSearchFilters(InstrumentCountFilters, CommonSearchFilters):
    order: list[InstrumentOrderEnum] = Field(default=[], description=INSTRUMENT_ORDER_DESCRIPTION)
    include: list[Literal["instrumentScientists.user"]] = Field(default=[], description=INSTRUMENT_INCLUDE_DESCRIPTION)
