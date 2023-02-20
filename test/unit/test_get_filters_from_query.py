import pytest

from datagateway_api.src.common.exceptions import ApiError
from datagateway_api.src.common.helpers import get_filters_from_query_string


class TestGetFiltersFromQueryString:
    def test_invalid_api_type(self):
        with pytest.raises(ApiError):
            get_filters_from_query_string("unknown_api")
