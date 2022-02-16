import pytest

from datagateway_api.src.common.exceptions import FilterError, SearchAPIError
from datagateway_api.src.search_api.filters import (
    SearchAPIIncludeFilter,
    SearchAPILimitFilter,
    SearchAPISkipFilter,
    SearchAPIWhereFilter,
)
from datagateway_api.src.search_api.nested_where_filters import NestedWhereFilters
from datagateway_api.src.search_api.query import SearchAPIQuery
from datagateway_api.src.search_api.query_filter_factory import (
    SearchAPIQueryFilterFactory,
)


class TestSearchAPIQueryFilterFactory:
    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_where",
        [
            pytest.param(
                {"filter": {"where": {"title": "My Title"}}},
                "Document",
                SearchAPIWhereFilter("title", "My Title", "eq"),
                id="Property value with no operator",
            ),
            pytest.param(
                {"filter": {"where": {"summary": {"like": "My Test Summary"}}}},
                "Document",
                SearchAPIWhereFilter("summary", "My Test Summary", "like"),
                id="Property value with operator",
            ),
            pytest.param(
                {"where": {"summary": {"like": "My Test Summary"}}},
                "Document",
                SearchAPIWhereFilter("summary", "My Test Summary", "like"),
                id="WHERE filter in syntax for count endpoints",
            ),
        ],
    )
    def test_valid_where_filter(
        self, test_request_filter, test_entity_name, expected_where,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        assert len(filters) == 1
        assert repr(filters[0]) == repr(expected_where)

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_filters",
        [
            pytest.param(
                {"filter": {"where": {"isPublic": True}}},
                "Dataset",
                [],
                id="Public data",
            ),
            pytest.param(
                {"filter": {"where": {"isPublic": {"neq": False}}}},
                "Dataset",
                [],
                id="Public data - neq operator",
            ),
            pytest.param(
                {"filter": {"where": {"isPublic": {"eq": False}}}},
                "Dataset",
                [SearchAPISkipFilter(1), SearchAPILimitFilter(0)],
                id="Non-public data",
            ),
            pytest.param(
                {"filter": {"where": {"isPublic": {"neq": True}}}},
                "Dataset",
                [SearchAPISkipFilter(1), SearchAPILimitFilter(0)],
                id="Non-public data - neq operator",
            ),
        ],
    )
    def test_valid_where_filter_on_is_public_field(
        self, test_request_filter, test_entity_name, expected_filters,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        assert len(filters) == len(expected_filters)
        for test_filter in filters:
            if isinstance(test_filter, SearchAPISkipFilter):
                assert test_filter.skip_value == 1
            if isinstance(test_filter, SearchAPILimitFilter):
                assert test_filter.limit_value == 0

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_lhs, expected_rhs"
        ", expected_joining_operator",
        [
            pytest.param(
                {"filter": {"where": {"text": "Dataset 1"}}},
                "Dataset",
                [],
                [SearchAPIWhereFilter("title", "Dataset 1", "like")],
                "or",
                id="Text operator on dataset",
            ),
            pytest.param(
                {"filter": {"where": {"text": "Instrument 1"}}},
                "Instrument",
                [SearchAPIWhereFilter("name", "Instrument 1", "like")],
                [SearchAPIWhereFilter("facility", "Instrument 1", "like")],
                "or",
                id="Text operator on instrument",
            ),
        ],
    )
    def test_valid_where_filter_text_operator(
        self,
        test_request_filter,
        test_entity_name,
        expected_lhs,
        expected_rhs,
        expected_joining_operator,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        assert len(filters) == 1
        assert isinstance(filters[0], NestedWhereFilters)
        assert repr(filters[0].lhs) == repr(expected_lhs)
        assert repr(filters[0].rhs) == repr(expected_rhs)
        assert filters[0].joining_operator == expected_joining_operator
        assert repr(filters[0].search_api_query) == repr(
            SearchAPIQuery(test_entity_name),
        )

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name",
        [
            pytest.param(
                {"filter": {"where": {"text": "Instrument 1"}}},
                "UnknownEntity",
                id="Unknown entity",
            ),
        ],
    )
    def test_invalid_where_filter_text_operator(
        self, test_request_filter, test_entity_name,
    ):
        with pytest.raises(SearchAPIError):
            SearchAPIQueryFilterFactory.get_query_filter(
                test_request_filter, test_entity_name,
            )

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_lhs, expected_rhs"
        ", expected_joining_operator",
        [
            pytest.param(
                {"filter": {"where": {"and": [{"summary": "My Test Summary"}]}}},
                "Document",
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
                "Document",
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
                "Document",
                [
                    SearchAPIWhereFilter("summary", "My Test Summary", "eq"),
                    SearchAPIWhereFilter("title", "Test title", "eq"),
                ],
                [SearchAPIWhereFilter("type", "Test type", "eq")],
                "and",
                id="Multiple conditions (three), property values with no operator",
            ),
            pytest.param(
                {"filter": {"where": {"and": [{"size": {"lt": 50}}]}}},
                "File",
                [],
                [SearchAPIWhereFilter("size", 50, "lt")],
                "and",
                id="Single condition, property value with operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {"role": {"like": "Test role"}},
                                {"size": {"gte": 275}},
                            ],
                        },
                    },
                },
                "Member",
                [SearchAPIWhereFilter("role", "Test role", "like")],
                [SearchAPIWhereFilter("size", 275, "gte")],
                "and",
                id="Multiple conditions (two), property values with operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "and": [
                                {"name": {"like": "Test name"}},
                                {"size": {"gte": 275}},
                                {"path": {"nlike": "Test path"}},
                            ],
                        },
                    },
                },
                "File",
                [
                    SearchAPIWhereFilter("name", "Test name", "like"),
                    SearchAPIWhereFilter("size", 275, "gte"),
                ],
                [SearchAPIWhereFilter("path", "Test path", "nlike")],
                "and",
                id="Multiple conditions (three), property values with operator",
            ),
            pytest.param(
                {"filter": {"where": {"and": [{"text": "Dataset 1"}]}}},
                "Dataset",
                [],
                [
                    NestedWhereFilters(
                        [], SearchAPIWhereFilter("title", "Dataset 1", "like"), "or",
                    ),
                ],
                "and",
                id="Single condition, text operator on dataset",
            ),
            pytest.param(
                {"filter": {"where": {"and": [{"text": "Instrument 1"}]}}},
                "Instrument",
                [],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("name", "Instrument 1", "like")],
                        [SearchAPIWhereFilter("facility", "Instrument 1", "like")],
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
                "Dataset",
                [
                    NestedWhereFilters(
                        [], [SearchAPIWhereFilter("title", "Dataset 1", "like")], "or",
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
                "Instrument",
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("name", "Instrument 1", "like")],
                        [SearchAPIWhereFilter("facility", "Instrument 1", "like")],
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
                "Dataset",
                [
                    NestedWhereFilters(
                        [], [SearchAPIWhereFilter("title", "Dataset 1", "like")], "or",
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
                "Instrument",
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("name", "Instrument 1", "like")],
                        [SearchAPIWhereFilter("facility", "Instrument 1", "like")],
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
        expected_lhs,
        expected_rhs,
        expected_joining_operator,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        assert len(filters) == 1
        assert isinstance(filters[0], NestedWhereFilters)
        assert repr(filters[0].lhs) == repr(expected_lhs)
        assert repr(filters[0].rhs) == repr(expected_rhs)
        assert filters[0].joining_operator == expected_joining_operator
        assert repr(filters[0].search_api_query) == repr(
            SearchAPIQuery(test_entity_name),
        )

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_lhs, expected_rhs"
        ", expected_joining_operator",
        [
            pytest.param(
                {"filter": {"where": {"or": [{"summary": "My Test Summary"}]}}},
                "Document",
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
                "Document",
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
                "Document",
                [
                    SearchAPIWhereFilter("summary", "My Test Summary", "eq"),
                    SearchAPIWhereFilter("title", "Test title", "eq"),
                ],
                [SearchAPIWhereFilter("type", "Test type", "eq")],
                "or",
                id="Multiple conditions (three), property values with no operator",
            ),
            pytest.param(
                {"filter": {"where": {"or": [{"size": {"lt": 50}}]}}},
                "File",
                [],
                [SearchAPIWhereFilter("size", 50, "lt")],
                "or",
                id="Single condition, property value with operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [
                                {"name": {"like": "Test name"}},
                                {"size": {"gte": 275}},
                            ],
                        },
                    },
                },
                "File",
                [SearchAPIWhereFilter("name", "Test name", "like")],
                [SearchAPIWhereFilter("size", 275, "gte")],
                "or",
                id="Multiple conditions (two), property values with operator",
            ),
            pytest.param(
                {
                    "filter": {
                        "where": {
                            "or": [
                                {"name": {"like": "Test name"}},
                                {"size": {"gte": 275}},
                                {"path": {"nlike": "Test path"}},
                            ],
                        },
                    },
                },
                "File",
                [
                    SearchAPIWhereFilter("name", "Test name", "like"),
                    SearchAPIWhereFilter("size", 275, "gte"),
                ],
                [SearchAPIWhereFilter("path", "Test path", "nlike")],
                "or",
                id="Multiple conditions (three), property values with operator",
            ),
            pytest.param(
                {"filter": {"where": {"or": [{"text": "Dataset 1"}]}}},
                "Dataset",
                [],
                [
                    NestedWhereFilters(
                        [], SearchAPIWhereFilter("title", "Dataset 1", "like"), "or",
                    ),
                ],
                "or",
                id="Single condition, text operator on dataset",
            ),
            pytest.param(
                {"filter": {"where": {"or": [{"text": "Instrument 1"}]}}},
                "Instrument",
                [],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("name", "Instrument 1", "like")],
                        [SearchAPIWhereFilter("facility", "Instrument 1", "like")],
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
                "Dataset",
                [
                    NestedWhereFilters(
                        [], [SearchAPIWhereFilter("title", "Dataset 1", "like")], "or",
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
                "Instrument",
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("name", "Instrument 1", "like")],
                        [SearchAPIWhereFilter("facility", "Instrument 1", "like")],
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
                "Dataset",
                [
                    NestedWhereFilters(
                        [], [SearchAPIWhereFilter("title", "Dataset 1", "like")], "or",
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
                "Instrument",
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("name", "Instrument 1", "like")],
                        [SearchAPIWhereFilter("facility", "Instrument 1", "like")],
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
        expected_lhs,
        expected_rhs,
        expected_joining_operator,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        assert len(filters) == 1
        assert isinstance(filters[0], NestedWhereFilters)
        assert repr(filters[0].lhs) == repr(expected_lhs)
        assert repr(filters[0].rhs) == repr(expected_rhs)
        assert filters[0].joining_operator == expected_joining_operator
        assert repr(filters[0].search_api_query) == repr(
            SearchAPIQuery(test_entity_name),
        )

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_lhs, expected_rhs"
        ", expected_joining_operator",
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
                "Document",
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
                "Document",
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
                "Document",
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
                "Document",
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
                "Document",
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
                "Document",
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
                "Document",
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
        expected_lhs,
        expected_rhs,
        expected_joining_operator,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        assert len(filters) == 1
        assert isinstance(filters[0], NestedWhereFilters)
        assert repr(filters[0].lhs) == repr(expected_lhs)
        assert repr(filters[0].rhs) == repr(expected_rhs)
        assert filters[0].joining_operator == expected_joining_operator
        assert repr(filters[0].search_api_query) == repr(
            SearchAPIQuery(test_entity_name),
        )

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_lhs, expected_rhs"
        ", expected_joining_operator",
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
                "Document",
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
                "Document",
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
                "Document",
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
                "Document",
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
                "Document",
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
                "Document",
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
                "Document",
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
        expected_lhs,
        expected_rhs,
        expected_joining_operator,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        assert len(filters) == 1
        assert isinstance(filters[0], NestedWhereFilters)
        assert repr(filters[0].lhs) == repr(expected_lhs)
        assert repr(filters[0].rhs) == repr(expected_rhs)
        assert filters[0].joining_operator == expected_joining_operator
        assert repr(filters[0].search_api_query) == repr(
            SearchAPIQuery(test_entity_name),
        )

    @pytest.mark.parametrize(
        "test_request_filter, test_entity_name, expected_length"
        ", expected_included_entities",
        [
            pytest.param(
                {"filter": {"include": [{"relation": "files"}]}},
                "Dataset",
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
                "Dataset",
                1,
                [["files", "instrument"]],
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
        ", expected_included_entities, expected_where_filter_data"
        ", expected_nested_wheres",
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
                "Dataset",
                2,
                [["parameters"]],
                [SearchAPIWhereFilter("parameters.name", "My parameter", "eq")],
                "",
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
                "Dataset",
                2,
                [["parameters"]],
                [SearchAPIWhereFilter("parameters.name", "My parameter", "ne")],
                "",
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
                "Dataset",
                2,
                [["files"]],
                [],
                [
                    NestedWhereFilters(
                        [], [SearchAPIWhereFilter("files.name", "file1", "like")], "or",
                    ),
                ],
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
                "Dataset",
                1,
                [["parameters"]],
                [],
                [],
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
                "Dataset",
                2,
                [["documents"]],
                [],
                [
                    NestedWhereFilters(
                        [SearchAPIWhereFilter("documents.title", "document1", "like")],
                        [
                            SearchAPIWhereFilter(
                                "documents.summary", "document1", "like",
                            ),
                        ],
                        "or",
                    ),
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
                "Dataset",
                2,
                [["documents"]],
                [],
                [
                    NestedWhereFilters(
                        [
                            SearchAPIWhereFilter(
                                "documents.summary", "My Test Summary", "eq",
                            ),
                        ],
                        [SearchAPIWhereFilter("documents.title", "Test title", "eq")],
                        "and",
                    ),
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
                                        "or": [
                                            {"summary": "My Test Summary"},
                                            {"title": "Test title"},
                                        ],
                                    },
                                },
                            },
                        ],
                    },
                },
                "Dataset",
                2,
                [["documents"]],
                [],
                [
                    NestedWhereFilters(
                        [
                            SearchAPIWhereFilter(
                                "documents.summary", "My Test Summary", "eq",
                            ),
                        ],
                        [SearchAPIWhereFilter("documents.title", "Test title", "eq")],
                        "or",
                    ),
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
                "Dataset",
                2,
                [["documents"]],
                [],
                [
                    NestedWhereFilters(
                        [
                            NestedWhereFilters(
                                [
                                    SearchAPIWhereFilter(
                                        "documents.summary", "My Test Summary", "eq",
                                    ),
                                ],
                                [
                                    SearchAPIWhereFilter(
                                        "documents.title", "Test title", "like",
                                    ),
                                ],
                                "and",
                            ),
                            NestedWhereFilters(
                                [
                                    SearchAPIWhereFilter(
                                        "documents.pid", "Test pid", "eq",
                                    ),
                                ],
                                [
                                    SearchAPIWhereFilter(
                                        "documents.type", "Test type", "eq",
                                    ),
                                ],
                                "and",
                            ),
                        ],
                        [
                            NestedWhereFilters(
                                [
                                    SearchAPIWhereFilter(
                                        "documents.doi", "Test doi", "eq",
                                    ),
                                ],
                                [
                                    SearchAPIWhereFilter(
                                        "documents.license", "Test license", "like",
                                    ),
                                ],
                                "or",
                            ),
                        ],
                        "and",
                    ),
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
                "Dataset",
                2,
                [["documents"]],
                [],
                [
                    NestedWhereFilters(
                        [
                            NestedWhereFilters(
                                [
                                    SearchAPIWhereFilter(
                                        "documents.summary", "My Test Summary", "eq",
                                    ),
                                ],
                                [
                                    SearchAPIWhereFilter(
                                        "documents.title", "Test title", "like",
                                    ),
                                ],
                                "and",
                            ),
                            NestedWhereFilters(
                                [
                                    SearchAPIWhereFilter(
                                        "documents.pid", "Test pid", "eq",
                                    ),
                                ],
                                [
                                    SearchAPIWhereFilter(
                                        "documents.type", "Test type", "eq",
                                    ),
                                ],
                                "and",
                            ),
                        ],
                        [
                            NestedWhereFilters(
                                [
                                    SearchAPIWhereFilter(
                                        "documents.doi", "Test doi", "eq",
                                    ),
                                ],
                                [
                                    SearchAPIWhereFilter(
                                        "documents.license", "Test license", "like",
                                    ),
                                ],
                                "or",
                            ),
                        ],
                        "or",
                    ),
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
                "Dataset",
                3,
                [["parameters", "documents"]],
                [
                    SearchAPIWhereFilter("parameters.name", "My parameter", "eq"),
                    SearchAPIWhereFilter("documents.title", "Document title", "eq"),
                ],
                [],
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
                "Document",
                3,
                [["datasets.instrument"]],
                [
                    SearchAPIWhereFilter("datasets.title", "Dataset 1", "eq"),
                    SearchAPIWhereFilter(
                        "datasets.instrument.name", "Instrument 1", "eq",
                    ),
                ],
                [],
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
        expected_nested_wheres,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        assert len(filters) == expected_length
        for test_filter in filters:
            if isinstance(test_filter, SearchAPIIncludeFilter):
                assert test_filter.panosc_entity_name == test_entity_name
                for expected_include in expected_included_entities:
                    assert test_filter.included_filters == expected_include
                    expected_included_entities.remove(expected_include)
            if isinstance(test_filter, NestedWhereFilters):
                for expected_nested in expected_nested_wheres:
                    assert repr(test_filter) == repr(expected_nested)
                    expected_nested_wheres.remove(expected_nested)
            if isinstance(test_filter, SearchAPIWhereFilter):
                for expected_where in expected_where_filter_data:
                    assert repr(test_filter) == repr(expected_where)
                    expected_where_filter_data.remove(expected_where)

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
                "Document",
                1,
                [["datasets.parameters"]],
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
                "Document",
                1,
                [["datasets.parameters", "datasets.instrument"]],
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
                "Instrument",
                1,
                [["datasets.documents.parameters"]],
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
        for test_filter in filters:
            if isinstance(test_filter, SearchAPIIncludeFilter):
                for expected_include in expected_included_entities:
                    assert test_filter.included_filters == expected_include
                    expected_included_entities.remove(expected_include)

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
        ", expected_nested_wheres, expected_limit_values, expected_skip_values",
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
                "Dataset",
                4,
                [["instrument"]],
                [SearchAPIWhereFilter("title", "My Title", "eq")],
                [],
                [50],
                [20],
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
                                "scope": {"where": {"name": "Instrument 1"}},
                            },
                        ],
                        "limit": 50,
                        "skip": 20,
                    },
                },
                "Dataset",
                5,
                [["instrument"]],
                [SearchAPIWhereFilter("instrument.name", "Instrument 1", "eq")],
                [
                    NestedWhereFilters(
                        [
                            NestedWhereFilters(
                                [
                                    SearchAPIWhereFilter(
                                        "summary", "My Test Summary", "eq",
                                    ),
                                ],
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
                                [
                                    SearchAPIWhereFilter(
                                        "license", "Test license", "like",
                                    ),
                                ],
                                "or",
                            ),
                        ],
                        "and",
                    ),
                ],
                [50],
                [20],
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
        expected_nested_wheres,
        expected_limit_values,
        expected_skip_values,
    ):
        filters = SearchAPIQueryFilterFactory.get_query_filter(
            test_request_filter, test_entity_name,
        )

        assert len(filters) == expected_length
        for test_filter in filters:
            if isinstance(test_filter, SearchAPIIncludeFilter):
                for expected_include in expected_included_entities:
                    assert test_filter.included_filters == expected_include
                    expected_included_entities.remove(expected_include)
            if isinstance(test_filter, NestedWhereFilters):
                for expected_nested in expected_nested_wheres:
                    assert repr(test_filter) == repr(expected_nested)
                    expected_nested_wheres.remove(expected_nested)
            if isinstance(test_filter, SearchAPIWhereFilter):
                for expected_where in expected_where_filter_data:
                    assert repr(test_filter) == repr(expected_where)
                    expected_where_filter_data.remove(expected_where)
            if isinstance(test_filter, SearchAPILimitFilter):
                for expected_limit in expected_limit_values:
                    assert test_filter.limit_value == expected_limit
                    expected_limit_values.remove(expected_limit)
            if isinstance(test_filter, SearchAPISkipFilter):
                for expected_skip in expected_skip_values:
                    assert test_filter.skip_value == expected_skip
                    expected_skip_values.remove(expected_skip)

    @pytest.mark.parametrize(
        "test_request_filter",
        [
            pytest.param("invalid query filter input", id="Generally invalid input"),
            pytest.param({"filter": {"test": "value"}}, id="Invalid filter name"),
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
            pytest.param(
                {
                    "filter": {
                        "include": [
                            {"relation": "parameters", "scope": {"limit": 50}},
                        ],
                    },
                },
                id="Unsupported limit filter in scope of include filter",
            ),
            pytest.param(
                {
                    "filter": {
                        "include": [{"relation": "parameters", "scope": {"skip": 20}}],
                    },
                },
                id="Unsupported skip filter in scope of include filter",
            ),
            pytest.param(
                {"filter": {"where": {"isPublic": {"lt": True}}}},
                id="Unsupported operator in where filter with boolean value",
            ),
        ],
    )
    def test_invalid_filter_input(self, test_request_filter):
        with pytest.raises(FilterError):
            SearchAPIQueryFilterFactory.get_query_filter(test_request_filter)

    @pytest.mark.parametrize(
        "filter_input, expected_return",
        [
            pytest.param(
                {"property": "value"},
                ("property", "value", "eq"),
                id="No operator specified (string)",
            ),
            pytest.param(
                {"property": False},
                ("property", False, "eq"),
                id="No operator specified (bool)",
            ),
            pytest.param(
                {"property": 5},
                ("property", 5, "eq"),
                id="No operator specified (int)",
            ),
            pytest.param(
                {"property": {"eq": "value"}},
                ("property", "value", "eq"),
                id="Specific operator given in input (eq)",
            ),
            pytest.param(
                {"property": {"neq": "value"}},
                ("property", "value", "neq"),
                id="Specific operator given in input (neq)",
            ),
            pytest.param(
                {"property": {"gt": "value"}},
                ("property", "value", "gt"),
                id="Specific operator given in input (gt)",
            ),
            pytest.param(
                {"isPublic": True},
                ("isPublic", True, "eq"),
                id="No operator specified using isPublic",
            ),
            pytest.param(
                {"isPublic": {"eq": False}},
                ("isPublic", False, "eq"),
                id="Specific operator using isPublic (eq)",
            ),
            pytest.param(
                {"isPublic": {"neq": True}},
                ("isPublic", True, "neq"),
                id="Specific operator using isPublic (neq)",
            ),
        ],
    )
    def test_valid_get_condition_values(self, filter_input, expected_return):
        test_condition_values = SearchAPIQueryFilterFactory.get_condition_values(
            filter_input,
        )

        assert test_condition_values == expected_return

    @pytest.mark.parametrize(
        "filter_input",
        [
            pytest.param({"isPublic": {"lt": True}}, id="isPublic invalid operator"),
            pytest.param(
                {"name": {"gt": False}}, id="Invalid operator on boolean value",
            ),
        ],
    )
    def test_invalid_get_condition_values(self, filter_input):
        with pytest.raises(FilterError):
            SearchAPIQueryFilterFactory.get_condition_values(filter_input)

    @pytest.mark.parametrize(
        "test_filter, entity_name, expected_field_name",
        [
            pytest.param(
                SearchAPIWhereFilter("name", "test name", "eq"),
                "File",
                ["File.name"],
                id="Single where filter",
            ),
            pytest.param(
                [
                    SearchAPIWhereFilter("name", "test name", "eq"),
                    SearchAPIWhereFilter("id", 3, "eq"),
                ],
                "File",
                ["File.name", "File.id"],
                id="List of where filters",
            ),
            pytest.param(
                NestedWhereFilters(
                    [SearchAPIWhereFilter("name", "test name", "eq")],
                    [SearchAPIWhereFilter("id", 3, "eq")],
                    "OR",
                    SearchAPIQuery("File"),
                ),
                "File",
                ["File.name", "File.id"],
                id="NestedWhereFilters object",
            ),
        ],
    )
    def test_prefix_entity_name(self, test_filter, entity_name, expected_field_name):
        SearchAPIQueryFilterFactory.prefix_where_filter_field_with_entity_name(
            test_filter, entity_name,
        )

        if not isinstance(test_filter, list):
            test_filter = [test_filter]

        for filter_, field_name in zip(test_filter, expected_field_name):
            if isinstance(filter_, NestedWhereFilters):
                assert filter_.lhs[0].field == expected_field_name[0]
                assert filter_.rhs[0].field == expected_field_name[1]
            else:
                assert filter_.field == field_name

        # assert test_filter.field == expected_output
