from enum import StrEnum
from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field, model_serializer

from datagateway_api.datagateway_api.icat.filters import PythonICATDistinctFieldFilter
from datagateway_api.read_only_api.models.request.common import (
    DISTINCT_DESCRIPTION,
    AnyFilter,
    CommonAndIncludeFilters,
    CommonWhereFilter,
    include_description,
    order_description,
    validate_order,
    where_description,
)

INVESTIGATION_QUERYABLE_FIELDS = (
    "name",
    "title",
    "visitId",
    "startDate",
    "endDate",
    "investigationInstruments.instrument.name",
)
INVESTIGATION_ORDERABLE_FIELDS = ("name", "title", "visitId", "fileSize", "startDate", "endDate")
INVESTIGATION_INCLUDABLE_PATHS = (
    "investigationInstruments.instrument",
    "investigationUsers.user",
    "samples.type",
    "parameters.type",
    "publications",
)
INVESTIGATION_INCLUDE_DESCRIPTION = include_description(INVESTIGATION_INCLUDABLE_PATHS)


class InvestigationDistinctEnum(StrEnum):
    TITLE = "title"
    NAME = "name"


class InvestigationOrderEnum(StrEnum):
    TITLE_ASC = "title asc"
    TITLE_DESC = "title desc"
    NAME_ASC = "name asc"
    NAME_DESC = "name desc"
    VISIT_ID_ASC = "visitId asc"
    VISIT_ID_DESC = "visitId desc"
    FILE_SIZE_ASC = "fileSize asc"
    FILE_SIZE_DESC = "fileSize desc"
    START_DATE_ASC = "startDate asc"
    START_DATE_DESC = "startDate desc"
    END_DATE_ASC = "endDate asc"
    END_DATE_DESC = "endDate desc"


class TitleFilter(BaseModel):
    title: AnyFilter


class VisitIdFilter(BaseModel):
    visitId: AnyFilter


class StartDateFilter(BaseModel):
    startDate: AnyFilter


class EndDateFilter(BaseModel):
    endDate: AnyFilter


class InstrumentNameFilter(BaseModel):
    instrumentName: AnyFilter = Field(alias="investigationInstruments.instrument.name")


class InvestigationWhereFilter(CommonWhereFilter):
    title: AnyFilter = None
    visitId: AnyFilter = None
    startDate: AnyFilter = None
    endDate: AnyFilter = None
    instrumentName: AnyFilter = Field(default=None, alias="investigationInstruments.instrument.name")


class InvestigationIncludeEnum(StrEnum):
    INSTRUMENTS = "investigationInstruments.instrument"
    USERS = "investigationUsers.user"
    SAMPLES = "samples.type"
    PARAMETERS = "parameters.type"
    PUBLICATIONS = "publications"


class InvestigationFilters(CommonAndIncludeFilters):
    distinct: list[InvestigationDistinctEnum] = Field(default=[], description=DISTINCT_DESCRIPTION)
    where: list[InvestigationWhereFilter] = Field(
        default=[],
        description=where_description(INVESTIGATION_QUERYABLE_FIELDS),
    )
    order: Annotated[list[InvestigationOrderEnum], AfterValidator(validate_order)] = Field(
        default=[],
        description=order_description(INVESTIGATION_ORDERABLE_FIELDS),
    )
    include: list[InvestigationIncludeEnum] = Field(default=[], description=INVESTIGATION_INCLUDE_DESCRIPTION)

    @model_serializer(mode="plain")
    def serialize(self) -> list:
        filters = super().serialize()
        if self.distinct:
            filters.insert(0, PythonICATDistinctFieldFilter([d.value for d in self.distinct]))

        return filters
