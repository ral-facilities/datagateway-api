from enum import StrEnum

from pydantic import BaseModel, Field

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

INVESTIGATION_WHERE_DESCRIPTION = WHERE_DESCRIPTION.format(
    queryable_fields=(
        "'name', 'title', 'visitId', 'doi', 'startDate', 'endDate', 'investigationFacilityCycles.facilityCycle.id', "
        "'investigationInstruments.instrument.id', 'investigationInstruments.instrument.name', "
        "'investigationUsers.role', 'investigationUsers.user.name', and 'investigationUsers.user.fullName'"
    ),
)
INVESTIGATION_ORDER_DESCRIPTION = ORDER_DESCRIPTION.format(
    orderable_fields=(
        "'name', 'title', 'visitId', 'doi', 'fileSize', 'startDate', 'endDate', and "
        "'investigationInstruments.instrument.name'"
    ),
)
INVESTIGATION_INCLUDE_DESCRIPTION = INCLUDE_DESCRIPTION.format(
    includable_paths=(
        "'investigationInstruments.instrument', 'investigationUsers.user', 'samples.type', 'parameters.type', "
        "'publications', 'datasets', 'investigationFacilityCycles.facilityCycle', and "
        "'dataCollectionInvestigations.dataCollection.dataPublications.type'"
    ),
)


class InvestigationDistinctEnum(StrEnum):
    ID = "id"
    TITLE = "title"
    NAME = "name"


class InvestigationOrderEnum(StrEnum):
    TITLE_ASC = "title asc"
    TITLE_DESC = "title desc"
    NAME_ASC = "name asc"
    NAME_DESC = "name desc"
    VISIT_ID_ASC = "visitId asc"
    VISIT_ID_DESC = "visitId desc"
    DOI_ASC = "doi asc"
    DOI_DESC = "doi desc"
    FILE_SIZE_ASC = "fileSize asc"
    FILE_SIZE_DESC = "fileSize desc"
    START_DATE_ASC = "startDate asc"
    START_DATE_DESC = "startDate desc"
    END_DATE_ASC = "endDate asc"
    END_DATE_DESC = "endDate desc"
    INSTRUMENT_NAME_ASC = "investigationInstruments.instrument.name asc"
    INSTRUMENT_NAME_DESC = "investigationInstruments.instrument.name desc"


class InvestigationNameFilter(BaseModel):
    name: AnyFilter = None


class InvestigationWhereFilter(CommonWhereFilters):
    title: AnyFilter = None
    name: AnyFilter = None
    visitId: AnyFilter = None
    doi: AnyFilter = None
    startDate: AnyFilter = None
    endDate: AnyFilter = None
    facilityCycleId: EqualFilter | None = Field(default=None, alias="investigationFacilityCycles.facilityCycle.id")
    instrumentId: EqualFilter | None = Field(default=None, alias="investigationInstruments.instrument.id")
    data_publication_id: EqualFilter | None = Field(
        default=None,
        alias="dataCollectionInvestigations.dataCollection.dataPublications.id",
    )
    instrumentName: AnyFilter = Field(default=None, alias="investigationInstruments.instrument.name")
    userRole: AnyFilter = Field(default=None, alias="investigationUsers.role")
    userName: AnyFilter = Field(default=None, alias="investigationUsers.user.name")
    userFullName: AnyFilter = Field(default=None, alias="investigationUsers.user.fullName")


class InvestigationIncludeEnum(StrEnum):
    INSTRUMENTS = "investigationInstruments.instrument"
    USERS = "investigationUsers.user"
    SAMPLES = "samples.type"
    PARAMETERS = "parameters.type"
    PUBLICATIONS = "publications"
    DATASETS = "datasets"
    FACILITY_CYCLES = "investigationFacilityCycles.facilityCycle"
    DATA_PUBLICATION_TYPE = "dataCollectionInvestigations.dataCollection.dataPublications.type"


class InvestigationFindOneFilters(BaseFilters):
    where: list[InvestigationNameFilter] = Field(default=[])


class InvestigationCountFilters(CommonCountFilters):
    distinct: list[InvestigationDistinctEnum] = Field(
        default=[],
        description="Return distinct value(s) of the specified fields. Only these fields will be returned.",
    )
    where: list[InvestigationWhereFilter] = Field(default=[], description=INVESTIGATION_WHERE_DESCRIPTION)


class InvestigationGetFilters(CommonGetFilters):
    include: list[InvestigationIncludeEnum] = Field(default=[], description=INVESTIGATION_INCLUDE_DESCRIPTION)


class InvestigationSearchFilters(InvestigationCountFilters, CommonSearchFilters):
    order: list[InvestigationOrderEnum] = Field(default=[], description=INVESTIGATION_ORDER_DESCRIPTION)
    include: list[InvestigationIncludeEnum] = Field(default=[], description=INVESTIGATION_INCLUDE_DESCRIPTION)
