import pytest

from datagateway_api.src.search_api.filters import SearchAPIWhereFilter
from datagateway_api.src.search_api.nested_where_filters import NestedWhereFilters


class TestNestedWhereFilters:
    @pytest.mark.parametrize(
        "lhs, rhs, joining_operator, expected_where_clause",
        [
            pytest.param("A", None, "AND", "(A)", id="(A) w/ misc. AND"),
            pytest.param("A", None, "OR", "(A)", id="(A) w/ misc. OR"),
            pytest.param("A", "B", "AND", "(A AND B)", id="(A AND B)"),
            pytest.param("A", "B", "OR", "(A OR B)", id="(A OR B)"),
            pytest.param(
                "(A AND B)",
                "(C AND D)",
                "AND",
                "((A AND B) AND (C AND D))",
                id="((A AND B) AND (C AND D))",
            ),
            pytest.param(
                "(A AND B)",
                "(C AND D)",
                "OR",
                "((A AND B) OR (C AND D))",
                id="((A AND B) OR (C AND D))",
            ),
            pytest.param(
                "(A OR B)",
                "(C OR D)",
                "OR",
                "((A OR B) OR (C OR D))",
                id="((A OR B) OR (C OR D))",
            ),
            pytest.param(
                "(A OR B)",
                "(C OR D)",
                "AND",
                "((A OR B) AND (C OR D))",
                id="((A OR B) AND (C OR D))",
            ),
            pytest.param(
                "(A AND B AND C) OR (C AND D)",
                "(E AND F)",
                "OR",
                "((A AND B AND C) OR (C AND D) OR (E AND F))",
                id="((A AND B AND C) OR (C AND D) OR (E AND F))",
            ),
            pytest.param(
                "(A AND B AND C) AND (C OR D)",
                "(E AND F)",
                "OR",
                "((A AND B AND C) AND (C OR D) OR (E AND F))",
                id="((A AND B AND C) AND (C OR D)) OR (E AND F))",
            ),
            pytest.param(
                "((A AND B AND C) AND (C OR D))",
                "(E AND F)",
                "OR",
                "(((A AND B AND C) AND (C OR D)) OR (E AND F))",
                id="(((A AND B AND C) AND (C OR D))) OR (E AND F))",
            ),
        ],
    )
    def test_str_filters(self, lhs, rhs, joining_operator, expected_where_clause):
        test_nest = NestedWhereFilters(lhs, rhs, joining_operator)

        where_clause = str(test_nest)

        assert where_clause == expected_where_clause

    @pytest.mark.parametrize(
        "lhs, rhs, joining_operator, expected_where_clause",
        [
            pytest.param(
                SearchAPIWhereFilter("name", "test name", "eq", "and"),
                SearchAPIWhereFilter("id", 3, "eq", "and"),
                "OR",
                "(o.name = 'test name' OR o.id = '3')",
                id="(o.name = 'test name' OR o.id = '3')",
            ),
        ],
    )
    def test_search_api_filters(
        self, lhs, rhs, joining_operator, expected_where_clause,
    ):
        test_nest = NestedWhereFilters(lhs, rhs, joining_operator)
        where_clause = str(test_nest)
        assert where_clause == expected_where_clause

    @pytest.mark.parametrize(
        "lhs, rhs, joining_operator, expected_where_clause",
        [
            pytest.param(
                NestedWhereFilters("A", "B", "OR"),
                NestedWhereFilters("C", "D", "AND"),
                "OR",
                "((A OR B) OR (C AND D))",
                id="((A OR B) OR (C AND D))",
            ),
        ],
    )
    def test_nested_classes(
        self, lhs, rhs, joining_operator, expected_where_clause,
    ):
        test_nest = NestedWhereFilters(lhs, rhs, joining_operator)
        where_clause = str(test_nest)
        assert where_clause == expected_where_clause
