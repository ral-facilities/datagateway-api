from datagateway_api.src.common.helpers import get_filters_from_query_string


class TestGetFiltersFromQueryString:
    def test_valid_no_filters(self, flask_test_app_db):
        with flask_test_app_db:
            flask_test_app_db.get("/")

            assert [] == get_filters_from_query_string("datagateway_api")

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
