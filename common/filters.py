from abc import ABC, abstractmethod


class QueryFilter(ABC):
    @property
    @abstractmethod
    def precedence(self):
        pass

    @abstractmethod
    def apply_filter(self, query):
        pass


class WhereFilter(QueryFilter):
    precedence = 1

    def __init__(self, field, value, operation):
        self.field = field
        self.included_field = None
        self.included_included_field = None
        self._set_filter_fields()
        self.value = value
        self.operation = operation
        # super().__init__()

    def _set_filter_fields(self):
        if self.field.count(".") == 1:
            self.included_field = self.field.split(".")[1]
            self.field = self.field.split(".")[0]

        if self.field.count(".") == 2:
            self.included_included_field = self.field.split(".")[2]
            self.included_field = self.field.split(".")[1]
            self.field = self.field.split(".")[0]


class DistinctFieldFilter(QueryFilter):
    precedence = 0

    def __init__(self, fields):
        # This allows single string distinct filters
        self.fields = fields if type(fields) is list else [fields]


class OrderFilter(QueryFilter):
    precedence = 2

    def __init__(self, field, direction):
        self.field = field
        self.direction = direction


class SkipFilter(QueryFilter):
    precedence = 3

    def __init__(self, skip_value):
        self.skip_value = skip_value


class LimitFilter(QueryFilter):
    precedence = 4

    def __init__(self, limit_value):
        self.limit_value = limit_value


class IncludeFilter(QueryFilter):
    precedence = 5

    def __init__(self, included_filters):
        self.included_filters = included_filters["include"]


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
        for filter in self.filters:
            filter.apply_filter(query)
