import logging

from common.filters import (
    WhereFilter,
    DistinctFieldFilter,
    OrderFilter,
    SkipFilter,
    LimitFilter,
    IncludeFilter,
)
from common.exceptions import FilterError
from common.config import config
from common.constants import Constants

log = logging.getLogger()


class PythonICATWhereFilter(WhereFilter):
    def __init__(self, field, value, operation):
        super().__init__(field, value, operation)

    def apply_filter(self, query):
        log.info("Creating condition for ICAT where filter")
        if self.operation == "eq":
            where_filter = self.create_condition(self.field, "=", self.value)
        elif self.operation == "ne":
            where_filter = self.create_condition(self.field, "!=", self.value)
        elif self.operation == "like":
            where_filter = self.create_condition(self.field, "like", f"%{self.value}%")
        elif self.operation == "lt":
            where_filter = self.create_condition(self.field, "<", self.value)
        elif self.operation == "lte":
            where_filter = self.create_condition(self.field, "<=", self.value)
        elif self.operation == "gt":
            where_filter = self.create_condition(self.field, ">", self.value)
        elif self.operation == "gte":
            where_filter = self.create_condition(self.field, ">=", self.value)
        elif self.operation == "in":
            # Convert self.value into a string with brackets equivalent to tuple format.
            # Cannot convert straight to tuple as single element tuples contain a
            # trailing comma which Python ICAT/JPQL doesn't accept
            self.value = str(self.value).replace("[", "(").replace("]", ")")
            where_filter = self.create_condition(self.field, "in", self.value)
        else:
            raise FilterError(f"Bad operation given to where filter: {self.operation}")

        log.debug("ICAT Where Filter: %s", where_filter)
        try:
            log.info("Adding ICAT where filter to query")
            query.addConditions(where_filter)
        except ValueError:
            raise FilterError(
                "Something went wrong when adding WHERE filter to ICAT query"
            )

    @staticmethod
    def create_condition(attribute_name, operator, value):
        """
        Construct and return a Python dictionary containing conditions to be used in a
        Query object

        :param attribute_name: Attribute name to search
        :type attribute_name: :class:`str`
        :param operator: Operator to use when filtering the data
        :type operator: :class:`str`
        :param value: What ICAT will use to filter the data
        :type value: :class:`str` or :class:`tuple` (when using an IN expression)
        :return: Condition (of type :class:`dict`) ready to be added to a Python ICAT
            Query object
        """

        conditions = {}
        # Removing quote marks when doing conditions with IN expressions or when a
        # distinct filter is used in a request
        jpql_value = (
            f"{value}" if operator == "in" or operator == "!=" else f"'{value}'"
        )
        conditions[attribute_name] = f"{operator} {jpql_value}"
        log.debug("Conditions in ICAT where filter, %s", conditions)
        return conditions


class PythonICATDistinctFieldFilter(DistinctFieldFilter):
    def __init__(self, fields):
        super().__init__(fields)

    def apply_filter(self, query):
        try:
            log.info("Adding ICAT distinct filter to ICAT query")
            query.setAggregate("DISTINCT")

            # Using where filters to identify which fields to apply distinct too
            for field in self.fields:
                where_filter = PythonICATWhereFilter(field, "null", "ne")
                where_filter.apply_filter(query)

            log.debug("Fields for distinct filter: %s", self.fields)
        except ValueError as e:
            raise FilterError(e)


class PythonICATOrderFilter(OrderFilter):
    # Used to append the order tuples across all filters in a single request
    result_order = []

    def __init__(self, field, direction):
        # Python ICAT doesn't automatically uppercase the direction, errors otherwise
        super().__init__(field, direction.upper())

    def apply_filter(self, query):
        PythonICATOrderFilter.result_order.append((self.field, self.direction))
        log.debug("Result Order: %s", PythonICATOrderFilter.result_order)

        try:
            log.info("Adding order filter")
            query.setOrder(PythonICATOrderFilter.result_order)
        except ValueError as e:
            # Typically either invalid attribute(s) or attribute(s) contains 1-many
            # relationship
            raise FilterError(e)


class PythonICATSkipFilter(SkipFilter):
    def __init__(self, skip_value):
        super().__init__(skip_value)

    def apply_filter(self, query):
        icat_properties = Constants.ICAT_PROPERTIES
        icat_set_limit(query, self.skip_value, icat_properties["maxEntities"])


class PythonICATLimitFilter(LimitFilter):
    def __init__(self, limit_value):
        super().__init__(limit_value)
        self.skip_value = 0

    def apply_filter(self, query):
        icat_set_limit(query, self.skip_value, self.limit_value)


def icat_set_limit(query, skip_number, limit_number):
    """
    Add limit (utilising skip and count) to an ICAT query

    :param query: ICAT Query object to execute within Python ICAT
    :type query: :class:`icat.query.Query`
    :param skip_number: Number of results to skip
    :type skip_number: :class:`int`
    :param limit_number: Number of results to limit in the query
    :type limit_number: :class:`int`
    :raises FilterError: If the tuple is not of two elements, or the elements aren't of
        the valid type
    """
    try:
        query.setLimit((skip_number, limit_number))
    except TypeError as e:
        # Not a two element tuple as managed by Python ICAT's setLimit()
        raise FilterError(e)


class PythonICATIncludeFilter(IncludeFilter):
    def __init__(self, included_filters):
        super().__init__(included_filters)

    def apply_filter(self, query):
        pass
