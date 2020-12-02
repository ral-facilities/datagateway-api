from common.filters import (
    WhereFilter,
    DistinctFieldFilter,
    OrderFilter,
    SkipFilter,
    LimitFilter,
    IncludeFilter,
)
from common.exceptions import FilterError, MultipleIncludeError
from common.database import models

from sqlalchemy import asc, desc
import logging

log = logging.getLogger()


class DatabaseWhereFilter(WhereFilter):
    def __init__(self, field, value, operation):
        super().__init__(field, value, operation)

        self.included_field = None
        self.included_included_field = None
        self._extract_filter_fields(field)

    def _extract_filter_fields(self, field):
        """
        Extract the related fields names and put them into separate variables

        :param field: ICAT field names, separated by dots
        :type field: :class:`str`
        """

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

    def apply_filter(self, query):
        try:
            field = getattr(query.table, self.field)
        except AttributeError:
            raise FilterError(
                f"Unknown attribute {self.field} on table {query.table.__name__}"
            )

        if self.included_included_field:
            included_table = getattr(models, self.field)
            included_included_table = getattr(models, self.included_field)
            query.base_query = query.base_query.join(included_table).join(
                included_included_table
            )
            field = getattr(included_included_table, self.included_included_field)

        elif self.included_field:
            included_table = getattr(models, self.field)
            query.base_query = query.base_query.join(included_table)
            field = getattr(included_table, self.included_field)

        if self.operation == "eq":
            query.base_query = query.base_query.filter(field == self.value)
        elif self.operation == "ne":
            query.base_query = query.base_query.filter(field != self.value)
        elif self.operation == "like":
            query.base_query = query.base_query.filter(field.like(f"%{self.value}%"))
        elif self.operation == "lt":
            query.base_query = query.base_query.filter(field < self.value)
        elif self.operation == "lte":
            query.base_query = query.base_query.filter(field <= self.value)
        elif self.operation == "gt":
            query.base_query = query.base_query.filter(field > self.value)
        elif self.operation == "gte":
            query.base_query = query.base_query.filter(field >= self.value)
        elif self.operation == "in":
            query.base_query = query.base_query.filter(field.in_(self.value))
        else:
            raise FilterError(
                f" Bad operation given to where filter. operation: {self.operation}"
            )


class DatabaseDistinctFieldFilter(DistinctFieldFilter):
    def __init__(self, fields):
        super().__init__(fields)

    def apply_filter(self, query):
        query.is_distinct_fields_query = True
        try:
            self.fields = [getattr(query.table, field) for field in self.fields]
        except AttributeError:
            raise FilterError("Bad field requested")
        query.base_query = query.session.query(*self.fields).distinct()


class DatabaseOrderFilter(OrderFilter):
    def __init__(self, field, direction):
        super().__init__(field, direction)

    def apply_filter(self, query):
        if self.direction.upper() == "ASC":
            query.base_query = query.base_query.order_by(asc(self.field.upper()))
        elif self.direction.upper() == "DESC":
            query.base_query = query.base_query.order_by(desc(self.field.upper()))
        else:
            raise FilterError(f" Bad filter: {self.direction}")


class DatabaseSkipFilter(SkipFilter):
    def __init__(self, skip_value):
        super().__init__(skip_value)

    def apply_filter(self, query):
        query.base_query = query.base_query.offset(self.skip_value)


class DatabaseLimitFilter(LimitFilter):
    def __init__(self, limit_value):
        self.limit_value = limit_value

    def apply_filter(self, query):
        query.base_query = query.base_query.limit(self.limit_value)


class DatabaseIncludeFilter(IncludeFilter):
    def __init__(self, included_filters):
        super().__init__(included_filters)

    def apply_filter(self, query):
        if not query.include_related_entities:
            query.include_related_entities = True
        else:
            raise MultipleIncludeError()
