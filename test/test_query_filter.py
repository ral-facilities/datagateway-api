import pytest

import datagateway_api.common.config as config
from datagateway_api.common.datagateway_api.query_filter_factory import (
    QueryFilterFactory,
)
from datagateway_api.common.exceptions import ApiError
from datagateway_api.common.filters import QueryFilter


class TestQueryFilter:
    def test_abstract_class(self):
        """Test the `QueryFilter` class has all required abstract methods"""

        QueryFilter.__abstractmethods__ = set()

        class DummyQueryFilter(QueryFilter):
            pass

        qf = DummyQueryFilter()

        apply_filter = "apply_filter"

        assert qf.precedence is None
        assert qf.apply_filter(apply_filter) is None

    def test_invalid_query_filter_getter(self):
        config.config.datagateway_api.backend = "invalid_backend"
        with pytest.raises(ApiError):
            QueryFilterFactory.get_query_filter({"order": "id DESC"})
