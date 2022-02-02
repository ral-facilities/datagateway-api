import pytest

from datagateway_api.src.common.exceptions import BadRequestError, FilterError
from datagateway_api.src.common.filter_order_handler import FilterOrderHandler
from datagateway_api.src.datagateway_api.icat.filters import PythonICATWhereFilter


class TestICATWhereFilter:
    @pytest.mark.parametrize(
        "operation, value, expected_condition_value",
        [
            pytest.param("eq", 5, ["%s = '5'"], id="equal"),
            pytest.param("ne", 5, ["%s != '5'"], id="not equal (ne)"),
            pytest.param("neq", 5, ["%s != '5'"], id="not equal (neq)"),
            pytest.param("like", 5, ["%s like '%%5%%'"], id="like"),
            pytest.param("ilike", 5, ["UPPER(%s) like UPPER('%%5%%')"], id="ilike"),
            pytest.param("nlike", 5, ["%s not like '%%5%%'"], id="not like"),
            pytest.param(
                "nilike", 5, ["UPPER(%s) not like UPPER('%%5%%')"], id="not ilike",
            ),
            pytest.param("lt", 5, ["%s < '5'"], id="less than"),
            pytest.param("lte", 5, ["%s <= '5'"], id="less than or equal"),
            pytest.param("gt", 5, ["%s > '5'"], id="greater than"),
            pytest.param("gte", 5, ["%s >= '5'"], id="greater than or equal"),
            pytest.param(
                "in", [1, 2, 3, 4], ["%s in (1, 2, 3, 4)"], id="in a list (in)",
            ),
            pytest.param("in", [], ["%s in (NULL)"], id="in empty list (in)"),
            pytest.param(
                "inq", [1, 2, 3, 4], ["%s in (1, 2, 3, 4)"], id="in a list (inq)",
            ),
            pytest.param("inq", [], ["%s in (NULL)"], id="in empty list (inq)"),
            pytest.param(
                "nin", [1, 2, 3, 4], ["%s not in (1, 2, 3, 4)"], id="not in a list",
            ),
            pytest.param("nin", [], ["%s not in (NULL)"], id="not in empty list"),
            pytest.param("between", [1, 2], ["%s between '1' and '2'"], id="between"),
            pytest.param("regexp", "^Test", ["%s regexp '^Test'"], id="regexp"),
        ],
    )
    def test_valid_operations(
        self, icat_query, operation, value, expected_condition_value,
    ):
        test_filter = PythonICATWhereFilter("id", value, operation)
        test_filter.apply_filter(icat_query)

        assert icat_query.conditions == {"id": expected_condition_value}

    @pytest.mark.parametrize(
        "operation, value",
        [
            pytest.param("in", "1, 2, 3, 4, 5", id="in a list (in)"),
            pytest.param("inq", "1, 2, 3, 4, 5", id="in a list (inq)"),
            pytest.param("nin", "1, 2, 3, 4, 5", id="nin"),
            pytest.param("between", "1, 2, 3, 4, 5", id="between - string value"),
            pytest.param("between", [], id="between - empty list"),
            pytest.param(
                "between", [1], id="between - list with less than two elements",
            ),
            pytest.param(
                "between", [1, 2, 3], id="between - list with more than two elements",
            ),
        ],
    )
    def test_invalid_operations_raise_bad_request_error(self, operation, value):
        with pytest.raises(BadRequestError):
            PythonICATWhereFilter("id", value, operation)

    def test_invalid_operation(self, icat_query):
        test_filter = PythonICATWhereFilter("id", 10, "non")

        with pytest.raises(FilterError):
            test_filter.apply_filter(icat_query)

    def test_valid_internal_icat_value(self, icat_query):
        """Check that values that point to other values in the schema are applied"""
        test_filter = PythonICATWhereFilter("startDate", "o.endDate", "lt")
        test_filter.apply_filter(icat_query)

        assert icat_query.conditions == {"startDate": ["%s < o.endDate"]}

    def test_valid_field(self, icat_query):
        test_filter = PythonICATWhereFilter("title", "Investigation Title", "eq")
        test_filter.apply_filter(icat_query)

        assert icat_query.conditions == {"title": ["%s = 'Investigation Title'"]}

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

        assert icat_query.conditions == {"id": ["%s < '10'", "%s > '5'"]}
