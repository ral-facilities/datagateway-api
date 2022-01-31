from icat.query import Query


class ConditionSettingQuery(Query):
    """
    Custom Query class to support the getting and setting of WHERE clauses outside of
    the typical `Query.conditions` dict
    """

    def __init__(
        self,
        client,
        entity_name,
        conditions=None,
        aggregate=None,
        includes=None,
        str_conditions="",
    ):

        super().__init__(
            client,
            entity_name,
            conditions=conditions,
            aggregate=aggregate,
            includes=includes,
        )
        self.setConditionsByString(str_conditions)

    def setConditionsByString(self, str_conditions):  # noqa: N802
        self._str_conditions = str_conditions

    @property
    def where_clause(self):
        """
        Overriding Python ICAT's implementation to support the creation of WHERE clauses
        within the search API
        """

        if self._str_conditions:
            return f"WHERE {self._str_conditions}"
        else:
            return super().where_clause
