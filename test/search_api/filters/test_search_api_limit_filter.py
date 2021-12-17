import pytest

from datagateway_api.src.common.exceptions import FilterError
from datagateway_api.src.search_api.filters import SearchAPILimitFilter
from datagateway_api.src.search_api.query import SearchAPIQuery


class TestSearchAPILimitFilter:
    @pytest.mark.parametrize(
        "limit_value",
        [
            pytest.param(10, id="typical"),
            pytest.param(0, id="low boundary"),
            pytest.param(9999, id="high boundary"),
        ],
    )
    def test_valid_limit_value(self, limit_value):
        test_filter = SearchAPILimitFilter(limit_value)
        test_query = SearchAPIQuery("Document")
        test_filter.apply_filter(test_query)

        assert test_query.query.query.limit == (0, limit_value)

    @pytest.mark.parametrize(
        "limit_value",
        [pytest.param(-50, id="extreme invalid"), pytest.param(-1, id="boundary")],
    )
    def test_invalid_limit_value(self, limit_value):
        with pytest.raises(FilterError):
            SearchAPILimitFilter(limit_value)
