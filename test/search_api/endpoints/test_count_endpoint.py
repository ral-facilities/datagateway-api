import pytest

from datagateway_api.src.common.config import Config


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
        ],
    )
    def test_valid_count_endpoint(
        self, flask_test_app_search_api, endpoint_name, request_filter, expected_json,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/{endpoint_name}/count?filter="
            f"{request_filter}",
        )

        print(test_response)
        print(test_response.json)

        assert test_response.status_code == 200
        assert test_response.json == expected_json

    def test_invalid_count_endpoint(self):
        # TODO - test for bad filter (where only)
        pass
