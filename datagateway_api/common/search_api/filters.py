from datagateway_api.common.datagateway_api.icat.filters import (
    PythonICATIncludeFilter,
    PythonICATLimitFilter,
    PythonICATSkipFilter,
    PythonICATWhereFilter,
)

# TODO - Implement each of these filters for Search API, inheriting from the Python ICAT
# versions


class SearchAPIWhereFilter(PythonICATWhereFilter):
    def __init__(self, field, value, operation, boolean_operator="and"):
        super().__init__(field, value, operation)
        self.boolean_operator = boolean_operator

    def apply_filter(self, query):
        return super().apply_filter(query)


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
