import pytest

from datagateway_api.src.search_api.filters import SearchAPIWhereFilter
from datagateway_api.src.search_api.nested_where_filters import NestedWhereFilters
from datagateway_api.src.search_api.query import SearchAPIQuery


class TestNestedWhereFilters:
    @pytest.mark.parametrize(
        "lhs, rhs, joining_operator, expected_where_clause",
        [
            pytest.param("A", None, "AND", "(A)", id="LHS (A) w/ misc. AND"),
            pytest.param("A", None, "OR", "(A)", id="LHS (A) w/ misc. OR"),
            pytest.param([], "A", "AND", "(A)", id="RHS (A) w/ misc. AND"),
            pytest.param([], "A", "OR", "(A)", id="RHS (A) w/ misc. OR"),
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
        "lhs, rhs, joining_operator, query, expected_where_clause",
        [
            pytest.param(
                SearchAPIWhereFilter("name", "test name", "eq"),
                SearchAPIWhereFilter("id", 3, "eq"),
                "OR",
                SearchAPIQuery("File"),
                "(o.name = 'test name' OR o.id = '3')",
                id="(o.title = 'test name' OR o.id = '3')",
            ),
            pytest.param(
                [SearchAPIWhereFilter("name", "test name", "eq")],
                SearchAPIWhereFilter("id", 3, "eq"),
                "OR",
                SearchAPIQuery("File"),
                "(o.name = 'test name' OR o.id = '3')",
                id="Single filter list in LHS",
            ),
            pytest.param(
                [SearchAPIWhereFilter("name", "test name", "eq")],
                [SearchAPIWhereFilter("id", 3, "eq")],
                "OR",
                SearchAPIQuery("File"),
                "(o.name = 'test name' OR o.id = '3')",
                id="Single filter list in LHS and RHS",
            ),
            pytest.param(
                [
                    SearchAPIWhereFilter("name", "test name", "eq"),
                    SearchAPIWhereFilter("id", 10, "lt"),
                ],
                [SearchAPIWhereFilter("id", 3, "gt")],
                "AND",
                SearchAPIQuery("File"),
                "(o.name = 'test name' AND o.id < '10' AND o.id > '3')",
                id="Multiple filters on LHS",
            ),
            pytest.param(
                [
                    SearchAPIWhereFilter("title", "test name", "eq"),
                    SearchAPIWhereFilter("pid", 10, "lt"),
                ],
                [
                    SearchAPIWhereFilter("pid", 3, "gt"),
                    SearchAPIWhereFilter("summary", "Test Summary", "like"),
                ],
                "AND",
                SearchAPIQuery("Document"),
                "(o.name = 'test name' AND o.doi < '10' AND o.doi > '3' AND o.summary"
                " like '%Test Summary%')",
                id="Multiple filters on LHS and RHS",
            ),
        ],
    )
    def test_search_api_filters(
        self, lhs, rhs, joining_operator, query, expected_where_clause,
    ):
        # TODO - Is creating clients causing this to be slow? Test once session handler
        # work merged
        test_nest = NestedWhereFilters(lhs, rhs, joining_operator, query)
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
