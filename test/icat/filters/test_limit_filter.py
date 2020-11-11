import pytest

from datagateway_api.common.exceptions import FilterError
from datagateway_api.common.filter_order_handler import FilterOrderHandler
from datagateway_api.common.icat.filters import (
    PythonICATLimitFilter,
    PythonICATSkipFilter,
)


class TestICATLimitFilter:
    @pytest.mark.parametrize(
        "limit_value",
        [
            pytest.param(10, id="typical"),
            pytest.param(0, id="low boundary"),
            pytest.param(9999, id="high boundary"),
        ],
    )
    def test_valid_limit_value(self, icat_query, limit_value):
        test_filter = PythonICATLimitFilter(limit_value)
        test_filter.apply_filter(icat_query)

        assert icat_query.limit == (0, limit_value)

    @pytest.mark.parametrize(
        "limit_value",
        [pytest.param(-50, id="extreme invalid"), pytest.param(-1, id="boundary")],
    )
    def test_invalid_limit_value(self, icat_query, limit_value):
        test_filter = PythonICATLimitFilter(limit_value)

        with pytest.raises(FilterError):
            test_filter.apply_filter(icat_query)

    @pytest.mark.parametrize(
        "skip_value, limit_value",
        [
            pytest.param(10, 10, id="identical typical values"),
            pytest.param(0, 0, id="identical low boundary values"),
            pytest.param(15, 25, id="different typical values"),
            pytest.param(0, 9999, id="different boundary values"),
        ],
    )
    def test_limit_and_skip_merge_correctly(self, icat_query, skip_value, limit_value):
        """
        Skip and limit values are set together in Python ICAT, limit value should match
        max entities allowed in one transaction in ICAT as defined in ICAT properties
        """
        skip_filter = PythonICATSkipFilter(skip_value)
        limit_filter = PythonICATLimitFilter(limit_value)

        filter_handler = FilterOrderHandler()
        filter_handler.add_filters([skip_filter, limit_filter])
        filter_handler.merge_python_icat_limit_skip_filters()
        filter_handler.apply_filters(icat_query)

        assert icat_query.limit == (skip_value, limit_value)
