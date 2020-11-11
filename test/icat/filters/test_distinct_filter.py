import pytest

from datagateway_api.common.exceptions import FilterError
from datagateway_api.common.icat.filters import PythonICATDistinctFieldFilter


class TestICATDistinctFilter:
    def test_valid_str_field_input(self, icat_query):
        test_filter = PythonICATDistinctFieldFilter("name")
        test_filter.apply_filter(icat_query)

        assert (
            icat_query.conditions == {"name": "!= null"}
            and icat_query.aggregate == "DISTINCT"
        )

    def test_valid_list_fields_input(self, icat_query):
        test_filter = PythonICATDistinctFieldFilter(["doi", "name", "title"])
        test_filter.apply_filter(icat_query)

        assert (
            icat_query.conditions
            == {"doi": "!= null", "name": "!= null", "title": "!= null"}
            and icat_query.aggregate == "DISTINCT"
        )

    def test_invalid_field(self, icat_query):
        test_filter = PythonICATDistinctFieldFilter("my_new_field")
        with pytest.raises(FilterError):
            test_filter.apply_filter(icat_query)

    def test_distinct_aggregate_added(self, icat_query):
        test_filter = PythonICATDistinctFieldFilter("id")
        test_filter.apply_filter(icat_query)

        assert icat_query.aggregate == "DISTINCT"

    @pytest.mark.parametrize("existing_aggregate", ["COUNT", "AVG", "SUM"])
    def test_existing_aggregate_appended(self, icat_query, existing_aggregate):
        icat_query.setAggregate(existing_aggregate)

        test_filter = PythonICATDistinctFieldFilter("name")
        test_filter.apply_filter(icat_query)

        assert icat_query.aggregate == f"{existing_aggregate}:DISTINCT"
