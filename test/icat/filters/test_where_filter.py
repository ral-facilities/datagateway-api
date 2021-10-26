import pytest

from datagateway_api.common.datagateway_api.filter_order_handler import (
    FilterOrderHandler,
)
from datagateway_api.common.datagateway_api.icat.filters import PythonICATWhereFilter
from datagateway_api.common.exceptions import BadRequestError, FilterError


class TestICATWhereFilter:
    @pytest.mark.parametrize(
        "operation, value, expected_condition_value",
        [
            pytest.param("eq", 5, "= '5'", id="equal"),
            pytest.param("ne", 5, "!= 5", id="not equal"),
            pytest.param("like", 5, "like '%5%'", id="like"),
            pytest.param("nlike", 5, "not like '%5%'", id="not like"),
            pytest.param("lt", 5, "< '5'", id="less than"),
            pytest.param("lte", 5, "<= '5'", id="less than or equal"),
            pytest.param("gt", 5, "> '5'", id="greater than"),
            pytest.param("gte", 5, ">= '5'", id="greater than or equal"),
            pytest.param("in", [1, 2, 3, 4], "in (1, 2, 3, 4)", id="in a list"),
            pytest.param("in", [], "in (NULL)", id="empty list"),
        ],
    )
    def test_valid_operations(
        self, icat_query, operation, value, expected_condition_value,
    ):
        test_filter = PythonICATWhereFilter("id", value, operation)
        test_filter.apply_filter(icat_query)

        assert icat_query.conditions == {"id": expected_condition_value}

    def test_invalid_in_operation(self, icat_query):
        with pytest.raises(BadRequestError):
            PythonICATWhereFilter("id", "1, 2, 3, 4, 5", "in")

    def test_invalid_operation(self, icat_query):
        test_filter = PythonICATWhereFilter("id", 10, "non")

        with pytest.raises(FilterError):
            test_filter.apply_filter(icat_query)

    def test_valid_internal_icat_value(self, icat_query):
        """Check that values that point to other values in the schema are applied"""
        test_filter = PythonICATWhereFilter("startDate", "o.endDate", "lt")
        test_filter.apply_filter(icat_query)

        assert icat_query.conditions == {"startDate": "< o.endDate"}

    def test_valid_field(self, icat_query):
        test_filter = PythonICATWhereFilter("title", "Investigation Title", "eq")
        test_filter.apply_filter(icat_query)

        assert icat_query.conditions == {"title": "= 'Investigation Title'"}

    def test_invalid_field(self, icat_query):
        test_filter = PythonICATWhereFilter("random_field", "my_value", "eq")

        with pytest.raises(FilterError):
            test_filter.apply_filter(icat_query)

    def test_multiple_conditions_per_field(self, icat_query):
        lt_filter = PythonICATWhereFilter("id", 10, "lt")
        gt_filter = PythonICATWhereFilter("id", 5, "gt")

        filter_handler = FilterOrderHandler()
        filter_handler.add_filters([lt_filter, gt_filter])
        filter_handler.apply_filters(icat_query)

        assert icat_query.conditions == {"id": ["< '10'", "> '5'"]}
