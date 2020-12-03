from unittest import TestCase

from datagateway_api.common.config import config
from datagateway_api.common.exceptions import ApiError
from datagateway_api.common.query_filter import QueryFilterFactory

backend_type = config.get_backend_type()
if backend_type == "db":
    from datagateway_api.common.database.filters import (
        DatabaseDistinctFieldFilter as DistinctFieldFilter,
        DatabaseIncludeFilter as IncludeFilter,
        DatabaseLimitFilter as LimitFilter,
        DatabaseOrderFilter as OrderFilter,
        DatabaseSkipFilter as SkipFilter,
        DatabaseWhereFilter as WhereFilter,
    )
elif backend_type == "python_icat":
    # TODO - Adapt these tests for the ICAT implementation of filters
    from datagateway_api.common.icat.filters import (
        PythonICATDistinctFieldFilter as DistinctFieldFilter,
        PythonICATIncludeFilter as IncludeFilter,
        PythonICATLimitFilter as LimitFilter,
        PythonICATOrderFilter as OrderFilter,
        PythonICATSkipFilter as SkipFilter,
        PythonICATWhereFilter as WhereFilter,
    )
else:
    raise ApiError(
        "Cannot select which implementation of filters to import, check the config file"
        " has a valid backend type",
    )


class TestQueryFilterFactory(TestCase):
    def test_order_filter(self):
        self.assertIs(
            OrderFilter,
            type(QueryFilterFactory.get_query_filter({"order": "ID DESC"})),
        )

    def test_limit_filter(self):
        self.assertIs(
            LimitFilter, type(QueryFilterFactory.get_query_filter({"limit": 10})),
        )

    def test_skip_filter(self):
        self.assertIs(
            SkipFilter, type(QueryFilterFactory.get_query_filter({"skip": 10})),
        )

    def test_where_filter(self):
        self.assertIs(
            WhereFilter,
            type(QueryFilterFactory.get_query_filter({"where": {"ID": {"eq": "1"}}})),
        )
        self.assertIs(
            WhereFilter,
            type(QueryFilterFactory.get_query_filter({"where": {"ID": {"lte": "1"}}})),
        )
        self.assertIs(
            WhereFilter,
            type(QueryFilterFactory.get_query_filter({"where": {"ID": {"gte": "1"}}})),
        )
        self.assertIs(
            WhereFilter,
            type(QueryFilterFactory.get_query_filter({"where": {"ID": {"like": "3"}}})),
        )
        self.assertIs(
            WhereFilter,
            type(
                QueryFilterFactory.get_query_filter(
                    {"where": {"ID": {"in": ["1", "2", "3"]}}},
                ),
            ),
        )

    def test_include_filter(self):
        self.assertIs(
            IncludeFilter,
            type(QueryFilterFactory.get_query_filter({"include": "DATAFILE"})),
        )
        self.assertIs(
            IncludeFilter,
            type(QueryFilterFactory.get_query_filter({"include": ["TEST"]})),
        )
        self.assertIs(
            IncludeFilter,
            type(
                QueryFilterFactory.get_query_filter(
                    {"include": {"Test": ["TEST1", "Test2"]}},
                ),
            ),
        )

    def test_distinct_filter(self):
        self.assertIs(
            DistinctFieldFilter,
            type(QueryFilterFactory.get_query_filter({"distinct": "TEST"})),
        )