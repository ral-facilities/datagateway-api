import pytest

from datagateway_api.src.common.exceptions import FilterError
from datagateway_api.src.common.filter_order_handler import FilterOrderHandler
from datagateway_api.src.search_api.filters import SearchAPIScoringFilter
from datagateway_api.src.search_api.query import SearchAPIQuery


class TestSearchAPIScoringFilter:
    def test_valid_apply_scoring_filter(self):
        filter_input = SearchAPIScoringFilter("My test query")
        entity_name = "Document"
        expected_query = (
            "SELECT o FROM Investigation o WHERE UPPER(o.summary) like UPPER('%My "
            "test query%')"
        )

        filter_handler = FilterOrderHandler()
        filter_handler.add_filter(filter_input)
        test_query = SearchAPIQuery(entity_name)

        filter_handler.apply_filters(test_query)

        assert str(test_query.icat_query.query) == expected_query

    @pytest.mark.parametrize(
        "query_value",
        [
            pytest.param(1, id="integer value"),
            pytest.param(1.0, id="float value"),
            pytest.param(True, id="boolean value"),
        ],
    )
    def test_invalid_scoring_filter(self, query_value):
        with pytest.raises((FilterError, ValueError)):
            SearchAPIScoringFilter(query_value)
