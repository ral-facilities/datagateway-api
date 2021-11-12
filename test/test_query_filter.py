from unittest.mock import patch

import pytest

from datagateway_api.src.datagateway_api.query_filter_factory import QueryFilterFactory
from datagateway_api.src.common.exceptions import ApiError
from datagateway_api.src.common.filters import QueryFilter


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
        with patch(
            "datagateway_api.src.common.config.config.get_config_value",
            return_value="invalid_backend",
        ):
            with pytest.raises(ApiError):
                QueryFilterFactory.get_query_filter({"order": "id DESC"})
