import pytest

from datagateway_api.src.common.config import Config
from datagateway_api.src.common.exceptions import FilterError
from datagateway_api.src.common.helpers import get_icat_properties
from datagateway_api.src.search_api.filters import SearchAPISkipFilter
from datagateway_api.src.search_api.query import SearchAPIQuery


class TestSearchAPISkipFilter:
    @pytest.mark.parametrize(
        "skip_value", [pytest.param(10, id="typical"), pytest.param(0, id="boundary")],
    )
    def test_valid_skip_value(self, search_api_query_document, skip_value):
        test_filter = SearchAPISkipFilter(skip_value)
        test_filter.apply_filter(search_api_query_document)

        assert search_api_query_document.icat_query.query.limit == (
            skip_value,
            get_icat_properties(
                Config.config.search_api.icat_url,
                Config.config.search_api.icat_check_cert,
            )["maxEntities"],
        )

    @pytest.mark.parametrize(
        "skip_value",
        [pytest.param(-375, id="extreme invalid"), pytest.param(-1, id="boundary")],
    )
    def test_invalid_skip_value(self, skip_value):
        with pytest.raises(FilterError):
            SearchAPISkipFilter(skip_value)
