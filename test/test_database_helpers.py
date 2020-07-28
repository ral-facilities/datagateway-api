from unittest import TestCase

#from common.filters import QueryFilterFactory
from common.database_helpers import OrderFilter, LimitFilter, SkipFilter, WhereFilter, \
    IncludeFilter, DistinctFieldFilter, QueryFilterFactory


class TestQueryFilterFactory(TestCase):
    def test_order_filter(self):
        self.assertIs(OrderFilter, type(QueryFilterFactory.get_query_filter({"order": "ID DESC"})))

    def test_limit_filter(self):
        self.assertIs(LimitFilter, type(QueryFilterFactory.get_query_filter({"limit": 10})))

    def test_skip_filter(self):
        self.assertIs(SkipFilter, type(QueryFilterFactory.get_query_filter({"skip": 10})))

    def test_where_filter(self):
        self.assertIs(WhereFilter, type(QueryFilterFactory.get_query_filter({"where": {"ID": {"eq": "1"}}})))
        self.assertIs(WhereFilter, type(QueryFilterFactory.get_query_filter({"where": {"ID": {"lte": "1"}}})))
        self.assertIs(WhereFilter, type(QueryFilterFactory.get_query_filter({"where": {"ID": {"gte": "1"}}})))
        self.assertIs(WhereFilter, type(QueryFilterFactory.get_query_filter({"where": {"ID": {"like": "3"}}})))
        self.assertIs(WhereFilter,
                      type(QueryFilterFactory.get_query_filter({"where": {"ID": {"in": ["1", "2", "3"]}}})))

    def test_include_filter(self):
        self.assertIs(IncludeFilter, type(QueryFilterFactory.get_query_filter({"include": "DATAFILE"})))
        self.assertIs(IncludeFilter, type(QueryFilterFactory.get_query_filter({"include": ["TEST"]})))
        self.assertIs(IncludeFilter,
                      type(QueryFilterFactory.get_query_filter({"include": {"Test": ["TEST1", "Test2"]}})))

    def test_distinct_filter(self):
        self.assertIs(DistinctFieldFilter, type(QueryFilterFactory.get_query_filter({"distinct": "TEST"})))
