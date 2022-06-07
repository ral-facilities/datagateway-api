from datagateway_api.src.common.exceptions import SearchAPIError
from datagateway_api.src.datagateway_api.icat.query import ICATQuery
from datagateway_api.src.search_api.condition_setting_query import ConditionSettingQuery
from datagateway_api.src.search_api.panosc_mappings import mappings
from datagateway_api.src.search_api.session_handler import SessionHandler


class SearchAPIQuery:
    def __init__(self, panosc_entity_name, **kwargs):
        self.panosc_entity_name = panosc_entity_name
        self.icat_entity_name = mappings.mappings[panosc_entity_name][
            "base_icat_entity"
        ]
        self.icat_query = SearchAPIICATQuery(
            SessionHandler.client,
            self.icat_entity_name,
            **kwargs,
        )

    def __repr__(self):
        return (
            f"PaNOSC Entity Name: {self.panosc_entity_name}, ICAT Entity Name:"
            f" {self.icat_entity_name}, ICAT Query: {str(self.icat_query.query)}"
        )


class SearchAPIICATQuery(ICATQuery):
    """
    Class which has identical functionality to `ICATQuery` but uses a different
    `__init__` to call `ConditionSettingQuery` instead of the base `Query`. That class
    contains features required for the search API
    """

    def __init__(
        self,
        client,
        entity_name,
        conditions=None,
        aggregate=None,
        includes=None,
        str_conditions=None,
    ):
        try:
            self.query = ConditionSettingQuery(
                client,
                entity_name,
                conditions=conditions,
                aggregate=aggregate,
                includes=includes,
                str_conditions=str_conditions,
            )

            self.query.manual_count = False
        except ValueError as e:
            raise SearchAPIError(
                f"An issue has occurred while creating a query for ICAT: {e}",
            )
