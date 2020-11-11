import pytest


from datagateway_api.common.exceptions import FilterError
from datagateway_api.common.filter_order_handler import FilterOrderHandler
from datagateway_api.common.icat.filters import PythonICATOrderFilter


class TestICATOrderFilter:
    def test_direction_is_uppercase(self, icat_query):
        """Direction must be uppercase for Python ICAT to see the input as valid"""
        test_filter = PythonICATOrderFilter("id", "asc")

        assert test_filter.direction == "ASC"

    def test_result_order_appended(self, icat_query):
        id_filter = PythonICATOrderFilter("id", "ASC")
        title_filter = PythonICATOrderFilter("title", "DESC")

        filter_handler = FilterOrderHandler()
        filter_handler.add_filters([id_filter, title_filter])
        filter_handler.apply_filters(icat_query)

        assert PythonICATOrderFilter.result_order == [("id", "ASC"), ("title", "DESC")]

        filter_handler.clear_python_icat_order_filters()

    def test_filter_applied_to_query(self, icat_query):
        test_filter = PythonICATOrderFilter("id", "DESC")

        filter_handler = FilterOrderHandler()
        filter_handler.add_filter(test_filter)
        filter_handler.apply_filters(icat_query)

        assert icat_query.order == [("id", "DESC")]

        filter_handler.clear_python_icat_order_filters()

    def test_invalid_field(self, icat_query):
        test_filter = PythonICATOrderFilter("unknown_field", "DESC")

        filter_handler = FilterOrderHandler()
        filter_handler.add_filter(test_filter)
        with pytest.raises(FilterError):
            filter_handler.apply_filters(icat_query)

        filter_handler.clear_python_icat_order_filters()

    def test_invalid_direction(self, icat_query):
        test_filter = PythonICATOrderFilter("id", "up")

        filter_handler = FilterOrderHandler()
        filter_handler.add_filter(test_filter)
        with pytest.raises(FilterError):
            filter_handler.apply_filters(icat_query)
