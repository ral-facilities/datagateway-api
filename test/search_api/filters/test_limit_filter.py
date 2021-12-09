import pytest

from datagateway_api.src.common.exceptions import FilterError
from datagateway_api.src.search_api.filters import SearchAPILimitFilter


class TestSearchAPILimitFilter:
    @pytest.mark.parametrize(
        "limit_value",
        [
            pytest.param(10, id="typical"),
            pytest.param(0, id="low boundary"),
            pytest.param(9999, id="high boundary"),
        ],
    )
    def test_valid_limit_value(self, icat_query, limit_value):
        test_filter = SearchAPILimitFilter(limit_value)
        test_filter.apply_filter(icat_query)

        assert icat_query.limit == (0, limit_value)

    @pytest.mark.parametrize(
        "limit_value",
        [pytest.param(-50, id="extreme invalid"), pytest.param(-1, id="boundary")],
    )
    def test_invalid_limit_value(self, icat_query, limit_value):
        with pytest.raises(FilterError):
            SearchAPILimitFilter(limit_value)
