import pytest

from datagateway_api.common.datagateway_api.database.filters import (
    DatabaseDistinctFieldFilter,
    DatabaseIncludeFilter,
    DatabaseLimitFilter,
    DatabaseOrderFilter,
    DatabaseSkipFilter,
    DatabaseWhereFilter,
)
from datagateway_api.common.datagateway_api.query_filter_factory import (
    QueryFilterFactory,
)


class TestQueryFilterFactory:
    @pytest.mark.usefixtures("flask_test_app_db")
    def test_valid_distinct_filter(self):
        assert isinstance(
            QueryFilterFactory.get_query_filter({"distinct": "TEST"}),
            DatabaseDistinctFieldFilter,
        )

    @pytest.mark.usefixtures("flask_test_app_db")
    @pytest.mark.parametrize(
        "filter_input",
        [
            pytest.param({"include": "DATAFILE"}, id="string"),
            pytest.param({"include": ["TEST"]}, id="list of strings inside dictionary"),
            pytest.param(
                {"include": {"Test": ["TEST1", "Test2"]}},
                id="list of strings inside nested dictionary",
            ),
        ],
    )
    def test_valid_include_filter(self, filter_input):
        assert isinstance(
            QueryFilterFactory.get_query_filter(filter_input), DatabaseIncludeFilter,
        )

    @pytest.mark.usefixtures("flask_test_app_db")
    def test_valid_limit_filter(self):
        assert isinstance(
            QueryFilterFactory.get_query_filter({"limit": 10}), DatabaseLimitFilter,
        )

    @pytest.mark.usefixtures("flask_test_app_db")
    def test_valid_order_filter(self):
        assert isinstance(
            QueryFilterFactory.get_query_filter({"order": "id DESC"}),
            DatabaseOrderFilter,
        )

    @pytest.mark.usefixtures("flask_test_app_db")
    def test_valid_skip_filter(self):
        assert isinstance(
            QueryFilterFactory.get_query_filter({"skip": 10}), DatabaseSkipFilter,
        )

    @pytest.mark.usefixtures("flask_test_app_db")
    @pytest.mark.parametrize(
        "filter_input",
        [
            pytest.param({"where": {"id": {"eq": "1"}}}, id="eq operator"),
            pytest.param({"where": {"id": {"gt": "1"}}}, id="gt operator"),
            pytest.param({"where": {"id": {"gte": "1"}}}, id="gte operator"),
            pytest.param({"where": {"id": {"in": ["1", "2", "3"]}}}, id="in operator"),
            pytest.param({"where": {"id": {"like": "3"}}}, id="like operator"),
            pytest.param({"where": {"id": {"nlike": "3"}}}, id="not like operator"),
            pytest.param({"where": {"id": {"lt": "1"}}}, id="lt operator"),
            pytest.param({"where": {"id": {"lte": "1"}}}, id="lte operator"),
        ],
    )
    def test_valid_where_filter(self, filter_input):
        assert isinstance(
            QueryFilterFactory.get_query_filter(filter_input), DatabaseWhereFilter,
        )
