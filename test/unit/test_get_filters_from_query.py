import pytest
from starlette.datastructures import QueryParams

from datagateway_api.src.common.exceptions import ApiError
from datagateway_api.src.common.helpers import get_filters_from_query_string


# Dummy Request object to mimic FastAPI Request
class DummyRequest:
    def __init__(self, query_dict=None):
        # QueryParams is immutable, dict-like
        self.query_params = QueryParams(query_dict or {})


class TestGetFiltersFromQueryString:
    def test_invalid_api_type(self):
        dummy_request = DummyRequest()
        with pytest.raises(ApiError):
            # Pass the dummy request as first argument
            get_filters_from_query_string(dummy_request, "unknown_api")
