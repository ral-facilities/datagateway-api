import pytest

from datagateway_api.common.datagateway_api.filter_order_handler import (
    FilterOrderHandler,
)
from datagateway_api.common.datagateway_api.icat.filters import (
    PythonICATLimitFilter,
    PythonICATWhereFilter,
)


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

        assert icat_query.conditions == {"id": "= '2'"} and icat_query.limit == (0, 10)
