from abc import ABC, abstractmethod
import logging

from datagateway_api.src.common.exceptions import BadRequestError, FilterError

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

        if self.operation in ["in", "nin", "inq", "between"]:
            if not isinstance(self.value, list):
                raise BadRequestError(
                    f"When using the {self.operation} operation for a WHERE filter, the"
                    f" values must be in a list format e.g. [1, 2]",
                )
            if self.operation == "between" and len(self.value) != 2:
                raise BadRequestError(
                    "When using the 'between' operation for a WHERE filter, the list"
                    "must contain two values e.g. [1, 2]",
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
        if skip_value >= 0:
            self.skip_value = skip_value
        else:
            raise FilterError("The value of the skip filter must be positive")


class LimitFilter(QueryFilter):
    precedence = 4

    def __init__(self, limit_value):
        if limit_value >= 0:
            self.limit_value = limit_value
        else:
            raise FilterError("The value of the limit filter must be positive")


class IncludeFilter(QueryFilter):
    precedence = 5

    def __init__(self, included_filters):
        self.included_filters = included_filters
