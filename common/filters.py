from abc import ABC, abstractmethod
import logging

from common.exceptions import BadRequestError

log = logging.getLogger()


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
        # The field is set to None as a precaution but this should be set by the
        # individual backend since backends deal with this data differently
        self.field = None
        self.value = value
        self.operation = operation

        if self.operation == "in":
            if not isinstance(self.value, list):
                raise BadRequestError(
                    "When using the 'in' operation for a WHERE filter, the values must"
                    " be in a list format e.g. [1, 2, 3]"
                )


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
