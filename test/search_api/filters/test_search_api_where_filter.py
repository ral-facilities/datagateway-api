import pytest

from datagateway_api.src.datagateway_api.filter_order_handler import FilterOrderHandler
from datagateway_api.src.search_api.filters import SearchAPIWhereFilter
from datagateway_api.src.search_api.nested_where_filters import NestedWhereFilters
from datagateway_api.src.search_api.query import SearchAPIQuery


class TestSearchAPIWhereFilter:
    @pytest.mark.parametrize(
        "filter_input, entity_name, expected_query",
        [
            pytest.param(
                SearchAPIWhereFilter("name", "WISH", "eq"),
                "Instrument",
                "SELECT o FROM Instrument o WHERE o.name = 'WISH'",
                id="Regular WHERE filter",
            ),
            pytest.param(
                SearchAPIWhereFilter("title", "My Dataset 1", "ne"),
                "Dataset",
                "SELECT o FROM Dataset o WHERE o.name != My Dataset 1",
                id="WHERE filter with non-default operator",
            ),
            pytest.param(
                # DataGateway API date format: "2018-05-05 15:00:00"
                SearchAPIWhereFilter("startDate", "2018-05-05T15:00:00.000Z", "gt"),
                "Document",
                "SELECT o FROM Investigation o WHERE o.startDate >"
                " '2018-05-05T15:00:00.000Z'",
                id="WHERE filter with date value",
            ),
            pytest.param(
                SearchAPIWhereFilter("facility", "ISIS", "like"),
                "Instrument",
                "SELECT o FROM Instrument o JOIN o.facility AS f WHERE f.name like"
                " '%ISIS%'",
                id="WHERE filter on ICAT related entity",
            ),
            pytest.param(
                SearchAPIWhereFilter("keywords", "Keyword", "like"),
                "Document",
                "SELECT o FROM Investigation o JOIN o.keywords AS s1 WHERE s1.name like"
                " '%Keyword%'",
                id="WHERE filter on ICAT related entity with 0-many relationship",
            ),
            # TODO - add in the rest of the PaNOSC hops
            pytest.param(
                SearchAPIWhereFilter("samples.description", "Test description", "like"),
                "Dataset",
                "SELECT o FROM Dataset o JOIN o.sample AS s1 JOIN s1.parameters AS s2"
                " JOIN s2.type AS s3 WHERE s3.description like '%Test description%'",
                id="WHERE filter on ICAT related entity with a PaNOSC hop",
            ),
            pytest.param(
                SearchAPIWhereFilter("parameters.value", "My Parameter", "eq"),
                "Document",
                "SELECT o FROM Investigation o JOIN o.parameters AS p WHERE"
                " p.stringValue = 'My Parameter'",
                id="String parameter value (mapping that maps to multiple ICAT fields)",
            ),
            pytest.param(
                SearchAPIWhereFilter(
                    "parameters.value", "2018-05-05T15:00:00.000Z", "eq",
                ),
                "Document",
                "SELECT o FROM Investigation o JOIN o.parameters AS p WHERE"
                " p.dateTimeValue = '2018-05-05T15:00:00.000Z'",
                id="Datetime parameter value (mapping that maps to multiple ICAT"
                " fields)",
            ),
            pytest.param(
                SearchAPIWhereFilter("parameters.value", 20, "eq"),
                "Document",
                "SELECT o FROM Investigation o JOIN o.parameters AS p WHERE"
                " p.numericValue = '20'",
                id="Numeric (int) parameter value (mapping that maps to multiple ICAT"
                " fields)",
            ),
            pytest.param(
                SearchAPIWhereFilter("parameters.value", 20.0, "eq"),
                "Document",
                "SELECT o FROM Investigation o JOIN o.parameters AS p WHERE"
                " p.numericValue = '20.0'",
                id="Numeric (float) parameter value (mapping that maps to multiple ICAT"
                "fields)",
            ),
        ],
    )
    def test_valid_apply_where_filter(self, filter_input, entity_name, expected_query):

        filter_handler = FilterOrderHandler()
        filter_handler.add_filter(filter_input)
        test_query = SearchAPIQuery(entity_name)

        filter_handler.apply_filters(test_query)

        print(f"JPQL Query: {str(test_query.query.query)}")

        assert expected_query == str(test_query.query.query)

    @pytest.mark.parametrize(
        "filter_input, entity_name, expected_query",
        [
            pytest.param(
                NestedWhereFilters(
                    [], [SearchAPIWhereFilter("name", "SANS2D", "like")], "and",
                ),
                "Instrument",
                "SELECT o FROM Instrument o WHERE (o.name like '%SANS2D%')",
                id="Nested input with single filter",
            ),
            pytest.param(
                NestedWhereFilters(
                    [], [SearchAPIWhereFilter("facility", "ISIS", "like")], "or",
                ),
                "Instrument",
                "SELECT o FROM Instrument o JOIN o.facility AS f WHERE (f.name like"
                " '%ISIS%')",
                id="Nested input with single filter on ICAT related entity",
            ),
            pytest.param(
                NestedWhereFilters(
                    [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                    [SearchAPIWhereFilter("title", "Test title", "eq")],
                    "or",
                ),
                "Document",
                "SELECT o FROM Investigation o WHERE (o.summary = 'My Test Summary' or"
                " o.name = 'Test title')",
                id="Nested input with LHS and RHS present",
            ),
            pytest.param(
                NestedWhereFilters(
                    [SearchAPIWhereFilter("summary", "My Test Summary", "eq")],
                    [SearchAPIWhereFilter("keywords", "Test keyword", "eq")],
                    "and",
                ),
                "Document",
                "SELECT o FROM Investigation o JOIN o.keywords AS s1 WHERE (o.summary ="
                " 'My Test Summary' and s1.name = 'Test keyword')",
                id="Nested input with filter on ICAT related entity with 0-many"
                " relationship",
            ),
            pytest.param(
                NestedWhereFilters(
                    [SearchAPIWhereFilter("title", "Test title", "eq")],
                    [
                        SearchAPIWhereFilter(
                            "samples.description", "Test description", "like",
                        ),
                    ],
                    "and",
                ),
                "Dataset",
                "SELECT o FROM Dataset o JOIN o.sample AS s1 JOIN s1.parameters AS s2"
                " JOIN s2.type AS s3 WHERE (o.name = 'Test title' and"
                " s3.description like '%Test description%')",
                id="Nested input with filter on ICAT related entity with multiple hops",
            ),
            pytest.param(
                NestedWhereFilters(
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
                            [SearchAPIWhereFilter("doi", "Test doi", "eq")],
                            "or",
                        ),
                    ],
                    "and",
                ),
                "Document",
                "SELECT o FROM Investigation o WHERE ((o.summary = 'My Test Summary' or"
                " o.name like '%Test title%') and (o.doi = 'Test pid' or o.doi ="
                " 'Test doi'))",
                id="Nested input - (A or B) and (C or D)",
            ),
        ],
    )
    def test_valid_apply_nested_filters(
        self, filter_input, entity_name, expected_query,
    ):
        filter_handler = FilterOrderHandler()
        filter_handler.add_filter(filter_input)
        test_query = SearchAPIQuery(entity_name)
        filter_handler.add_query_to_where_filters(test_query)

        filter_handler.apply_filters(test_query)

        print(f"JPQL Query: {str(test_query.query.query)}")

        assert str(test_query.query.query) == expected_query
