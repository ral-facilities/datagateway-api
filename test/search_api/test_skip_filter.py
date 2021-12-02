import pytest

from datagateway_api.src.common.config import config
from datagateway_api.src.common.exceptions import FilterError
from datagateway_api.src.common.helpers import get_icat_properties
from datagateway_api.src.search_api.filters import SearchAPISkipFilter


class TestSearchAPISkipFilter:
    @pytest.mark.parametrize(
        "skip_value", [pytest.param(10, id="typical"), pytest.param(0, id="boundary")],
    )
    def test_valid_skip_value(self, icat_query, skip_value):
        test_filter = SearchAPISkipFilter(skip_value)
        test_filter.apply_filter(icat_query)

        assert icat_query.limit == (
            skip_value,
            get_icat_properties(
                config.search_api.icat_url, config.search_api.icat_check_cert,
            )["maxEntities"],
        )

    @pytest.mark.parametrize(
        "skip_value",
        [pytest.param(-375, id="extreme invalid"), pytest.param(-1, id="boundary")],
    )
    def test_invalid_skip_value(self, icat_query, skip_value):
        with pytest.raises(FilterError):
            SearchAPISkipFilter(skip_value)
