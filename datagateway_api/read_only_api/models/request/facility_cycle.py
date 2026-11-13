from enum import StrEnum

from pydantic import Field

from datagateway_api.read_only_api.models.request.common import (
    ORDER_DESCRIPTION,
    WHERE_DESCRIPTION,
    AnyFilter,
    CommonCountFilters,
    CommonSearchFilters,
    CommonWhereFilters,
    EqualFilter,
)

FACILITY_CYCLE_WHERE_DESCRIPTION = WHERE_DESCRIPTION.format(
    queryable_fields="'name', 'investigationFacilityCycles.investigation.investigationInstruments.instrument.id'",
)
FACILITY_CYCLE_ORDER_DESCRIPTION = ORDER_DESCRIPTION.format(orderable_fields="'name', 'startDate', and 'endDate'")


class FacilityCycleDistinctEnum(StrEnum):
    ID = "id"
    NAME = "name"
    START_DATE = "startDate"
    END_DATE = "endDate"


class FacilityCycleWhereFilters(CommonWhereFilters):
    instrumentId: EqualFilter | None = Field(
        default=None,
        alias="investigationFacilityCycles.investigation.investigationInstruments.instrument.id",
    )
    name: AnyFilter = None
    startDate: AnyFilter = None
    endDate: AnyFilter = None


class FacilityCycleOrderEnum(StrEnum):
    NAME_ASC = "name asc"
    NAME_DESC = "name desc"
    START_DATE_ASC = "startDate asc"
    START_DATE_DESC = "startDate desc"
    END_DATE_ASC = "endDate asc"
    END_DATE_DESC = "endDate desc"


class FacilityCycleCountFilters(CommonCountFilters):
    distinct: list[FacilityCycleDistinctEnum] = Field(
        default=[],
        description="Return distinct value(s) of the specified fields. Only these fields will be returned.",
    )
    where: list[FacilityCycleWhereFilters] = Field(default=[], description=FACILITY_CYCLE_WHERE_DESCRIPTION)


class FacilityCycleSearchFilters(FacilityCycleCountFilters, CommonSearchFilters):
    order: list[FacilityCycleOrderEnum] = Field(default=[], description=FACILITY_CYCLE_ORDER_DESCRIPTION)
