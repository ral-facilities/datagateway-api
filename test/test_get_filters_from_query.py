import pytest

from datagateway_api.src.common.exceptions import ApiError, FilterError
from datagateway_api.src.common.helpers import get_filters_from_query_string
from datagateway_api.src.datagateway_api.database.filters import (
    DatabaseDistinctFieldFilter,
    DatabaseIncludeFilter,
    DatabaseLimitFilter,
    DatabaseOrderFilter,
    DatabaseSkipFilter,
)


class TestGetFiltersFromQueryString:
    def test_valid_no_filters(self, flask_test_app_db):
        with flask_test_app_db:
            flask_test_app_db.get("/")

            assert [] == get_filters_from_query_string("datagateway_api")

    def test_invalid_filter(self, flask_test_app_db):
        with flask_test_app_db:
            flask_test_app_db.get('/?test="test"')

            with pytest.raises(FilterError):
                get_filters_from_query_string("datagateway_api")

    @pytest.mark.parametrize(
        "filter_input, filter_type",
        [
            pytest.param(
                'distinct="id"', DatabaseDistinctFieldFilter, id="DB distinct filter",
            ),
            pytest.param(
                'include="TEST"', DatabaseIncludeFilter, id="DB include filter",
            ),
            pytest.param("limit=10", DatabaseLimitFilter, id="DB limit filter"),
            pytest.param('order="id DESC"', DatabaseOrderFilter, id="DB order filter"),
            pytest.param("skip=10", DatabaseSkipFilter, id="DB skip filter"),
        ],
    )
    def test_valid_filter(self, flask_test_app_db, filter_input, filter_type):
        with flask_test_app_db:
            flask_test_app_db.get(f"/?{filter_input}")
            filters = get_filters_from_query_string("datagateway_api")

            assert isinstance(filters[0], filter_type)

    def test_valid_multiple_filters(self, flask_test_app_db):
        with flask_test_app_db:
            flask_test_app_db.get("/?limit=10&skip=4")
            filters = get_filters_from_query_string("datagateway_api")

            assert len(filters) == 2

    def test_valid_search_api_filter(self, flask_test_app_db):
        with flask_test_app_db:
            flask_test_app_db.get('/?filter={"skip": 5, "limit": 10}')

            filters = get_filters_from_query_string("search_api", "Dataset")

            assert len(filters) == 2

    def test_invalid_api_type(self):
        with pytest.raises(ApiError):
            get_filters_from_query_string("unknown_api")
