from common.icat.filters import (
    PythonICATLimitFilter,
    PythonICATSkipFilter,
    PythonICATOrderFilter,
)


class FilterOrderHandler(object):
    """
    The FilterOrderHandler takes in filters, sorts them according to the order of
    operations, then applies them.
    """

    def __init__(self):
        self.filters = []

    def add_filter(self, filter):
        self.filters.append(filter)

    def add_filters(self, filters):
        self.filters.extend(filters)

    def remove_filter(self, filter):
        self.filters.remove(filter)

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

        for filter in self.filters:
            filter.apply_filter(query)

    def merge_python_icat_limit_skip_filters(self):
        """
        When there are both limit and skip filters in a request, merge them into the
        limit filter and remove the skip filter from the instance
        """

        if any(
            isinstance(icat_filter, PythonICATSkipFilter)
            for icat_filter in self.filters
        ) and any(
            isinstance(icat_filter, PythonICATLimitFilter)
            for icat_filter in self.filters
        ):
            # Merge skip and limit filter into a single limit filter
            for icat_filter in self.filters:
                if isinstance(icat_filter, PythonICATSkipFilter):
                    skip_filter = icat_filter
                    request_skip_value = icat_filter.skip_value

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

        if any(
            isinstance(icat_filter, PythonICATOrderFilter)
            for icat_filter in self.filters
        ):
            PythonICATOrderFilter.result_order = []

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
