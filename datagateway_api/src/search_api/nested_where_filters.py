import logging

from datagateway_api.src.common.filters import WhereFilter
from datagateway_api.src.search_api.filters import SearchAPIWhereFilter

log = logging.getLogger()


class NestedWhereFilters:
    precedence = WhereFilter.precedence

    def __init__(self, lhs, rhs, joining_operator, search_api_query=None):
        """
        Class to represent nested conditions that use different boolean operators e.g.
        `(A OR B) AND (C OR D)`. This works by joining the two conditions with a boolean
        operator

        :param lhs: Left hand side of the condition - either a string condition, WHERE
            filter or instance of this class
        :type lhs: Any class that has `__str__()` implemented, but use cases will be for
            :class:`str` or :class:`SearchAPIWhereFilter` or :class:`NestedWhereFilters`
        :param rhs: Right hand side of the condition - either a string condition, WHERE
            filter or instance of this class
        :type rhs: Any class that has `__str__()` implemented, but use cases will be for
            :class:`str` or :class:`SearchAPIWhereFilter` or :class:`NestedWhereFilters`
        :param joining_operator: Boolean operator used to join the conditions of `lhs`
            `rhs` (e.g. `AND` or `OR`)
        :type joining_operator: :class:`str`
        """

        # Ensure each side is in a list for consistency for string conversion
        if not isinstance(lhs, list):
            lhs = [lhs]
        if not isinstance(rhs, list):
            rhs = [rhs]

        self.lhs = lhs
        self.rhs = rhs
        self.joining_operator = joining_operator
        self.search_api_query = search_api_query
        if self.search_api_query is not None:
            NestedWhereFilters.set_search_api_query(self, search_api_query)

    def apply_filter(self, query):
        query.query.query.setConditionsByString(str(self))

    @staticmethod
    def set_search_api_query(query_filter, search_api_query):
        """
        TODO
        """

        log.debug(
            "Query filter: %s, Search API query: %s",
            repr(query_filter),
            search_api_query,
        )

        if isinstance(query_filter, SearchAPIWhereFilter):
            query_filter.search_api_query = search_api_query
        elif isinstance(query_filter, NestedWhereFilters):
            NestedWhereFilters.set_search_api_query(
                query_filter.lhs, search_api_query,
            )
            NestedWhereFilters.set_search_api_query(
                query_filter.rhs, search_api_query,
            )
        elif isinstance(query_filter, list):
            for where_filter in query_filter:
                NestedWhereFilters.set_search_api_query(
                    where_filter, search_api_query,
                )

    def __str__(self):
        """
        Join the condition on the left with the one on the right with the boolean
        operator
        """
        boolean_algebra_list = [self.lhs, self.rhs]
        try:
            boolean_algebra_list.remove([None])
        except ValueError:
            # If neither side contains `None`, we should continue as normal
            pass

        # If either side contains a list of WHERE filter objects, flatten the conditions
        conditions = [str(m) for n in (i for i in boolean_algebra_list) for m in n]
        operator = f" {self.joining_operator} "

        return f"({operator.join(conditions)})"

    def __repr__(self):
        return (
            f"LHS: {repr(self.lhs)}, RHS: {repr(self.rhs)}, Operator:"
            f" {repr(self.joining_operator)}"
        )
