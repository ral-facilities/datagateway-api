import logging

from sqlalchemy import asc, desc

from datagateway_api.common.database import models
from datagateway_api.common.exceptions import FilterError, MultipleIncludeError
from datagateway_api.common.filters import (
    DistinctFieldFilter,
    IncludeFilter,
    LimitFilter,
    OrderFilter,
    SkipFilter,
    WhereFilter,
)
from datagateway_api.common.helpers import get_entity_object_from_name


log = logging.getLogger()


class DatabaseFilterUtilities:
    """
    Class containing utility functions used in the WhereFilter and DistinctFilter

    In this class, the terminology of 'included entities' has been made more generic to
    'related entities'. When these functions are used with the WhereFilter, the related
    entities are in fact included entities (entities which are also present in the input
    of an include filter in the same request). However, when these functions are used
    with the DistinctFilter, they are related entities, not included entities as there's
    no requirement for the entity names to also be present in an include filter (this is
    to match the ICAT backend)
    """

    def __init__(self):
        self.related_field = None
        self.related_related_field = None

    def _extract_filter_fields(self, field):
        """
        Extract the related fields names and put them into separate variables

        :param field: ICAT field names, separated by dots
        :type field: :class:`str`
        :raises ValueError: If the maximum related/included depth is exceeded
        """

        fields = field.split(".")
        related_depth = len(fields)

        log.debug("Fields: %s, Related Depth: %d", fields, related_depth)

        if related_depth == 1:
            self.field = fields[0]
        elif related_depth == 2:
            self.field = fields[0]
            self.related_field = fields[1]
        elif related_depth == 3:
            self.field = fields[0]
            self.related_field = fields[1]
            self.related_related_field = fields[2]
        else:
            raise ValueError(f"Maximum related depth exceeded. {field}'s depth > 3")

        # TODO - Remove if not needed
        # return (field, related_field, related_related_field)

    def _add_query_join(self, query):
        """
        Fetches the appropriate entity model based on the contents of `self.field` and
        adds any required JOINs to the query if any related fields have been used in the
        filter

        :param query: The query to have filters applied to
        :type query: :class:`datagateway_api.common.database.helpers.[QUERY]`
        :return: Entity model of the field (usually the field relating to the endpoint
            the request is coming from)
        """
        try:
            field = getattr(query.table, self.field)
        except AttributeError:
            raise FilterError(
                f"Unknown attribute {self.field} on table {query.table.__name__}",
            )

        if self.related_related_field:
            included_table = getattr(models, self.field)
            included_included_table = getattr(models, self.related_field)
            query.base_query = query.base_query.join(included_table).join(
                included_included_table,
            )
            field = getattr(included_included_table, self.related_related_field)
        elif self.related_field:
            included_table = get_entity_object_from_name(self.field)
            query.base_query = query.base_query.join(included_table)
            field = getattr(included_table, self.related_field)

        return field


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
                f"Unknown attribute {self.field} on table {query.table.__name__}",
            )

        if self.included_included_field:
            included_table = getattr(models, self.field)
            included_included_table = getattr(models, self.included_field)
            query.base_query = query.base_query.join(included_table).join(
                included_included_table,
            )
            field = getattr(included_included_table, self.included_included_field)
        elif self.included_field:
            included_table = get_entity_object_from_name(self.field)
            query.base_query = query.base_query.join(included_table)
            field = getattr(included_table, self.included_field)

        if self.operation == "eq":
            query.base_query = query.base_query.filter(field == self.value)
        elif self.operation == "ne":
            query.base_query = query.base_query.filter(field != self.value)
        elif self.operation == "like":
            query.base_query = query.base_query.filter(field.like(f"%{self.value}%"))
        elif self.operation == "nlike":
            query.base_query = query.base_query.filter(field.notlike(f"%{self.value}%"))
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
                f" Bad operation given to where filter. operation: {self.operation}",
            )


class DatabaseDistinctFieldFilter(DistinctFieldFilter, DatabaseFilterUtilities):
    def __init__(self, fields):
        # TODO - what's the Pythonic solution here?
        # super().__init__(fields)
        DistinctFieldFilter.__init__(self, fields)
        DatabaseFilterUtilities.__init__(self)

    def apply_filter(self, query):
        query.is_distinct_fields_query = True
        try:
            distinct_fields = []
            for field_name in self.fields:
                self._extract_filter_fields(field_name)
                field = self._add_query_join(query)
                distinct_fields.append(field)
        except AttributeError:
            raise FilterError("Bad field requested")
        query.base_query = query.session.query(*distinct_fields).distinct()


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
