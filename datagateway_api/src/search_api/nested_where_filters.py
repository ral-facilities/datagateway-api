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

        # Ensure each side is in a list for consistency for string conversion
        if not isinstance(lhs, list):
            lhs = [lhs]
        if not isinstance(rhs, list):
            rhs = [rhs]

        self.lhs = lhs
        self.rhs = rhs
        self.joining_operator = f" {joining_operator} "

    def __str__(self):
        """
        Join the condition on the left with the one on the right with the boolean
        operator
        """
        boolean_algebra_list = [self.lhs, self.rhs]
        try:
            boolean_algebra_list.remove(None)
        except ValueError:
            # If neither side contains `None`, we should continue as normal
            pass

        # If either side contains a list of WHERE filter objects, flatten the conditions
        conditions = [str(m) for n in (i for i in boolean_algebra_list) for m in n]

        return f"({self.joining_operator.join(conditions)})"

    def __repr__(self):
        return f"LHS: {repr(self.lhs)}, RHS: {repr(self.rhs)}, Operator: {repr(self.joining_operator)}"
