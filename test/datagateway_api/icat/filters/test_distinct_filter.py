import pytest

from datagateway_api.src.datagateway_api.icat.filters import (
    PythonICATDistinctFieldFilter,
)
from datagateway_api.src.common.exceptions import FilterError


class TestICATDistinctFilter:
    @pytest.mark.parametrize(
        "attribute_name",
        [
            pytest.param("name", id="Attribute for own entity"),
            pytest.param("investigationUsers.role", id="Related attribute name"),
        ],
    )
    def test_valid_str_field_input(self, icat_query, attribute_name):
        test_filter = PythonICATDistinctFieldFilter(attribute_name)
        test_filter.apply_filter(icat_query)

        assert (
            icat_query.attributes == [attribute_name]
            and icat_query.aggregate == "DISTINCT"
        )

    def test_valid_list_fields_input(self, icat_query):
        test_filter = PythonICATDistinctFieldFilter(["doi", "name", "title"])
        test_filter.apply_filter(icat_query)

        assert (
            icat_query.attributes == ["doi", "name", "title"]
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

    @pytest.mark.parametrize(
        "existing_aggregate, expected_instance_aggregate",
        [
            pytest.param(
                "COUNT", "DISTINCT", id="Existing count aggregate (count endpoints)",
            ),
            pytest.param("AVG", "AVG:DISTINCT", id="Existing avg aggregate"),
            pytest.param("SUM", "SUM:DISTINCT", id="Existing sum aggregate"),
        ],
    )
    def test_existing_aggregate_on_query(
        self, icat_query, existing_aggregate, expected_instance_aggregate,
    ):
        icat_query.setAggregate(existing_aggregate)

        test_filter = PythonICATDistinctFieldFilter("name")
        test_filter.apply_filter(icat_query)

        assert icat_query.aggregate == expected_instance_aggregate

    def test_manual_count_flag(self, icat_query):
        icat_query.setAggregate("COUNT")

        test_filter = PythonICATDistinctFieldFilter("name")
        test_filter.apply_filter(icat_query)

        assert icat_query.manual_count
