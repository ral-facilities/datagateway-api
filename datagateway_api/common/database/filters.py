import logging

from sqlalchemy import asc, desc

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
        """
        The `distinct_join_flag` tracks if JOINs need to be added to the query - on a
        distinct filter, if there's no unrelated fields (i.e. no fields with a
        `related_depth` of 1), adding JOINs to the query (using `_add_query_join()`)
        will result in a `sqlalchemy.exc.InvalidRequestError`
        """
        self.field = None
        self.related_field = None
        self.related_related_field = None
        self.distinct_join_flag = False

    def _extract_filter_fields(self, field):
        """
        Extract the related fields names and put them into separate variables

        :param field: ICAT field names, separated by dots
        :type field: :class:`str`
        :raises ValueError: If the maximum related/included depth is exceeded
        """

        # Flushing fields in case they have been previously set
        self.field = None
        self.related_field = None
        self.related_related_field = None

        fields = field.split(".")
        related_depth = len(fields)

        log.debug("Fields: %s, Related Depth: %d", fields, related_depth)

        if related_depth == 1:
            self.field = fields[0]
            self.distinct_join_flag = True
        elif related_depth == 2:
            self.field = fields[0]
            self.related_field = fields[1]
        elif related_depth == 3:
            self.field = fields[0]
            self.related_field = fields[1]
            self.related_related_field = fields[2]
        else:
            raise ValueError(f"Maximum related depth exceeded. {field}'s depth > 3")

    def _add_query_join(self, query):
        """
        Adds any required JOINs to the query if any related fields have been used in the
        filter

        :param query: The query to have filters applied to
        :type query: :class:`datagateway_api.common.database.helpers.[QUERY]`
        """

        if self.related_related_field:
            included_table = get_entity_object_from_name(self.field)
            included_included_table = get_entity_object_from_name(self.related_field)
            query.base_query = query.base_query.join(included_table).join(
                included_included_table,
            )
        elif self.related_field:
            included_table = get_entity_object_from_name(self.field)
            query.base_query = query.base_query.join(included_table)

    def _get_entity_model_for_filter(self, query):
        """
        Fetches the appropriate entity model based on the contents of the instance
        variables of this class

        :param query: The query to have filters applied to
        :type query: :class:`datagateway_api.common.database.helpers.[QUERY]`
        :return: Entity model of the field (usually the field relating to the endpoint
            the request is coming from)
        """
        if self.related_related_field:
            included_included_table = get_entity_object_from_name(self.related_field)
            field = self._get_field(included_included_table, self.related_related_field)
        elif self.related_field:
            included_table = get_entity_object_from_name(self.field)
            field = self._get_field(included_table, self.related_field)
        else:
            # No related fields
            field = self._get_field(query.table, self.field)

        return field

    def _get_field(self, table, field):
        try:
            return getattr(table, field)
        except AttributeError:
            raise FilterError(f"Unknown attribute {field} on table {table.__name__}")


class DatabaseWhereFilter(WhereFilter, DatabaseFilterUtilities):
    def __init__(self, field, value, operation):
        # TODO - Apply any 'pythonic' solution here too
        WhereFilter.__init__(self, field, value, operation)
        DatabaseFilterUtilities.__init__(self)

        self._extract_filter_fields(field)

    def apply_filter(self, query):
        self._add_query_join(query)
        field = self._get_entity_model_for_filter(query)

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
                distinct_fields.append(self._get_entity_model_for_filter(query))

            # Base query must be set to a DISTINCT query before adding JOINs - if these
            # actions are done in the opposite order, the JOINs will overwrite the
            # SELECT multiple and effectively turn the query into a `SELECT *`
            query.base_query = query.session.query(*distinct_fields).distinct()

            if self.distinct_join_flag:
                for field_name in self.fields:
                    self._extract_filter_fields(field_name)
                    self._add_query_join(query)
        except AttributeError:
            raise FilterError("Bad field requested")


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
