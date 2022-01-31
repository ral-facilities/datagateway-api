import pytest

from datagateway_api.src.datagateway_api.filter_order_handler import FilterOrderHandler
from datagateway_api.src.search_api.filters import SearchAPIIncludeFilter
from datagateway_api.src.search_api.query import SearchAPIQuery


class TestSearchAPIIncludeFilter:
    def test_valid_apply_filter_single(self):
        filter_input = SearchAPIIncludeFilter("documents", "Dataset")
        entity_name = "Dataset"
        expected_query = "SELECT o FROM Dataset o INCLUDE o.investigation"

        filter_handler = FilterOrderHandler()
        filter_handler.add_filter(filter_input)
        test_query = SearchAPIQuery(entity_name)

        filter_handler.apply_filters(test_query)

        assert expected_query == str(test_query.icat_query.query)

    @pytest.mark.parametrize(
        "test_include_filter, entity_name, expected_query",
        [
            pytest.param(
                SearchAPIIncludeFilter(["documents"], "Dataset"),
                "Dataset",
                "SELECT o FROM Dataset o INCLUDE o.investigation",
                id="Dataset.documents",
            ),
            pytest.param(
                SearchAPIIncludeFilter(["datasets"], "Document"),
                "Document",
                "SELECT o FROM Investigation o INCLUDE o.datasets",
                id="Document.datasets",
            ),
            pytest.param(
                SearchAPIIncludeFilter(["samples"], "Dataset"),
                "Dataset",
                "SELECT o FROM Dataset o INCLUDE o.sample",
                id="Dataset.samples",
            ),
            pytest.param(
                SearchAPIIncludeFilter(["members"], "Document"),
                "Document",
                "SELECT o FROM Investigation o INCLUDE o.investigationUsers",
                id="Document.members",
            ),
            pytest.param(
                SearchAPIIncludeFilter(["members.person"], "Document"),
                "Document",
                "SELECT o FROM Investigation o INCLUDE o.investigationUsers AS iu,"
                " iu.user",
                id="Document.members.person",
            ),
            pytest.param(
                SearchAPIIncludeFilter(["dataset.samples.datasets"], "File"),
                "File",
                "SELECT o FROM Datafile o INCLUDE o.dataset AS ds, ds.sample AS s1,"
                " s1.datasets",
                id="File.dataset.samples.datasets",
            ),
            pytest.param(
                SearchAPIIncludeFilter(["dataset.samples.datasets.documents"], "File"),
                "File",
                "SELECT o FROM Datafile o INCLUDE o.dataset AS ds, ds.sample AS s1,"
                " s1.datasets AS s2, s2.investigation",
                id="File.dataset.samples.datasets.documents",
            ),
            pytest.param(
                SearchAPIIncludeFilter(["datasets", "members"], "Document"),
                "Document",
                "SELECT o FROM Investigation o INCLUDE o.datasets,"
                " o.investigationUsers",
                id="Document.datasets & Document.members",
            ),
            pytest.param(
                SearchAPIIncludeFilter(["dataset", "dataset.samples"], "File"),
                "File",
                "SELECT o FROM Datafile o INCLUDE o.dataset AS ds, ds.sample",
                id="File.dataset & File.dataset.samples",
            ),
            pytest.param(
                SearchAPIIncludeFilter(["documents", "files", "samples"], "Dataset"),
                "Dataset",
                "SELECT o FROM Dataset o INCLUDE o.datafiles, o.investigation,"
                " o.sample",
                id="List of three included entities",
            ),
        ],
    )
    def test_valid_apply_filter(self, test_include_filter, entity_name, expected_query):
        filter_handler = FilterOrderHandler()
        filter_handler.add_filter(test_include_filter)
        test_query = SearchAPIQuery(entity_name)

        filter_handler.apply_filters(test_query)

        assert expected_query == str(test_query.icat_query.query)
