import pytest

from datagateway_api.src.common.exceptions import FilterError
from datagateway_api.src.search_api.filters import (
    SearchAPIIncludeFilter,
    SearchAPILimitFilter,
    SearchAPISkipFilter,
    SearchAPIWhereFilter,
)
from datagateway_api.src.search_api.query_filter_factory import (
    SearchAPIQueryFilterFactory,
)


class TestSearchAPIQueryFilterFactory:
    @pytest.mark.parametrize(
        "test_request_filter, expected_length, expected_fields, expected_operations"
        ", expected_values, expected_boolean_operators",
        [
            pytest.param(
                {"filter": {"where": {"title": "My Title"}}},
                1,
                ["title"],
                ["eq"],
                ["My Title"],
                ["and"],
                id="Property value, no specified operator",
            ),
            pytest.param(
                {"filter": {"where": {"summary": {"like": "My Test Summary"}}}},
                1,
                ["summary"],
                ["like"],
                ["My Test Summary"],
                ["and"],
                id="Property value with operator",
            ),
            pytest.param(
                {"filter": {"where": {"and": [{"summary": "My Test Summary"}]}}},
                1,
                ["summary"],
                ["eq"],
                ["My Test Summary"],
                ["and"],
                id="AND with single condition, no specified operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {"summary": "My Test Summary"},
                                {"title": "Test title"},
                            ],
                        },
                    },
                },
                2,
                ["summary", "title"],
                ["eq", "eq"],
                ["My Test Summary", "Test title"],
                ["and", "and"],
                id="AND with multiple conditions, no specified operator",
            ),
            pytest.param(
                {"filter": {"where": {"and": [{"value": {"lt": 50}}]}}},
                1,
                ["value"],
                ["lt"],
                [50],
                ["and"],
                id="AND, single condition with operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {"name": {"like": "Test name"}},
                                {"value": {"gte": 275}},
                            ],
                        },
                    },
                },
                2,
                ["name", "value"],
                ["like", "gte"],
                ["Test name", 275],
                ["and", "and"],
                id="AND, multiple conditions with operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {
                                    "and": [
                                        {"name": {"like": "Test name"}},
                                        {"value": {"gte": 275}},
                                    ],
                                },
                            ],
                        },
                    },
                },
                2,
                ["name", "value"],
                ["like", "gte"],
                ["Test name", 275],
                ["and", "and"],
                id="Nested AND, multiple conditions with operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [
                                {"name": {"like": "Test name"}},
                                {"value": {"gte": 275}},
                            ],
                        },
                    },
                },
                2,
                ["name", "value"],
                ["like", "gte"],
                ["Test name", 275],
                ["or", "or"],
                id="OR, multiple conditions with operator",
            ),
        ],
    )
    def test_valid_where_filter(
        self,
        test_request_filter,
        expected_length,
        expected_fields,
        expected_operations,
        expected_values,
        expected_boolean_operators,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(test_request_filter)

        assert len(filters) == expected_length
        for test_filter, field, operation, value, boolean_operator in zip(
            filters,
            expected_fields,
            expected_operations,
            expected_values,
            expected_boolean_operators,
        ):
            assert isinstance(test_filter, SearchAPIWhereFilter)
            assert test_filter.field == field
            assert test_filter.operation == operation
            assert test_filter.value == value
            assert test_filter.boolean_operator == boolean_operator

    @pytest.mark.parametrize(
        "test_request_filter, expected_length, expected_included_entities, expected_where_filter_data",
        [
            pytest.param(
                {"filter": {"include": [{"relation": "files"}]}},
                1,
                [["files"]],
                [[]],
                id="Single related model",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [{"relation": "files"}, {"relation": "instrument"}],
                    },
                },
                2,
                [["files"], ["instrument"]],
                [[], []],
                id="Multiple related models",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "parameters",
                                "scope": {"where": {"name": "My parameter"}},
                            },
                        ],
                    },
                },
                2,
                [["parameters"], []],
                [[], ["parameters.name", "eq", "My parameter"]],
                id="Related model with scope",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "parameters",
                                "scope": {"where": {"name": {"ne": "My parameter"}}},
                            },
                        ],
                    },
                },
                2,
                [["parameters"], []],
                [[], ["parameters.name", "ne", "My parameter"]],
                id="Related model with scope (with operator)",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "parameters",
                                "scope": {"where": {"text": "My parameter"}},
                            },
                        ],
                    },
                },
                2,
                [["parameters"], []],
                [[], ["parameters.name", "ne", "My parameter"]],
                id="Related model with scope (text operator)",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "documents",
                                "scope": {
                                    "where": {
                                        "and": [
                                            {"summary": "My Test Summary"},
                                            {"title": "Test title"},
                                        ],
                                    },
                                },
                            },
                        ],
                    },
                },
                3,
                [["documents"], [], []],
                [
                    [],
                    ["documents.summary", "eq", "My Test Summary"],
                    ["documents.title", "eq", "Test title"],
                ],
                id="Related model with scope (boolean operator)",
            ),
        ],
    )
    def test_valid_include_filter(
        self,
        test_request_filter,
        expected_length,
        expected_included_entities,
        expected_where_filter_data,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(test_request_filter)

        assert len(filters) == expected_length

        for test_filter, included_entities, where_filter_data in zip(
            filters, expected_included_entities, expected_where_filter_data,
        ):
            if isinstance(test_filter, SearchAPIIncludeFilter):
                assert test_filter.included_filters == included_entities
            if isinstance(test_filter, SearchAPIWhereFilter):
                assert test_filter.field == where_filter_data[0]
                assert test_filter.operation == where_filter_data[1]
                assert test_filter.value == where_filter_data[2]
                # TODO - Assert for boolean_operator

    @pytest.mark.parametrize(
        "test_request_filter, expected_limit_value",
        [
            pytest.param({"filter": {"limit": 0}}, 0, id="Limit 0 values"),
            pytest.param({"filter": {"limit": 50}}, 50, id="Limit 50 values"),
        ],
    )
    def test_valid_limit_filter(self, test_request_filter, expected_limit_value):
        filters = SearchAPIQueryFilterFactory.get_query_filter(test_request_filter)

        assert len(filters) == 1
        assert isinstance(filters[0], SearchAPILimitFilter)
        assert filters[0].limit_value == expected_limit_value

    @pytest.mark.parametrize(
        "test_request_filter, expected_skip_value",
        [
            pytest.param({"filter": {"skip": 0}}, 0, id="Skip 0 values"),
            pytest.param({"filter": {"skip": 50}}, 50, id="Skip 50 values"),
        ],
    )
    def test_valid_skip_filter(
        self, test_request_filter, expected_skip_value,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(test_request_filter)

        assert len(filters) == 1
        assert isinstance(filters[0], SearchAPISkipFilter)
        assert filters[0].skip_value == expected_skip_value

    @pytest.mark.parametrize(
        "test_request_filter",
        [
            pytest.param("invalid query filter input", id="Generally invalid input"),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "parameters",
                                "scope": {"text": "My parameter"},
                            },
                        ],
                    },
                },
                id="Invalid scope syntax on include filter",
            ),
        ],
    )
    def test_invalid_filter_input(self, test_request_filter):
        with pytest.raises(FilterError):
            SearchAPIQueryFilterFactory.get_query_filter(test_request_filter)
