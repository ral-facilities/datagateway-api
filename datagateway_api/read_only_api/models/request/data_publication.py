from enum import StrEnum

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
    EqualFilter,
)

DATA_PUBLICATION_WHERE_DESCRIPTION = WHERE_DESCRIPTION.format(
    queryable_fields=(
        "'title', 'pid', 'publicationDate', 'type.name', 'users.user.name', 'users.orderKey', "
        "'relatedItems.relationType', 'relatedItems.identifier', "
        "'content.dataCollectionInvestigations.investigation.investigationInstruments.instrument.id', and "
        "'content.dataCollectionInvestigations.investigation.dataCollectionInvestigations.dataCollection."
        "dataPublications.id'"
    ),
)
DATA_PUBLICATION_ORDER_DESCRIPTION = ORDER_DESCRIPTION.format(
    orderable_fields="'title', 'pid', 'publicationDate', 'createTime'",
)
DATA_PUBLICATION_INCLUDE_DESCRIPTION = INCLUDE_DESCRIPTION.format(
    includable_paths=(
        "'facility', 'type', 'dates', 'relatedItems', 'relatedItems.publication', 'users', 'users.user', "
        "'users.affiliation', 'content.dataCollectionInvestigations.investigation', "
        "'content.dataCollectionInvestigations.investigation.datasets', "
        "'content.dataCollectionInvestigations.investigation.datasets.type', "
        "'content.dataCollectionInvestigations.investigation.investigationInstruments.instrument', "
        "'content.dataCollectionInvestigations.investigation.investigationUsers.user', "
        "'content.dataCollectionDatasets.dataset', and 'content.dataCollectionDatafiles.datafile'"
    ),
)


class DataPublicationDistinctEnum(StrEnum):
    ID = "id"
    TITLE = "title"
    PID = "pid"


class DataPublicationWhereFilters(CommonWhereFilters):
    title: AnyFilter = None
    pid: AnyFilter = None
    publicationDate: AnyFilter = None
    type_name: AnyFilter = Field(default=None, alias="type.name")
    user_name: EqualFilter | None = Field(default=None, alias="users.user.name")
    order_key: AnyFilter = Field(default=None, alias="users.orderKey")
    related_items_relation_type: EqualFilter | None = Field(default=None, alias="relatedItems.relationType")
    related_items_identifier: EqualFilter | None = Field(default=None, alias="relatedItems.identifier")
    investigation_instrument_id: EqualFilter | None = Field(
        default=None,
        alias="content.dataCollectionInvestigations.investigation.investigationInstruments.instrument.id",
    )
    investigation_data_publication_id: EqualFilter | None = Field(
        default=None,
        alias=(
            "content.dataCollectionInvestigations.investigation.dataCollectionInvestigations.dataCollection."
            "dataPublications.id"
        ),
    )


class DataPublicationOrderEnum(StrEnum):
    TITLE_ASC = "title asc"
    TITLE_DESC = "title desc"
    PID_ASC = "pid asc"
    PID_DESC = "pid desc"
    PUBLICATION_DATE_ASC = "publicationDate asc"
    PUBLICATION_DATE_DESC = "publicationDate desc"
    CREATE_TIME_ASC = "createTime asc"
    CREATE_TIME_DESC = "createTime desc"


class DataPublicationIncludeEnum(StrEnum):
    FACILITY = "facility"
    TYPE = "type"
    DATES = "dates"
    RELATED_ITEMS = "relatedItems"
    RELATED_ITEMS_PUBLICATION = "relatedItems.publication"
    USERS = "users"
    USERS_USER = "users.user"
    USERS_AFFILIATIONS = "users.affiliations"
    INVESTIGATIONS = "content.dataCollectionInvestigations.investigation"
    INVESTIGATIONS_DATASETS = "content.dataCollectionInvestigations.investigation.datasets"
    INVESTIGATIONS_DATASETS_TYPE = "content.dataCollectionInvestigations.investigation.datasets.type"
    INVESTIGATIONS_INSTRUMENT = "content.dataCollectionInvestigations.investigation.investigationInstruments.instrument"
    INVESTIGATION_USERS = "content.dataCollectionInvestigations.investigation.investigationUsers.user"
    DATASETS = "content.dataCollectionDatasets.dataset"
    DATAFILES = "content.dataCollectionDatafiles.datafile"


class DataPublicationCountFilters(CommonCountFilters):
    distinct: list[DataPublicationDistinctEnum] = Field(
        default=[],
        description="Return distinct value(s) of the specified fields. Only these fields will be returned.",
    )
    where: list[DataPublicationWhereFilters] = Field(default=[], description=DATA_PUBLICATION_WHERE_DESCRIPTION)


class DataPublicationGetFilters(CommonGetFilters):
    include: list[DataPublicationIncludeEnum] = Field(default=[], description=DATA_PUBLICATION_INCLUDE_DESCRIPTION)


class DataPublicationSearchFilters(DataPublicationCountFilters, CommonSearchFilters):
    include: list[DataPublicationIncludeEnum] = Field(default=[], description=DATA_PUBLICATION_INCLUDE_DESCRIPTION)
    order: list[DataPublicationOrderEnum] = Field(default=[], description=DATA_PUBLICATION_ORDER_DESCRIPTION)
