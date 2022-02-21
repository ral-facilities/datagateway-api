from icat.query import Query
import pytest

from datagateway_api.src.common.exceptions import SearchAPIError
from datagateway_api.src.datagateway_api.icat.query import ICATQuery
from datagateway_api.src.search_api.query import SearchAPIICATQuery, SearchAPIQuery
from datagateway_api.src.search_api.session_handler import SessionHandler


class TestSearchAPIQuery:
    def test_search_api_query_init(self, test_panosc_mappings):
        panosc_entity_name = "Document"
        test_query = SearchAPIQuery(panosc_entity_name)

        assert test_query.panosc_entity_name == panosc_entity_name
        assert (
            test_query.icat_entity_name
            == test_panosc_mappings.mappings[panosc_entity_name]["base_icat_entity"]
        )

    def test_search_api_query_repr(self, test_panosc_mappings):
        panosc_entity_name = "Document"
        test_query = SearchAPIQuery(panosc_entity_name)
        assert (
            repr(test_query)
            == f"PaNOSC Entity Name: {panosc_entity_name}, ICAT Entity Name:"
            f" {test_panosc_mappings.mappings[panosc_entity_name]['base_icat_entity']},"
            f" ICAT Query: {str(test_query.icat_query.query)}"
        )

    def test_valid_search_api_icat_query_init(self):
        test_query = SearchAPIICATQuery(SessionHandler.client, "Investigation")
        assert isinstance(test_query, ICATQuery)
        assert isinstance(test_query.query, Query)

    def test_invalid_search_api_icat_query_init(self):
        with pytest.raises(SearchAPIError):
            SearchAPIICATQuery(
                SessionHandler.client, "Investigation", includes="UnknownEntity",
            )
