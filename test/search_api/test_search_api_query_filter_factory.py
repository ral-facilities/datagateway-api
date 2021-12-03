import pytest

from datagateway_api.src.common.exceptions import FilterError
from datagateway_api.src.search_api.filters import (
    SearchAPIIncludeFilter,
    SearchAPILimitFilter,
    SearchAPISkipFilter,
    SearchAPIWhereFilter,
)
from datagateway_api.src.search_api.nested_where_filters import NestedWhereFilters
from datagateway_api.src.search_api.query_filter_factory import (
    SearchAPIQueryFilterFactory,
)


class TestSearchAPIQueryFilterFactory:
    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_length, expected_fields,"
        "expected_operations, expected_values, expected_boolean_operators",
        [
            pytest.param(
                {"filter": {"where": {"title": "My Title"}}},
                "documents",
                1,
                ["title"],
                ["eq"],
                ["My Title"],
                ["and"],
                id="Property value with no operator",
            ),
            pytest.param(
                {"filter": {"where": {"summary": {"like": "My Test Summary"}}}},
                "documents",
                1,
                ["summary"],
                ["like"],
                ["My Test Summary"],
                ["and"],
                id="Property value with operator",
            ),
            pytest.param(
                {"where": {"summary": {"like": "My Test Summary"}}},
                "documents",
                1,
                ["summary"],
                ["like"],
                ["My Test Summary"],
                ["and"],
                id="WHERE filter in syntax for count endpoints",
            ),
        ],
    )
    def test_valid_where_filter(
        self,
        test_request_filter,
        test_entity_name,
        expected_length,
        expected_fields,
        expected_operations,
        expected_values,
        expected_boolean_operators,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

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
        "test_request_filter, test_entity_name, expected_length, expected_lhs"
        ", expected_rhs, expected_joining_operator",
        [
            pytest.param(
                {"filter": {"where": {"text": "Dataset 1"}}},
                "datasets",
                1,
                [],
                [SearchAPIWhereFilter("title", "Dataset 1", "eq")],
                "or",
                id="Text operator on dataset",
            ),
            pytest.param(
                {"filter": {"where": {"text": "Instrument 1"}}},
                "instrument",
                1,
                [SearchAPIWhereFilter("name", "Instrument 1", "eq")],
                [SearchAPIWhereFilter("facility", "Instrument 1", "eq")],
                "or",
                id="Text operator on instrument",
            ),
        ],
    )
    def test_valid_where_filter_text_operator(
        self,
        test_request_filter,
        test_entity_name,
        expected_length,
        expected_lhs,
        expected_rhs,
        expected_joining_operator,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        # TODO - Will expected length always be 1?
        assert len(filters) == expected_length
        assert isinstance(filters[0], NestedWhereFilters)
        print(type(filters[0]))
        print(f"LHS: {repr(filters[0].lhs)}, Type: {type(filters[0].lhs)}")
        print(f"RHS: {repr(filters[0].rhs)}, Type: {type(filters[0].rhs)}")
        assert repr(filters[0].lhs) == repr(expected_lhs)
        assert repr(filters[0].rhs) == repr(expected_rhs)
        assert filters[0].joining_operator == expected_joining_operator

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_length, expected_fields,"
        "expected_operations, expected_values, expected_boolean_operators"
        ", expected_lhs, expected_rhs, expected_joining_operator",
        [
            pytest.param(
                {"filter": {"where": {"and": [{"summary": "My Test Summary"}]}}},
                "documents",
                1,
                ["summary"],
                ["eq"],
                ["My Test Summary"],
                ["and"],
                [],
                [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                "and",
                id="Single condition, property value with no operator",
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
                "documents",
                1,
                ["summary", "title"],
                ["eq", "eq"],
                ["My Test Summary", "Test title"],
                ["and", "and"],
                [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                [SearchAPIWhereFilter("title", "Test title", "eq")],
                "and",
                id="Multiple conditions (two), property values with no operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {"summary": "My Test Summary"},
                                {"title": "Test title"},
                                {"type": "Test type"},
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "type"],
                ["eq", "eq", "eq"],
                ["My Test Summary", "Test title", "Test type"],
                ["and", "and", "and"],
                [
                    SearchAPIWhereFilter("summary", "My Test Summary", "eq"),
                    SearchAPIWhereFilter("title", "Test title", "eq"),
                ],
                [SearchAPIWhereFilter("type", "Test type", "eq")],
                "and",
                id="Multiple conditions (three), property values with no operator",
            ),
            pytest.param(
                {"filter": {"where": {"and": [{"value": {"lt": 50}}]}}},
                "parameters",
                1,
                ["value"],
                ["lt"],
                [50],
                ["and"],
                [],
                [SearchAPIWhereFilter("value", 50, "lt")],
                "and",
                id="Single condition, property value with operator",
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
                "parameters",
                1,
                ["name", "value"],
                ["like", "gte"],
                ["Test name", 275],
                ["and", "and"],
                [SearchAPIWhereFilter("name", "Test name", "like")],
                [SearchAPIWhereFilter("value", 275, "gte")],
                "and",
                id="Multiple conditions (two), property values with operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {"name": {"like": "Test name"}},
                                {"value": {"gte": 275}},
                                {"unit": {"nlike": "Test unit"}},
                            ],
                        },
                    },
                },
                "parameters",
                1,
                ["name", "value", "unit"],
                ["like", "gte", "nlike"],
                ["Test name", 275, "Test unit"],
                ["and", "and", "and"],
                [
                    SearchAPIWhereFilter("name", "Test name", "like"),
                    SearchAPIWhereFilter("value", 275, "gte"),
                ],
                [SearchAPIWhereFilter("unit", "Test unit", "nlike")],
                "and",
                id="Multiple conditions (three), property values with operator",
            ),
            pytest.param(
                {"filter": {"where": {"and": [{"text": "Dataset 1"}]}}},
                "datasets",
                1,
                ["title"],
                ["eq"],
                ["Dataset 1"],
                ["or"],
                [],
                [
                    NestedWhereFilters(
                        [], SearchAPIWhereFilter("title", "Dataset 1", "eq"), "or",
                    ),
                ],
                "and",
                id="Single condition, text operator on dataset",
            ),
            pytest.param(
                {"filter": {"where": {"and": [{"text": "Instrument 1"}]}}},
                "instrument",
                1,
                ["name", "facility"],
                ["eq", "eq"],
                ["Instrument 1", "Instrument 1"],
                ["or", "or"],
                [],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("name", "Instrument 1", "eq")],
                        [SearchAPIWhereFilter("facility", "Instrument 1", "eq")],
                        "or",
                    ),
                ],
                "and",
                id="Single condition, text operator on instrument",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {"and": [{"text": "Dataset 1"}, {"pid": "Test pid"}]},
                    },
                },
                "datasets",
                1,
                ["title", "pid"],
                ["eq", "eq"],
                ["Dataset 1", "Test pid"],
                ["or", "and"],
                [
                    NestedWhereFilters(
                        [], [SearchAPIWhereFilter("title", "Dataset 1", "eq")], "or",
                    ),
                ],
                [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                "and",
                id="Multiple conditions (two), text operator on dataset and "
                "property value with no operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [{"text": "Instrument 1"}, {"pid": "Test pid"}],
                        },
                    },
                },
                "instrument",
                1,
                ["name", "facility", "pid"],
                ["eq", "eq", "eq"],
                ["Instrument 1", "Instrument 1", "Test pid"],
                ["or", "or", "and"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("name", "Instrument 1", "eq")],
                        [SearchAPIWhereFilter("facility", "Instrument 1", "eq")],
                        "or",
                    ),
                ],
                [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                "and",
                id="Multiple conditions (two), text operator on instrument and "
                "property value with no operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {"text": "Dataset 1"},
                                {"pid": {"eq": "Test pid"}},
                            ],
                        },
                    },
                },
                "datasets",
                1,
                ["title", "pid"],
                ["eq", "eq"],
                ["Dataset 1", "Test pid"],
                ["or", "and"],
                [
                    NestedWhereFilters(
                        [], [SearchAPIWhereFilter("title", "Dataset 1", "eq")], "or",
                    ),
                ],
                [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                "and",
                id="Multiple conditions (two), text operator on dataset and "
                "property value with operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {"text": "Instrument 1"},
                                {"pid": {"eq": "Test pid"}},
                            ],
                        },
                    },
                },
                "instrument",
                1,
                ["name", "facility", "pid"],
                ["eq", "eq", "eq"],
                ["Instrument 1", "Instrument 1", "Test pid"],
                ["or", "or", "and"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("name", "Instrument 1", "eq")],
                        [SearchAPIWhereFilter("facility", "Instrument 1", "eq")],
                        "or",
                    ),
                ],
                [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                "and",
                id="Multiple conditions (two), text operator on instrument and "
                "property value with operator",
            ),
        ],
    )
    def test_valid_where_filter_with_and_boolean_operator(
        self,
        test_request_filter,
        test_entity_name,
        expected_length,
        expected_fields,
        expected_operations,
        expected_values,
        expected_boolean_operators,
        expected_lhs,
        expected_rhs,
        expected_joining_operator,
    ):
        # TODO - Could test_entity_name just be hardcoded to the same entity?
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        # TODO - Will expected length always be 1?
        assert len(filters) == expected_length
        assert isinstance(filters[0], NestedWhereFilters)
        print(type(filters[0]))
        print(f"LHS: {repr(filters[0].lhs)}, Type: {type(filters[0].lhs)}")
        print(f"RHS: {repr(filters[0].rhs)}, Type: {type(filters[0].rhs)}")
        assert repr(filters[0].lhs) == repr(expected_lhs)
        assert repr(filters[0].rhs) == repr(expected_rhs)
        assert filters[0].joining_operator == expected_joining_operator

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_length, expected_fields,"
        "expected_operations, expected_values, expected_boolean_operators"
        ", expected_lhs, expected_rhs, expected_joining_operator",
        [
            pytest.param(
                {"filter": {"where": {"or": [{"summary": "My Test Summary"}]}}},
                "documents",
                1,
                ["summary"],
                ["eq"],
                ["My Test Summary"],
                ["or"],
                [],
                [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                "or",
                id="Single condition, property value with no operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [
                                {"summary": "My Test Summary"},
                                {"title": "Test title"},
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title"],
                ["eq", "eq"],
                ["My Test Summary", "Test title"],
                ["or", "or"],
                [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                [SearchAPIWhereFilter("title", "Test title", "eq")],
                "or",
                id="Multiple conditions (two), property values with no operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [
                                {"summary": "My Test Summary"},
                                {"title": "Test title"},
                                {"type": "Test type"},
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "type"],
                ["eq", "eq", "eq"],
                ["My Test Summary", "Test title", "Test type"],
                ["or", "or", "or"],
                [
                    SearchAPIWhereFilter("summary", "My Test Summary", "eq"),
                    SearchAPIWhereFilter("title", "Test title", "eq"),
                ],
                [SearchAPIWhereFilter("type", "Test type", "eq")],
                "or",
                id="Multiple conditions (three), property values with no operator",
            ),
            pytest.param(
                {"filter": {"where": {"or": [{"value": {"lt": 50}}]}}},
                "parameters",
                1,
                ["value"],
                ["lt"],
                [50],
                ["or"],
                [],
                [SearchAPIWhereFilter("value", 50, "lt")],
                "or",
                id="Single condition, property value with operator",
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
                "parameters",
                1,
                ["name", "value"],
                ["like", "gte"],
                ["Test name", 275],
                ["or", "or"],
                [SearchAPIWhereFilter("name", "Test name", "like")],
                [SearchAPIWhereFilter("value", 275, "gte")],
                "or",
                id="Multiple conditions (two), property values with operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [
                                {"name": {"like": "Test name"}},
                                {"value": {"gte": 275}},
                                {"unit": {"nlike": "Test unit"}},
                            ],
                        },
                    },
                },
                "parameters",
                1,
                ["name", "value", "unit"],
                ["like", "gte", "nlike"],
                ["Test name", 275, "Test unit"],
                ["or", "or", "or"],
                [
                    SearchAPIWhereFilter("name", "Test name", "like"),
                    SearchAPIWhereFilter("value", 275, "gte"),
                ],
                [SearchAPIWhereFilter("unit", "Test unit", "nlike")],
                "or",
                id="Multiple conditions (three), property values with operator",
            ),
            pytest.param(
                {"filter": {"where": {"or": [{"text": "Dataset 1"}]}}},
                "datasets",
                1,
                ["title"],
                ["eq"],
                ["Dataset 1"],
                ["or"],
                [],
                [
                    NestedWhereFilters(
                        [], SearchAPIWhereFilter("title", "Dataset 1", "eq"), "or",
                    ),
                ],
                "or",
                id="Single condition, text operator on dataset",
            ),
            pytest.param(
                {"filter": {"where": {"or": [{"text": "Instrument 1"}]}}},
                "instrument",
                1,
                ["name", "facility"],
                ["eq", "eq"],
                ["Instrument 1", "Instrument 1"],
                ["or", "or"],
                [],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("name", "Instrument 1", "eq")],
                        [SearchAPIWhereFilter("facility", "Instrument 1", "eq")],
                        "or",
                    ),
                ],
                "or",
                id="Single condition, text operator on instrument",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {"or": [{"text": "Dataset 1"}, {"pid": "Test pid"}]},
                    },
                },
                "datasets",
                1,
                ["title", "pid"],
                ["eq", "eq"],
                ["Dataset 1", "Test pid"],
                ["or", "or"],
                [
                    NestedWhereFilters(
                        [], [SearchAPIWhereFilter("title", "Dataset 1", "eq")], "or",
                    ),
                ],
                [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                "or",
                id="Multiple conditions (two), text operator on dataset and "
                "property value with no operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [{"text": "Instrument 1"}, {"pid": "Test pid"}],
                        },
                    },
                },
                "instrument",
                1,
                ["name", "facility", "pid"],
                ["eq", "eq", "eq"],
                ["Instrument 1", "Instrument 1", "Test pid"],
                ["or", "or", "or"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("name", "Instrument 1", "eq")],
                        [SearchAPIWhereFilter("facility", "Instrument 1", "eq")],
                        "or",
                    ),
                ],
                [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                "or",
                id="Multiple conditions (two), text operator on instrument and "
                "property value with no operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [{"text": "Dataset 1"}, {"pid": {"eq": "Test pid"}}],
                        },
                    },
                },
                "datasets",
                1,
                ["title", "pid"],
                ["eq", "eq"],
                ["Dataset 1", "Test pid"],
                ["or", "or"],
                [
                    NestedWhereFilters(
                        [], [SearchAPIWhereFilter("title", "Dataset 1", "eq")], "or",
                    ),
                ],
                [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                "or",
                id="Multiple conditions (two), text operator on dataset and "
                "property value with operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [
                                {"text": "Instrument 1"},
                                {"pid": {"eq": "Test pid"}},
                            ],
                        },
                    },
                },
                "instrument",
                1,
                ["name", "facility", "pid"],
                ["eq", "eq", "eq"],
                ["Instrument 1", "Instrument 1", "Test pid"],
                ["or", "or", "or"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("name", "Instrument 1", "eq")],
                        [SearchAPIWhereFilter("facility", "Instrument 1", "eq")],
                        "or",
                    ),
                ],
                [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                "or",
                id="Multiple conditions (two), text operator on instrument and "
                "property value with operator",
            ),
        ],
    )
    def test_valid_where_filter_with_or_boolean_operator(
        self,
        test_request_filter,
        test_entity_name,
        expected_length,
        expected_fields,
        expected_operations,
        expected_values,
        expected_boolean_operators,
        expected_lhs,
        expected_rhs,
        expected_joining_operator,
    ):
        # TODO - Could test_entity_name just be hardcoded to the same entity?
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        # TODO - Will expected length always be 1?
        assert len(filters) == expected_length
        assert isinstance(filters[0], NestedWhereFilters)
        print(type(filters[0]))
        print(f"LHS: {repr(filters[0].lhs)}, Type: {type(filters[0].lhs)}")
        print(f"RHS: {repr(filters[0].rhs)}, Type: {type(filters[0].rhs)}")
        assert repr(filters[0].lhs) == repr(expected_lhs)
        assert repr(filters[0].rhs) == repr(expected_rhs)
        assert filters[0].joining_operator == expected_joining_operator

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_length, expected_fields,"
        "expected_operations, expected_values, expected_boolean_operators"
        ", expected_lhs, expected_rhs, expected_joining_operator",
        [
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {
                                    "and": [
                                        {"summary": "My Test Summary"},
                                        {"title": {"like": "Test title"}},
                                    ],
                                },
                                {
                                    "and": [
                                        {"pid": "Test pid"},
                                        {"type": {"eq": "Test type"}},
                                    ],
                                },
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "pid", "type"],
                ["eq", "like", "eq", "eq"],
                ["My Test Summary", "Test title", "Test pid", "Test type"],
                ["and", "and", "and", "and"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                        [SearchAPIWhereFilter("title", "Test title", "like")],
                        "and",
                    ),
                ],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                        [SearchAPIWhereFilter("type", "Test type", "eq")],
                        "and",
                    ),
                ],
                "and",
                id="With two AND boolean operators",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {
                                    "and": [
                                        {"summary": "My Test Summary"},
                                        {"title": {"like": "Test title"}},
                                    ],
                                },
                                {
                                    "or": [
                                        {"pid": "Test pid"},
                                        {"type": {"eq": "Test type"}},
                                    ],
                                },
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "pid", "type"],
                ["eq", "like", "eq", "eq"],
                ["My Test Summary", "Test title", "Test pid", "Test type"],
                ["and", "and", "or", "or"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                        [SearchAPIWhereFilter("title", "Test title", "like")],
                        "and",
                    ),
                ],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                        [SearchAPIWhereFilter("type", "Test type", "eq")],
                        "or",
                    ),
                ],
                "and",
                id="With AND and OR boolean operators",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {
                                    "or": [
                                        {"summary": "My Test Summary"},
                                        {"title": {"like": "Test title"}},
                                    ],
                                },
                                {
                                    "or": [
                                        {"pid": "Test pid"},
                                        {"type": {"eq": "Test type"}},
                                    ],
                                },
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "pid", "type"],
                ["eq", "like", "eq", "eq"],
                ["My Test Summary", "Test title", "Test pid", "Test type"],
                ["or", "or", "or", "or"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                        [SearchAPIWhereFilter("title", "Test title", "like")],
                        "or",
                    ),
                ],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                        [SearchAPIWhereFilter("type", "Test type", "eq")],
                        "or",
                    ),
                ],
                "and",
                id="With two OR boolean operators",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {
                                    "and": [
                                        {"summary": "My Test Summary"},
                                        {"title": {"like": "Test title"}},
                                    ],
                                },
                                {
                                    "and": [
                                        {"pid": "Test pid"},
                                        {"type": {"eq": "Test type"}},
                                    ],
                                },
                                {
                                    "and": [
                                        {"doi": "Test doi"},
                                        {"license": {"like": "Test license"}},
                                    ],
                                },
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "pid", "type", "doi", "license"],
                ["eq", "like", "eq", "eq", "eq", "like"],
                [
                    "My Test Summary",
                    "Test title",
                    "Test pid",
                    "Test type",
                    "Test doi",
                    "Test license",
                ],
                ["and", "and", "and", "and", "and", "and"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                        [SearchAPIWhereFilter("title", "Test title", "like")],
                        "and",
                    ),
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                        [SearchAPIWhereFilter("type", "Test type", "eq")],
                        "and",
                    ),
                ],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("doi", "Test doi", "eq")],
                        [SearchAPIWhereFilter("license", "Test license", "like")],
                        "and",
                    ),
                ],
                "and",
                id="With three AND boolean operators",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {
                                    "and": [
                                        {"summary": "My Test Summary"},
                                        {"title": {"like": "Test title"}},
                                    ],
                                },
                                {
                                    "and": [
                                        {"pid": "Test pid"},
                                        {"type": {"eq": "Test type"}},
                                    ],
                                },
                                {
                                    "or": [
                                        {"doi": "Test doi"},
                                        {"license": {"like": "Test license"}},
                                    ],
                                },
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "pid", "type", "doi", "license"],
                ["eq", "like", "eq", "eq", "eq", "like"],
                [
                    "My Test Summary",
                    "Test title",
                    "Test pid",
                    "Test type",
                    "Test doi",
                    "Test license",
                ],
                ["and", "and", "and", "and", "or", "or"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                        [SearchAPIWhereFilter("title", "Test title", "like")],
                        "and",
                    ),
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                        [SearchAPIWhereFilter("type", "Test type", "eq")],
                        "and",
                    ),
                ],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("doi", "Test doi", "eq")],
                        [SearchAPIWhereFilter("license", "Test license", "like")],
                        "or",
                    ),
                ],
                "and",
                id="With two AND and one OR boolean operators",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {
                                    "and": [
                                        {"summary": "My Test Summary"},
                                        {"title": {"like": "Test title"}},
                                    ],
                                },
                                {
                                    "or": [
                                        {"pid": "Test pid"},
                                        {"type": {"eq": "Test type"}},
                                    ],
                                },
                                {
                                    "or": [
                                        {"doi": "Test doi"},
                                        {"license": {"like": "Test license"}},
                                    ],
                                },
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "pid", "type", "doi", "license"],
                ["eq", "like", "eq", "eq", "eq", "like"],
                [
                    "My Test Summary",
                    "Test title",
                    "Test pid",
                    "Test type",
                    "Test doi",
                    "Test license",
                ],
                ["and", "and", "or", "or", "or", "or"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                        [SearchAPIWhereFilter("title", "Test title", "like")],
                        "and",
                    ),
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                        [SearchAPIWhereFilter("type", "Test type", "eq")],
                        "or",
                    ),
                ],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("doi", "Test doi", "eq")],
                        [SearchAPIWhereFilter("license", "Test license", "like")],
                        "or",
                    ),
                ],
                "and",
                id="With one AND and two OR boolean operators",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {
                                    "or": [
                                        {"summary": "My Test Summary"},
                                        {"title": {"like": "Test title"}},
                                    ],
                                },
                                {
                                    "or": [
                                        {"pid": "Test pid"},
                                        {"type": {"eq": "Test type"}},
                                    ],
                                },
                                {
                                    "or": [
                                        {"doi": "Test doi"},
                                        {"license": {"like": "Test license"}},
                                    ],
                                },
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "pid", "type", "doi", "license"],
                ["eq", "like", "eq", "eq", "eq", "like"],
                [
                    "My Test Summary",
                    "Test title",
                    "Test pid",
                    "Test type",
                    "Test doi",
                    "Test license",
                ],
                ["or", "or", "or", "or", "or", "or"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                        [SearchAPIWhereFilter("title", "Test title", "like")],
                        "or",
                    ),
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                        [SearchAPIWhereFilter("type", "Test type", "eq")],
                        "or",
                    ),
                ],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("doi", "Test doi", "eq")],
                        [SearchAPIWhereFilter("license", "Test license", "like")],
                        "or",
                    ),
                ],
                "and",
                id="With three OR boolean operators",
            ),
        ],
    )
    def test_valid_where_filter_with_nested_and_boolean_operator(
        self,
        test_request_filter,
        test_entity_name,
        expected_length,
        expected_fields,
        expected_operations,
        expected_values,
        expected_boolean_operators,
        expected_lhs,
        expected_rhs,
        expected_joining_operator,
    ):
        # TODO - Could test_entity_name just be hardcoded to the same entity?
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        # TODO - Will expected length always be 1?
        assert len(filters) == expected_length
        assert isinstance(filters[0], NestedWhereFilters)
        print(type(filters[0]))
        print(f"LHS: {repr(filters[0].lhs)}, Type: {type(filters[0].lhs)}")
        print(f"RHS: {repr(filters[0].rhs)}, Type: {type(filters[0].rhs)}")
        assert repr(filters[0].lhs) == repr(expected_lhs)
        assert repr(filters[0].rhs) == repr(expected_rhs)
        assert filters[0].joining_operator == expected_joining_operator

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_length, expected_fields,"
        "expected_operations, expected_values, expected_boolean_operators"
        ", expected_lhs, expected_rhs, expected_joining_operator",
        [
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [
                                {
                                    "and": [
                                        {"summary": "My Test Summary"},
                                        {"title": {"like": "Test title"}},
                                    ],
                                },
                                {
                                    "and": [
                                        {"pid": "Test pid"},
                                        {"type": {"eq": "Test type"}},
                                    ],
                                },
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "pid", "type"],
                ["eq", "like", "eq", "eq"],
                ["My Test Summary", "Test title", "Test pid", "Test type"],
                ["and", "and", "and", "and"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                        [SearchAPIWhereFilter("title", "Test title", "like")],
                        "and",
                    ),
                ],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                        [SearchAPIWhereFilter("type", "Test type", "eq")],
                        "and",
                    ),
                ],
                "or",
                id="With two AND boolean operators",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [
                                {
                                    "and": [
                                        {"summary": "My Test Summary"},
                                        {"title": {"like": "Test title"}},
                                    ],
                                },
                                {
                                    "or": [
                                        {"pid": "Test pid"},
                                        {"type": {"eq": "Test type"}},
                                    ],
                                },
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "pid", "type"],
                ["eq", "like", "eq", "eq"],
                ["My Test Summary", "Test title", "Test pid", "Test type"],
                ["and", "and", "or", "or"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                        [SearchAPIWhereFilter("title", "Test title", "like")],
                        "and",
                    ),
                ],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                        [SearchAPIWhereFilter("type", "Test type", "eq")],
                        "or",
                    ),
                ],
                "or",
                id="With AND and OR boolean operators",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [
                                {
                                    "or": [
                                        {"summary": "My Test Summary"},
                                        {"title": {"like": "Test title"}},
                                    ],
                                },
                                {
                                    "or": [
                                        {"pid": "Test pid"},
                                        {"type": {"eq": "Test type"}},
                                    ],
                                },
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "pid", "type"],
                ["eq", "like", "eq", "eq"],
                ["My Test Summary", "Test title", "Test pid", "Test type"],
                ["or", "or", "or", "or"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                        [SearchAPIWhereFilter("title", "Test title", "like")],
                        "or",
                    ),
                ],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                        [SearchAPIWhereFilter("type", "Test type", "eq")],
                        "or",
                    ),
                ],
                "or",
                id="With two OR boolean operators",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [
                                {
                                    "and": [
                                        {"summary": "My Test Summary"},
                                        {"title": {"like": "Test title"}},
                                    ],
                                },
                                {
                                    "and": [
                                        {"pid": "Test pid"},
                                        {"type": {"eq": "Test type"}},
                                    ],
                                },
                                {
                                    "and": [
                                        {"doi": "Test doi"},
                                        {"license": {"like": "Test license"}},
                                    ],
                                },
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "pid", "type", "doi", "license"],
                ["eq", "like", "eq", "eq", "eq", "like"],
                [
                    "My Test Summary",
                    "Test title",
                    "Test pid",
                    "Test type",
                    "Test doi",
                    "Test license",
                ],
                ["and", "and", "and", "and", "and", "and"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                        [SearchAPIWhereFilter("title", "Test title", "like")],
                        "and",
                    ),
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                        [SearchAPIWhereFilter("type", "Test type", "eq")],
                        "and",
                    ),
                ],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("doi", "Test doi", "eq")],
                        [SearchAPIWhereFilter("license", "Test license", "like")],
                        "and",
                    ),
                ],
                "or",
                id="With three AND boolean operators",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [
                                {
                                    "and": [
                                        {"summary": "My Test Summary"},
                                        {"title": {"like": "Test title"}},
                                    ],
                                },
                                {
                                    "and": [
                                        {"pid": "Test pid"},
                                        {"type": {"eq": "Test type"}},
                                    ],
                                },
                                {
                                    "or": [
                                        {"doi": "Test doi"},
                                        {"license": {"like": "Test license"}},
                                    ],
                                },
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "pid", "type", "doi", "license"],
                ["eq", "like", "eq", "eq", "eq", "like"],
                [
                    "My Test Summary",
                    "Test title",
                    "Test pid",
                    "Test type",
                    "Test doi",
                    "Test license",
                ],
                ["and", "and", "and", "and", "or", "or"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                        [SearchAPIWhereFilter("title", "Test title", "like")],
                        "and",
                    ),
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                        [SearchAPIWhereFilter("type", "Test type", "eq")],
                        "and",
                    ),
                ],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("doi", "Test doi", "eq")],
                        [SearchAPIWhereFilter("license", "Test license", "like")],
                        "or",
                    ),
                ],
                "or",
                id="With two AND and one OR boolean operators",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [
                                {
                                    "and": [
                                        {"summary": "My Test Summary"},
                                        {"title": {"like": "Test title"}},
                                    ],
                                },
                                {
                                    "or": [
                                        {"pid": "Test pid"},
                                        {"type": {"eq": "Test type"}},
                                    ],
                                },
                                {
                                    "or": [
                                        {"doi": "Test doi"},
                                        {"license": {"like": "Test license"}},
                                    ],
                                },
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "pid", "type", "doi", "license"],
                ["eq", "like", "eq", "eq", "eq", "like"],
                [
                    "My Test Summary",
                    "Test title",
                    "Test pid",
                    "Test type",
                    "Test doi",
                    "Test license",
                ],
                ["and", "and", "or", "or", "or", "or"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                        [SearchAPIWhereFilter("title", "Test title", "like")],
                        "and",
                    ),
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                        [SearchAPIWhereFilter("type", "Test type", "eq")],
                        "or",
                    ),
                ],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("doi", "Test doi", "eq")],
                        [SearchAPIWhereFilter("license", "Test license", "like")],
                        "or",
                    ),
                ],
                "or",
                id="With one AND and two OR boolean operators",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [
                                {
                                    "or": [
                                        {"summary": "My Test Summary"},
                                        {"title": {"like": "Test title"}},
                                    ],
                                },
                                {
                                    "or": [
                                        {"pid": "Test pid"},
                                        {"type": {"eq": "Test type"}},
                                    ],
                                },
                                {
                                    "or": [
                                        {"doi": "Test doi"},
                                        {"license": {"like": "Test license"}},
                                    ],
                                },
                            ],
                        },
                    },
                },
                "documents",
                1,
                ["summary", "title", "pid", "type", "doi", "license"],
                ["eq", "like", "eq", "eq", "eq", "like"],
                [
                    "My Test Summary",
                    "Test title",
                    "Test pid",
                    "Test type",
                    "Test doi",
                    "Test license",
                ],
                ["or", "or", "or", "or", "or", "or"],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                        [SearchAPIWhereFilter("title", "Test title", "like")],
                        "or",
                    ),
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("pid", "Test pid", "eq")],
                        [SearchAPIWhereFilter("type", "Test type", "eq")],
                        "or",
                    ),
                ],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("doi", "Test doi", "eq")],
                        [SearchAPIWhereFilter("license", "Test license", "like")],
                        "or",
                    ),
                ],
                "or",
                id="With three OR boolean operators",
            ),
        ],
    )
    def test_valid_where_filter_with_nested_or_boolean_operator(
        self,
        test_request_filter,
        test_entity_name,
        expected_length,
        expected_fields,
        expected_operations,
        expected_values,
        expected_boolean_operators,
        expected_lhs,
        expected_rhs,
        expected_joining_operator,
    ):
        # TODO - Could test_entity_name just be hardcoded to the same entity?
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        # TODO - Will expected length always be 1?
        assert len(filters) == expected_length
        assert isinstance(filters[0], NestedWhereFilters)
        print(type(filters[0]))
        print(f"LHS: {repr(filters[0].lhs)}, Type: {type(filters[0].lhs)}")
        print(f"RHS: {repr(filters[0].rhs)}, Type: {type(filters[0].rhs)}")
        assert repr(filters[0].lhs) == repr(expected_lhs)
        assert repr(filters[0].rhs) == repr(expected_rhs)
        assert filters[0].joining_operator == expected_joining_operator

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_length"
        ", expected_included_entities",
        [
            pytest.param(
                {"filter": {"include": [{"relation": "files"}]}},
                "datasets",
                1,
                [["files"]],
                id="Single related model",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [{"relation": "files"}, {"relation": "instrument"}],
                    },
                },
                "datasets",
                2,
                [["files"], ["instrument"]],
                id="Multiple related models",
            ),
        ],
    )
    def test_valid_include_filter(
        self,
        test_request_filter,
        test_entity_name,
        expected_length,
        expected_included_entities,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        assert len(filters) == expected_length

        for test_filter, included_entities in zip(filters, expected_included_entities):
            if isinstance(test_filter, SearchAPIIncludeFilter):
                assert test_filter.included_filters == included_entities

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_length"
        ", expected_included_entities, expected_where_filter_data",
        [
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
                "datasets",
                2,
                [["parameters"], []],
                [[], ["parameters.name", "eq", "My parameter", "and"]],
                id="Property value with no operator",
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
                "datasets",
                2,
                [["parameters"], []],
                [[], ["parameters.name", "ne", "My parameter", "and"]],
                id="Property value with operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "files",
                                "scope": {"where": {"text": "file1"}},
                            },
                        ],
                    },
                },
                "datasets",
                2,
                [["files"], []],
                [[], ["files.name", "eq", "file1", "or"]],
                id="Text operator on defined field mapping to single field",
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
                "datasets",
                1,
                [["parameters"], []],
                [[], []],
                id="Text operator on non-defined field",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "documents",
                                "scope": {"where": {"text": "document1"}},
                            },
                        ],
                    },
                },
                "datasets",
                3,
                [["documents"], []],
                [
                    [],
                    ["documents.title", "eq", "document1", "or"],
                    ["documents.summary", "eq", "document1", "or"],
                ],
                id="Text operator on defined field mapping to multiple field",
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
                "datasets",
                3,
                [["documents"], [], []],
                [
                    [],
                    ["documents.summary", "eq", "My Test Summary", "and"],
                    ["documents.title", "eq", "Test title", "and"],
                ],
                id="AND boolean operator",
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
                "datasets",
                3,
                [["documents"], [], []],
                [
                    [],
                    ["documents.summary", "eq", "My Test Summary", "and"],
                    ["documents.title", "eq", "Test title", "and"],
                ],
                id="OR boolean operator",
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
                                            {
                                                "and": [
                                                    {"summary": "My Test Summary"},
                                                    {"title": {"like": "Test title"}},
                                                ],
                                            },
                                            {
                                                "and": [
                                                    {"pid": "Test pid"},
                                                    {"type": {"eq": "Test type"}},
                                                ],
                                            },
                                            {
                                                "or": [
                                                    {"doi": "Test doi"},
                                                    {
                                                        "license": {
                                                            "like": "Test license",
                                                        },
                                                    },
                                                ],
                                            },
                                        ],
                                    },
                                },
                            },
                        ],
                    },
                },
                "datasets",
                7,
                [["documents"], [], [], [], [], [], []],
                [
                    [],
                    ["documents.summary", "eq", "My Test Summary", "and"],
                    ["documents.title", "like", "Test title", "and"],
                    ["documents.pid", "eq", "Test pid", "and"],
                    ["documents.type", "eq", "Test type", "and"],
                    ["documents.doi", "eq", "Test doi", "or"],
                    ["documents.license", "like", "Test license", "or"],
                ],
                id="Nested AND boolean operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "documents",
                                "scope": {
                                    "where": {
                                        "or": [
                                            {
                                                "and": [
                                                    {"summary": "My Test Summary"},
                                                    {"title": {"like": "Test title"}},
                                                ],
                                            },
                                            {
                                                "and": [
                                                    {"pid": "Test pid"},
                                                    {"type": {"eq": "Test type"}},
                                                ],
                                            },
                                            {
                                                "or": [
                                                    {"doi": "Test doi"},
                                                    {
                                                        "license": {
                                                            "like": "Test license",
                                                        },
                                                    },
                                                ],
                                            },
                                        ],
                                    },
                                },
                            },
                        ],
                    },
                },
                "datasets",
                7,
                [["documents"], [], [], [], [], [], []],
                [
                    [],
                    ["documents.summary", "eq", "My Test Summary", "and"],
                    ["documents.title", "like", "Test title", "and"],
                    ["documents.pid", "eq", "Test pid", "and"],
                    ["documents.type", "eq", "Test type", "and"],
                    ["documents.doi", "eq", "Test doi", "or"],
                    ["documents.license", "like", "Test license", "or"],
                ],
                id="Nested OR boolean operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "parameters",
                                "scope": {"where": {"name": "My parameter"}},
                            },
                            {
                                "relation": "documents",
                                "scope": {"where": {"title": "Document title"}},
                            },
                        ],
                    },
                },
                "datasets",
                4,
                [["parameters"], [], ["documents"], []],
                [
                    [],
                    ["parameters.name", "eq", "My parameter", "and"],
                    [],
                    ["documents.title", "eq", "Document title", "and"],
                ],
                id="Multiple related models",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "datasets",
                                "scope": {
                                    "where": {"title": "Dataset 1"},
                                    "include": [
                                        {
                                            "relation": "instrument",
                                            "scope": {
                                                "where": {"name": "Instrument 1"},
                                            },
                                        },
                                    ],
                                },
                            },
                        ],
                    },
                },
                "documents",
                4,
                [["datasets"], [], ["datasets.instrument"], []],
                [
                    [],
                    ["datasets.title", "eq", "Dataset 1", "and"],
                    [],
                    ["datasets.instrument.name", "eq", "Instrument 1", "and"],
                ],
                id="Nested related models",
            ),
        ],
    )
    def test_valid_include_filter_with_where_filter_in_scope(
        self,
        test_request_filter,
        test_entity_name,
        expected_length,
        expected_included_entities,
        expected_where_filter_data,
    ):
        # TODO
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

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
                assert test_filter.boolean_operator == where_filter_data[3]

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_length"
        ", expected_included_entities",
        [
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "datasets",
                                "scope": {"include": [{"relation": "parameters"}]},
                            },
                        ],
                    },
                },
                "documents",
                2,
                [["datasets"], ["datasets.parameters"]],
                id="Single related model",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "datasets",
                                "scope": {
                                    "include": [
                                        {"relation": "parameters"},
                                        {"relation": "instrument"},
                                    ],
                                },
                            },
                        ],
                    },
                },
                "documents",
                3,
                [["datasets"], ["datasets.parameters"], ["datasets.instrument"]],
                id="Multiple related models",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "datasets",
                                "scope": {
                                    "include": [
                                        {
                                            "relation": "documents",
                                            "scope": {
                                                "include": [{"relation": "parameters"}],
                                            },
                                        },
                                    ],
                                },
                            },
                        ],
                    },
                },
                "instruments",
                3,
                [
                    ["datasets"],
                    ["datasets.documents"],
                    ["datasets.documents.parameters"],
                ],
                id="Nested related models",
            ),
        ],
    )
    def test_valid_include_filter_with_include_filter_in_scope(
        self,
        test_request_filter,
        test_entity_name,
        expected_length,
        expected_included_entities,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        assert len(filters) == expected_length

        for test_filter, included_entities in zip(filters, expected_included_entities):
            if isinstance(test_filter, SearchAPIIncludeFilter):
                assert test_filter.included_filters == included_entities

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_length"
        ", expected_included_entities, expected_limit_values",
        [
            pytest.param(
                {
                    "filter": {
                        "include": [{"relation": "datasets", "scope": {"limit": 50}}],
                    },
                },
                "documents",
                2,
                [["datasets"], []],
                [None, 50],
                id="Single related model",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {"relation": "datasets", "scope": {"limit": 50}},
                            {"relation": "parameters", "scope": {"limit": 20}},
                        ],
                    },
                },
                "documents",
                4,
                [["datasets"], [], ["parameters"], []],
                [None, 50, None, 20],
                id="Multiple related model",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "datasets",
                                "scope": {
                                    "include": [
                                        {
                                            "relation": "documents",
                                            "scope": {
                                                "include": [{"relation": "parameters"}],
                                                "limit": 20,
                                            },
                                        },
                                    ],
                                    "limit": 50,
                                },
                            },
                        ],
                    },
                },
                "documents",
                5,
                [
                    ["datasets"],
                    ["datasets.documents"],
                    ["datasets.documents.parameters"],
                    [],
                    [],
                ],
                [None, None, None, 20, 50],
                id="Nested related models",
            ),
        ],
    )
    def test_valid_include_filter_with_limit_filter_in_scope(
        self,
        test_request_filter,
        test_entity_name,
        expected_length,
        expected_included_entities,
        expected_limit_values,
    ):
        # TODO - do we need to support this??
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        assert len(filters) == expected_length

        for test_filter, included_entities, limit_value in zip(
            filters, expected_included_entities, expected_limit_values,
        ):
            if isinstance(test_filter, SearchAPIIncludeFilter):
                assert test_filter.included_filters == included_entities
            if isinstance(test_filter, SearchAPILimitFilter):
                assert test_filter.limit_value == limit_value

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_length"
        ", expected_included_entities, expected_skip_values",
        [
            pytest.param(
                {
                    "filter": {
                        "include": [{"relation": "datasets", "scope": {"skip": 50}}],
                    },
                },
                "documents",
                2,
                [["datasets"], []],
                [None, 50],
                id="Single related model",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {"relation": "datasets", "scope": {"skip": 50}},
                            {"relation": "parameters", "scope": {"skip": 20}},
                        ],
                    },
                },
                "documents",
                4,
                [["datasets"], [], ["parameters"], []],
                [None, 50, None, 20],
                id="Multiple related model",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "datasets",
                                "scope": {
                                    "include": [
                                        {
                                            "relation": "documents",
                                            "scope": {
                                                "include": [{"relation": "parameters"}],
                                                "skip": 20,
                                            },
                                        },
                                    ],
                                    "skip": 50,
                                },
                            },
                        ],
                    },
                },
                "documents",
                5,
                [
                    ["datasets"],
                    ["datasets.documents"],
                    ["datasets.documents.parameters"],
                    [],
                    [],
                ],
                [None, None, None, 20, 50],
                id="Nested related models",
            ),
        ],
    )
    def test_valid_include_filter_with_skip_filter_in_scope(
        self,
        test_request_filter,
        test_entity_name,
        expected_length,
        expected_included_entities,
        expected_skip_values,
    ):
        # TODO - do we need to support this??
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        assert len(filters) == expected_length

        for test_filter, included_entities, skip_value in zip(
            filters, expected_included_entities, expected_skip_values,
        ):
            if isinstance(test_filter, SearchAPIIncludeFilter):
                assert test_filter.included_filters == included_entities
            if isinstance(test_filter, SearchAPISkipFilter):
                assert test_filter.skip_value == skip_value

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_length"
        ", expected_included_entities, expected_where_filter_data"
        ", expected_limit_values, expected_skip_values",
        [
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {
                                "relation": "documents",
                                "scope": {
                                    "where": {"title": "My Title"},
                                    "include": [{"relation": "instrument"}],
                                    "limit": 50,
                                    "skip": 20,
                                },
                            },
                        ],
                    },
                },
                "datasets",
                5,
                [["documents"], [], ["documents.instrument"], [], []],
                [[], ["documents.title", "eq", "My Title", "and"], [], [], []],
                [None, None, None, 50, None],
                [None, None, None, None, 20],
                id="Simple case",
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
                                            {
                                                "and": [
                                                    {"summary": "My Test Summary"},
                                                    {"title": {"like": "Test title"}},
                                                ],
                                            },
                                            {
                                                "and": [
                                                    {"pid": "Test pid"},
                                                    {"type": {"eq": "Test type"}},
                                                ],
                                            },
                                            {
                                                "or": [
                                                    {"doi": "Test doi"},
                                                    {
                                                        "license": {
                                                            "like": "Test license",
                                                        },
                                                    },
                                                ],
                                            },
                                        ],
                                    },
                                    "include": [
                                        {
                                            "relation": "instrument",
                                            "scope": {
                                                "where": {"name": "Instrument 1"},
                                                "limit": 2,
                                            },
                                        },
                                    ],
                                    "limit": 50,
                                    "skip": 20,
                                },
                            },
                        ],
                    },
                },
                "datasets",
                12,
                [
                    ["documents"],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    ["documents.instrument"],
                    [],
                    [],
                    [],
                    [],
                ],
                [
                    [],
                    ["documents.summary", "eq", "My Test Summary", "and"],
                    ["documents.title", "like", "Test title", "and"],
                    ["documents.pid", "eq", "Test pid", "and"],
                    ["documents.type", "eq", "Test type", "and"],
                    ["documents.doi", "eq", "Test doi", "or"],
                    ["documents.license", "like", "Test license", "or"],
                    [],
                    ["documents.instrument.name", "eq", "Instrument 1", "and"],
                    [],
                    [],
                    [],
                ],
                [None, None, None, None, None, None, None, None, None, 2, 50, None],
                [None, None, None, None, None, None, None, None, None, None, None, 20],
                id="Complex case",
            ),
        ],
    )
    def test_valid_include_filter_with_all_filters_in_scope(
        self,
        test_request_filter,
        test_entity_name,
        expected_length,
        expected_included_entities,
        expected_where_filter_data,
        expected_limit_values,
        expected_skip_values,
    ):
        # TODO - are we going to support limit in include? If not, probably remove test?
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        assert len(filters) == expected_length

        for (
            test_filter,
            included_entities,
            where_filter_data,
            limit_value,
            skip_value,
        ) in zip(
            filters,
            expected_included_entities,
            expected_where_filter_data,
            expected_limit_values,
            expected_skip_values,
        ):
            if isinstance(test_filter, SearchAPIIncludeFilter):
                assert test_filter.included_filters == included_entities
            if isinstance(test_filter, SearchAPIWhereFilter):
                assert test_filter.field == where_filter_data[0]
                assert test_filter.operation == where_filter_data[1]
                assert test_filter.value == where_filter_data[2]
                assert test_filter.boolean_operator == where_filter_data[3]
            if isinstance(test_filter, SearchAPILimitFilter):
                assert test_filter.limit_value == limit_value
            if isinstance(test_filter, SearchAPISkipFilter):
                assert test_filter.skip_value == skip_value

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
        "test_request_filter, test_entity_name, expected_length"
        ", expected_included_entities, expected_where_filter_data"
        ", expected_limit_values, expected_skip_values",
        [
            pytest.param(
                {
                    "filter": {
                        "where": {"title": "My Title"},
                        "include": [{"relation": "instrument"}],
                        "limit": 50,
                        "skip": 20,
                    },
                },
                "datasets",
                4,
                [[], ["instrument"], [], []],
                [["title", "eq", "My Title", "and"], [], [], []],
                [None, None, 50, None],
                [None, None, None, 20],
                id="Simple case",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {
                                    "and": [
                                        {"summary": "My Test Summary"},
                                        {"title": {"like": "Test title"}},
                                    ],
                                },
                                {
                                    "and": [
                                        {"pid": "Test pid"},
                                        {"type": {"eq": "Test type"}},
                                    ],
                                },
                                {
                                    "or": [
                                        {"doi": "Test doi"},
                                        {"license": {"like": "Test license"}},
                                    ],
                                },
                            ],
                        },
                        "include": [
                            {
                                "relation": "instrument",
                                "scope": {
                                    "where": {"name": "Instrument 1"},
                                    "limit": 2,
                                },
                            },
                        ],
                        "limit": 50,
                        "skip": 20,
                    },
                },
                "datasets",
                11,
                [[], [], [], [], [], [], ["instrument"], [], [], [], []],
                [
                    ["summary", "eq", "My Test Summary", "and"],
                    ["title", "like", "Test title", "and"],
                    ["pid", "eq", "Test pid", "and"],
                    ["type", "eq", "Test type", "and"],
                    ["doi", "eq", "Test doi", "or"],
                    ["license", "like", "Test license", "or"],
                    [],
                    ["instrument.name", "eq", "Instrument 1", "and"],
                    [],
                    [],
                    [],
                ],
                [None, None, None, None, None, None, None, None, 2, 50, None],
                [None, None, None, None, None, None, None, None, None, None, 20],
                id="Complex case",
            ),
        ],
    )
    def test_valid_filter_input_with_all_filters(
        self,
        test_request_filter,
        test_entity_name,
        expected_length,
        expected_included_entities,
        expected_where_filter_data,
        expected_limit_values,
        expected_skip_values,
    ):
        # TODO - remove limit from scope
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        assert len(filters) == expected_length

        for (
            test_filter,
            included_entities,
            where_filter_data,
            limit_value,
            skip_value,
        ) in zip(
            filters,
            expected_included_entities,
            expected_where_filter_data,
            expected_limit_values,
            expected_skip_values,
        ):
            if isinstance(test_filter, SearchAPIIncludeFilter):
                assert test_filter.included_filters == included_entities
            if isinstance(test_filter, SearchAPIWhereFilter):
                assert test_filter.field == where_filter_data[0]
                assert test_filter.operation == where_filter_data[1]
                assert test_filter.value == where_filter_data[2]
                assert test_filter.boolean_operator == where_filter_data[3]
            if isinstance(test_filter, SearchAPILimitFilter):
                assert test_filter.limit_value == limit_value
            if isinstance(test_filter, SearchAPISkipFilter):
                assert test_filter.skip_value == skip_value

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
