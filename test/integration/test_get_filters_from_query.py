from fastapi import Request
import pytest

from datagateway_api.src.common.helpers import get_filters_from_query_string
from datagateway_api.src.datagateway_api.icat.filters import (
    PythonICATDistinctFieldFilter,
    PythonICATIncludeFilter,
    PythonICATLimitFilter,
    PythonICATOrderFilter,
    PythonICATSkipFilter,
)


class TestGetFiltersFromQueryString:
    def test_valid_no_filters(self, test_client):
        app = test_client.app

        @app.get("/")
        def test_filters_route(request: Request):
            filters = get_filters_from_query_string(request, "datagateway_api")
            assert filters == []

    @pytest.mark.parametrize(
        "filter_input, filter_type",
        [
            pytest.param(
                'distinct="id"',
                PythonICATDistinctFieldFilter,
                id="DB distinct filter",
            ),
            pytest.param(
                'include="TEST"',
                PythonICATIncludeFilter,
                id="DB include filter",
            ),
            pytest.param("limit=10", PythonICATLimitFilter, id="DB limit filter"),
            pytest.param(
                'order="id DESC"',
                PythonICATOrderFilter,
                id="DB order filter",
            ),
            pytest.param("skip=10", PythonICATSkipFilter, id="DB skip filter"),
        ],
    )
    def test_valid_filter(self, test_client, filter_input, filter_type):
        with test_client:
            app = test_client.app

            @app.get(f"/test-filters?{filter_input}")
            def test_filters_route(request: Request):
                filters = get_filters_from_query_string(request, "datagateway_api")
                assert isinstance(filters[0], filter_type)

    def test_valid_multiple_filters(self, test_client):
        with test_client:
            app = test_client.app

            @app.get("/?limit=10&skip=4")
            def test_filters_route(request: Request):
                filters = get_filters_from_query_string(request, "datagateway_api")
                assert len(filters) == 2

    def test_valid_search_api_filter(self, test_client):
        with test_client:
            app = test_client.app

            @app.get('/?filter={"skip": 5, "limit": 10}')
            def test_filters_route(request: Request):
                filters = get_filters_from_query_string(request, "search_api", "Dataset")
                assert len(filters) == 2
