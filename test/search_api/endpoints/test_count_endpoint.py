from unittest.mock import patch

import pytest

from datagateway_api.src.common.config import Config
from datagateway_api.src.common.date_handler import DateHandler


class TestSearchAPICountEndpoint:
    @pytest.mark.parametrize(
        "endpoint_name, request_filter, expected_json",
        [
            pytest.param(
                "datasets", "{}", {"count": 479}, id="Basic /datasets/count request",
            ),
            pytest.param(
                "documents", "{}", {"count": 239}, id="Basic /documents/count request",
            ),
            pytest.param(
                "instruments",
                "{}",
                {"count": 14},
                id="Basic /instruments/count request",
            ),
            pytest.param(
                "datasets",
                '{"title": "DATASET 30"}',
                {"count": 1},
                id="Dataset count with basic where",
            ),
            pytest.param(
                "documents",
                '{"title": "INVESTIGATION 2"}',
                {"count": 1},
                id="Document count with basic where",
            ),
            pytest.param(
                "instruments",
                '{"name": "INSTRUMENT 12"}',
                {"count": 1},
                id="Instrument count with basic where",
            ),
            pytest.param(
                "datasets",
                '{"title": {"like": "DATASET 30"}}',
                {"count": 11},
                id="Dataset count with where (operator specified)",
            ),
            pytest.param(
                "documents",
                '{"summary": {"ilike": "nature"}}',
                {"count": 7},
                id="Document count with where (operator specified)",
            ),
            pytest.param(
                "instruments",
                '{"name": {"nilike": "INSTRUMENT 5"}}',
                {"count": 13},
                id="Instrument count with where (operator specified)",
            ),
            pytest.param(
                "instruments",
                '{"facility": {"like": "LILS"}}',
                {"count": 14},
                id="Instrument count with where using related ICAT mapping",
            ),
        ],
    )
    def test_valid_count_endpoint(
        self, flask_test_app_search_api, endpoint_name, request_filter, expected_json,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/{endpoint_name}/count?where="
            f"{request_filter}",
        )

        assert test_response.status_code == 200
        assert test_response.json == expected_json

    @pytest.mark.parametrize(
        "endpoint_name, request_filter, expected_json",
        [
            pytest.param(
                "datasets",
                '{"isPublic": true}',
                {"count": 462},
                id="Dataset count with isPublic condition",
            ),
            pytest.param(
                "documents",
                '{"isPublic": true}',
                {"count": 76},
                id="Document count with isPublic condition",
            ),
        ],
    )
    @patch("datagateway_api.src.search_api.query_filter_factory.datetime")
    def test_valid_count_endpoint_is_public_field(
        self,
        datetime_mock,
        flask_test_app_search_api,
        endpoint_name,
        request_filter,
        expected_json,
    ):
        """
        The datetime must be mocked here to prevent tests from failing as time passes.
        A dataset or document that was created or released 2 years and 364 ago would be
        fall in the not public category, however that same dataset or document would
        fall in the public category (in the case of ISIS) a few days later because it
        will be 3 years old. As a result of this, the tests will fail because the actual
        count will be different to that of the expected. Mocking datetime takes care of
        this issue because it sets the time to the one provided in this test method.
        """
        datetime_mock.now.return_value = DateHandler.str_to_datetime_object(
            "2022-02-06 00:00:01+00:00",
        )
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/{endpoint_name}/count?where="
            f"{request_filter}",
        )

        assert test_response.status_code == 200
        assert test_response.json == expected_json

    @pytest.mark.parametrize(
        "request_filter",
        [
            pytest.param('{"bad filter"}', id="Bad filter"),
            pytest.param(
                '{"where": {"title": "DATASET 4"}}',
                id="Where filter inside where query param",
            ),
        ],
    )
    def test_invalid_count_endpoint(
        self, flask_test_app_search_api, request_filter,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/datasets/count"
            f"?where={request_filter}",
        )

        assert test_response.status_code == 400
