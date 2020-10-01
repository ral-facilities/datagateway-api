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
        self.field = None
        self.included_field = None
        self.included_included_field = None
        self._extract_filter_fields(field)

        self.value = value
        self.operation = operation

        if self.operation == "in":
            if not isinstance(self.value, list):
                raise BadRequestError(
                    "When using the 'in' operation for a WHERE filter, the values must"
                    " be in a list format e.g. [1, 2, 3]"
                )

    def _extract_filter_fields(self, field):
        fields = field.split(".")
        include_depth = len(fields)

        log.debug("Fields: %s, Include Depth: %d", fields, include_depth)

        if include_depth == 1:
            self.field = fields[0]
        elif include_depth == 2:
            self.field = fields[0]
            self.included_field = fields[1]
        elif include_depth == 3:
            self.field = fields[0]
            self.included_field = fields[1]
            self.included_included_field = fields[2]
        else:
            raise ValueError(f"Maximum include depth exceeded. {field}'s depth > 3")


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
