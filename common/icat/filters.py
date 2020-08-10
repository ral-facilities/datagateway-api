import logging

from common.filters import WhereFilter, DistinctFieldFilter, OrderFilter, SkipFilter, LimitFilter, \
    IncludeFilter
from common.exceptions import BadFilterError
from common.icat.helpers import create_condition

log = logging.getLogger()


class PythonICATWhereFilter(WhereFilter):
    def __init__(self, field, value, operation):
        super().__init__(field, value, operation)

    def apply_filter(self, query):
        # Convert the properties into stuff that ICAT will accept
            # Check self.field actually exists within the entity
            # 


        if self.operation == "eq":
            where_filter = create_condition(self.field, '=', [self.value])
        elif self.operation == "like":
            pass
        elif self.operation == "lte":
            where_filter = create_condition(self.field, '<=', [self.value])
        elif self.operation == "gte":
            where_filter = create_condition(self.field, '>=', [self.value])
        elif self.operation == "in":
            log.debug(f"Field: {self.field}, Type: {type(self.field)}, Value: {self.value}, Type: {type(self.value)}")
            where_filter = create_condition(self.field, '=', [self.value])
            log.debug(f"IN Filter: {where_filter}")
        else:
            raise BadFilterError(
                f" Bad operation given to where filter. operation: {self.operation}")

        try:
            query.addConditions(where_filter)
        except ValueError:
            raise BadFilterError()


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
