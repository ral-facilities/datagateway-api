class NestedWhereFilters:
    def __init__(self, lhs, rhs, joining_operator):
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

        self.lhs = str(lhs)
        self.rhs = str(rhs)
        self.joining_operator = joining_operator

    def __str__(self):
        """
        Join the condition on the left with the one on the right with the boolean
        operator
        """
        return f"({self.lhs} {self.joining_operator} {self.rhs})"
