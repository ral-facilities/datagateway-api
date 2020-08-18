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
        
        """
        if any(isinstance(filter, PythonICATOrderFilter) for filter in self.filters):
            PythonICATOrderFilter.result_order = []
        """

        for filter in self.filters:
            filter.apply_filter(query)
