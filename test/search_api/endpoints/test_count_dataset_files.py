import pytest

from datagateway_api.src.common.config import Config


class TestSearchAPICountDatasetFilesEndpoint:
    @pytest.mark.parametrize(
        "pid, request_filter, expected_json",
        [
            pytest.param(
                "0-8401-1070-7",
                "{}",
                {"count": 56},
                id="Basic /datasets/{pid}/files/count request",
            ),
        ],
    )
    def test_valid_count_dataset_files_endpoint(
        self, flask_test_app_search_api, pid, request_filter, expected_json,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/datasets/{pid}/files/count"
            f"?filter={request_filter}",
        )

        print(test_response)
        print(test_response.json)

        assert test_response.status_code == 200
        assert test_response.json == expected_json

    def test_invalid_count_dataset_files_endpoint(self):
        # TODO - test for bad filter (where only)
        pass
