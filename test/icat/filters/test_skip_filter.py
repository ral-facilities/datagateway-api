import pytest

from datagateway_api.common.config import config
from datagateway_api.common.exceptions import FilterError
from datagateway_api.common.icat.filters import PythonICATSkipFilter


class TestICATSkipFilter:
    @pytest.mark.parametrize(
        "skip_value", [pytest.param(10, id="typical"), pytest.param(0, id="boundary")],
    )
    def test_valid_skip_value(self, icat_query, skip_value):
        test_filter = PythonICATSkipFilter(skip_value)
        test_filter.apply_filter(icat_query)

        assert icat_query.limit == (
            skip_value,
            config.get_icat_properties()["maxEntities"],
        )

    @pytest.mark.parametrize(
        "skip_value",
        [pytest.param(-375, id="extreme invalid"), pytest.param(-1, id="boundary")],
    )
    def test_invalid_skip_value(self, icat_query, skip_value):
        test_filter = PythonICATSkipFilter(skip_value)

        with pytest.raises(FilterError):
            test_filter.apply_filter(icat_query)
