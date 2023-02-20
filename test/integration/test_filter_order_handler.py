import pytest

from datagateway_api.src.common.filter_order_handler import FilterOrderHandler
from datagateway_api.src.datagateway_api.icat.filters import (
    PythonICATIncludeFilter,
    PythonICATLimitFilter,
    PythonICATWhereFilter,
)
from datagateway_api.src.search_api.filters import SearchAPIIncludeFilter


class TestFilterOrderHandler:
    """
    `merge_python_icat_limit_skip_filters` and`clear_python_icat_order_filters()` are
    tested while testing the ICAT backend filters, so tests of these functions won't be
    found here
    """

    def test_add_filter(self, icat_query):
        test_handler = FilterOrderHandler()
        test_filter = PythonICATWhereFilter("id", 2, "eq")

        test_handler.add_filter(test_filter)

        assert test_handler.filters == [test_filter]

    def test_add_filters(self):
        test_handler = FilterOrderHandler()
        id_filter = PythonICATWhereFilter("id", 2, "eq")
        name_filter = PythonICATWhereFilter("name", "New Name", "like")
        filter_list = [id_filter, name_filter]

        test_handler.add_filters(filter_list)

        assert test_handler.filters == filter_list

    def test_remove_filter(self):
        test_filter = PythonICATWhereFilter("id", 2, "eq")

        test_handler = FilterOrderHandler()
        test_handler.add_filter(test_filter)
        test_handler.remove_filter(test_filter)

        assert test_handler.filters == []

    def test_remove_not_added_filter(self):
        test_handler = FilterOrderHandler()
        test_filter = PythonICATWhereFilter("id", 2, "eq")

        with pytest.raises(ValueError):
            test_handler.remove_filter(test_filter)

    def test_sort_filters(self):
        limit_filter = PythonICATLimitFilter(10)
        where_filter = PythonICATWhereFilter("id", 2, "eq")

        test_handler = FilterOrderHandler()
        test_handler.add_filters([limit_filter, where_filter])
        test_handler.sort_filters()

        assert test_handler.filters == [where_filter, limit_filter]

    def test_apply_filters(self, icat_query):
        where_filter = PythonICATWhereFilter("id", 2, "eq")
        limit_filter = PythonICATLimitFilter(10)

        test_handler = FilterOrderHandler()
        test_handler.add_filters([where_filter, limit_filter])
        test_handler.apply_filters(icat_query)

        assert icat_query.conditions == {"id": ["%s = '2'"]} and icat_query.limit == (
            0,
            10,
        )

    @pytest.mark.parametrize(
        "test_panosc_entity_name, test_filters, expected_filters_length,"
        "expected_num_of_python_include_filters, expected_icat_relations",
        [
            pytest.param(
                "Dataset", [], 0, 0, [], id="Dataset without related entities",
            ),
            pytest.param(
                "Dataset",
                [SearchAPIIncludeFilter(["documents"], "Dataset")],
                2,
                1,
                ["investigation.type", "investigation.keywords"],
                id="Dataset with related entity",
            ),
            pytest.param(
                "Dataset",
                [SearchAPIIncludeFilter(["documents", "instrument"], "Dataset")],
                2,
                1,
                [
                    "investigation.type",
                    "investigation.keywords",
                    "datasetInstruments.instrument.facility",
                ],
                id="Dataset with related entities",
            ),
            pytest.param(
                "Dataset",
                [SearchAPIIncludeFilter(["documents.parameters.document"], "Dataset")],
                2,
                1,
                [
                    "investigation.type",
                    "investigation.keywords",
                    "investigation.parameters.type",
                    "investigation.parameters.investigation.type",
                    "investigation.parameters.investigation.keywords",
                ],
                id="Dataset with nested related entity",
            ),
            pytest.param(
                "Dataset",
                [
                    SearchAPIIncludeFilter(
                        [
                            "documents.parameters.document",
                            "parameters.dataset.instrument",
                        ],
                        "Dataset",
                    ),
                ],
                2,
                1,
                [
                    "investigation.type",
                    "investigation.keywords",
                    "investigation.parameters.type",
                    "investigation.parameters.investigation.type",
                    "investigation.parameters.investigation.keywords",
                    "parameters.type",
                    "parameters.dataset.datasetInstruments.instrument.facility",
                ],
                id="Dataset with nested related entities",
            ),
            pytest.param(
                "Document",
                [
                    SearchAPIIncludeFilter(["parameters"], "Document"),
                    PythonICATIncludeFilter(["type", "keywords"]),
                ],
                2,
                1,
                ["type", "keywords", "parameters.type"],
                id="Document with related entity",
            ),
        ],
    )
    def test_add_icat_relations_for_non_related_fields_of_panosc_related_entities(
        self,
        test_panosc_entity_name,
        test_filters,
        expected_filters_length,
        expected_num_of_python_include_filters,
        expected_icat_relations,
    ):
        handler = FilterOrderHandler()
        handler.add_filters(test_filters)
        handler.add_icat_relations_for_non_related_fields_of_panosc_related_entities(
            test_panosc_entity_name,
        )

        actual_num_of_python_include_filters = 0
        for filter_ in handler.filters:
            if type(filter_) == PythonICATIncludeFilter:
                actual_num_of_python_include_filters += 1
                assert filter_.included_filters == expected_icat_relations

        assert (
            actual_num_of_python_include_filters
            == expected_num_of_python_include_filters
        )
        assert len(handler.filters) == expected_filters_length
