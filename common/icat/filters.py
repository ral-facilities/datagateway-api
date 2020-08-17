import logging

from common.filters import WhereFilter, DistinctFieldFilter, OrderFilter, SkipFilter, LimitFilter, \
    IncludeFilter
from common.exceptions import FilterError
from common.icat.helpers import create_condition

log = logging.getLogger()


class PythonICATWhereFilter(WhereFilter):
    def __init__(self, field, value, operation):
        super().__init__(field, value, operation)

    def apply_filter(self, query):
        
        if self.operation == "eq":
            where_filter = create_condition(self.field, '=', self.value)
        elif self.operation == "like":
            where_filter = create_condition(self.field, 'like', self.value)
        elif self.operation == "lt":
            where_filter = create_condition(self.field, '<', self.value)
        elif self.operation == "lte":
            where_filter = create_condition(self.field, '<=', self.value)
        elif self.operation == "gt":
            where_filter = create_condition(self.field, '>', self.value)
        elif self.operation == "gte":
            where_filter = create_condition(self.field, '>=', self.value)
        elif self.operation == "in":
            where_filter = create_condition(self.field, 'in', tuple(self.value))
        else:
            raise FilterError(f"Bad operation given to where filter: {self.operation}")

        try:
            query.addConditions(where_filter)
        except ValueError:
            raise FilterError()


class PythonICATDistinctFieldFilter(DistinctFieldFilter):
    def __init__(self, fields):
        super().__init__(fields)

    def apply_filter(self, query):
        pass


class PythonICATOrderFilter(OrderFilter):
    def __init__(self, field, direction):
        super().__init__(field, direction)

    def apply_filter(self, query):
        pass


class PythonICATSkipFilter(SkipFilter):
    def __init__(self, skip_value):
        super().__init__(skip_value)

    def apply_filter(self, query):
        pass


class PythonICATLimitFilter(LimitFilter):
    def __init__(self, limit_value):
        super().__init__(limit_value)

    def apply_filter(self, query):
        pass


class PythonICATIncludeFilter(IncludeFilter):
    def __init__(self, included_filters):
        super().__init__(included_filters)

    def apply_filter(self, query):
        pass
