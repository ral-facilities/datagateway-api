import logging

from datagateway_api.src.datagateway_api.icat.filters import (
    PythonICATLimitFilter,
    PythonICATOrderFilter,
    PythonICATSkipFilter,
)
from datagateway_api.src.search_api.nested_where_filters import NestedWhereFilters

log = logging.getLogger()


class FilterOrderHandler(object):
    """
    The FilterOrderHandler takes in filters, sorts them according to the order of
    operations, then applies them.
    """

    def __init__(self):
        self.filters = []

    def add_filter(self, query_filter):
        self.filters.append(query_filter)

    def add_filters(self, query_filter):
        self.filters.extend(query_filter)

    def remove_filter(self, query_filter):
        self.filters.remove(query_filter)

    def sort_filters(self):
        """
        Sorts the filters according to the order of operations
        """
        self.filters.sort(key=lambda x: x.precedence)

    def apply_filters(self, query):
        """
        Given a query apply the filters the handler has in the correct order.

        :param query: The query to have filters applied to
        """
        self.sort_filters()

        for query_filter in self.filters:
            query_filter.apply_filter(query)

    def merge_python_icat_limit_skip_filters(self):
        """
        When there are both limit and skip filters in a request, merge them into the
        limit filter and remove the skip filter from the instance
        """
        log.info("Merging a PythonICATSkipFilter and PythonICATLimitFilter together")
        skip_filter = None
        limit_filter = None

        for icat_filter in self.filters:
            if isinstance(icat_filter, PythonICATSkipFilter):
                skip_filter = icat_filter

            if isinstance(icat_filter, PythonICATLimitFilter):
                limit_filter = icat_filter

        if skip_filter and limit_filter:
            log.info("Merging skip filter with limit filter")
            limit_filter.skip_value = skip_filter.skip_value
            log.info("Removing skip filter from list of filters")
            self.remove_filter(skip_filter)
            log.debug("Filters: %s", self.filters)

    def clear_python_icat_order_filters(self):
        """
        Checks if any order filters have been added to the request and resets the
        variable used to manage which attribute(s) to use for sorting results.

        A reset is required because Python ICAT overwrites (as opposed to appending to
        it) the query's order list every time one is added to the query.
        """
        log.debug("Resetting result order for the order filter")

        if any(
            isinstance(icat_filter, PythonICATOrderFilter)
            for icat_filter in self.filters
        ):
            PythonICATOrderFilter.result_order = []
            PythonICATOrderFilter.join_specs = {}

    def manage_icat_filters(self, filters, query):
        """
        Utility function to call other functions in this class, used to manage filters
        when using the Python ICAT backend. These steps are the same with the different
        types of requests that utilise filters, therefore this function helps to reduce
        code duplication

        :param filters: The list of filters that will be applied to the query
        :type filters: List of specific implementations :class:`QueryFilter`
        :param query: ICAT query which will fetch the data at a later stage
        :type query: :class:`icat.query.Query`
        """

        self.add_filters(filters)
        self.merge_python_icat_limit_skip_filters()
        self.clear_python_icat_order_filters()
        self.apply_filters(query)
