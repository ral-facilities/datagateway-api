from icat.client import Client
from icat.query import Query

from datagateway_api.src.datagateway_api.icat.filters import (
    PythonICATIncludeFilter,
    PythonICATLimitFilter,
    PythonICATSkipFilter,
    PythonICATWhereFilter,
)

# TODO - Implement each of these filters for Search API, inheriting from the Python ICAT
# versions


class SearchAPIWhereFilter(PythonICATWhereFilter):
    def __init__(self, field, value, operation):
        super().__init__(field, value, operation)

    def apply_filter(self, query):
        return super().apply_filter(query)

    def __str__(self):
        # TODO - replace with `SessionHandler.client` when that work is merged
        client = Client("https://localhost.localdomain:8181", checkCert=False)
        client.login("simple", {"username": "root", "password": "pw"})

        # TODO - can't just hardcode investigation entity. Might need `icat_entity_name`
        # to be passed into init
        query = Query(client, "Investigation")
        query.addConditions(self.create_filter())
        str_conds = query.get_conditions_as_str()

        return str_conds[0]

    def __repr__(self):
        return (
            f"Field: '{self.field}', Value: '{self.value}', Operation:"
            f" '{self.operation}'"
        )


class SearchAPISkipFilter(PythonICATSkipFilter):
    def __init__(self, skip_value):
        super().__init__(skip_value)

    def apply_filter(self, query):
        return super().apply_filter(query)


class SearchAPILimitFilter(PythonICATLimitFilter):
    def __init__(self, limit_value):
        super().__init__(limit_value)

    def apply_filter(self, query):
        return super().apply_filter(query)


class SearchAPIIncludeFilter(PythonICATIncludeFilter):
    def __init__(self, included_filters):
        super().__init__(included_filters)

    def apply_filter(self, query):
        return super().apply_filter(query)
