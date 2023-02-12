from datagateway_api.src.common.base_query_filter_factory import QueryFilterFactory


class TestBaseQueryFilterFactory:
    def test_abstract_class(self):
        QueryFilterFactory.__abstractmethods__ = set()

        class DummyQueryFilterFactory(QueryFilterFactory):
            pass

        d = DummyQueryFilterFactory()

        request_filter = "request_filter"

        assert d.get_query_filter(request_filter) is None
