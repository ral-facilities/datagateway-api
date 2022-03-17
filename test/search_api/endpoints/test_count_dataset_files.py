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
                # Skipped because empty dict for filter doesn't work on where
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "0-8401-1070-7",
                '{"name": "Datafile 10060"}',
                {"count": 1},
                id="Count dataset files with name condition",
            ),
            pytest.param(
                "0-8401-1070-7",
                '{"name": {"nlike": "Datafile 10060"}}',
                {"count": 55},
                id="Count dataset files with name condition (operator specified)",
            ),
            pytest.param(
                "0-8401-1070-7",
                '{"size": {"gt": 50000000}}',
                {"count": 40},
                id="Count dataset files with size condition",
            ),
            pytest.param(
                "0-8401-1070-7",
                '{"name": "Unknown Datafile"}',
                {"count": 0},
                id="Count dataset files with filter to return zero count",
            ),
            pytest.param(
                "unknown pid",
                "{}",
                {"count": 0},
                id="Non-existent dataset pid",
                # Skipped because empty dict for filter doesn't work on where
                marks=pytest.mark.skip,
            ),
        ],
    )
    def test_valid_count_dataset_files_endpoint(
        self, flask_test_app_search_api, pid, request_filter, expected_json,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/datasets/{pid}/files/count"
            f"?where={request_filter}",
        )

        assert test_response.status_code == 200
        assert test_response.json == expected_json

    @pytest.mark.parametrize(
        "pid, request_filter",
        [
            pytest.param("0-8401-1070-7", '{"bad filter"}', id="Bad filter"),
            pytest.param(
                "0-8401-1070-7",
                '{"where": {"name": "FILE 4"}}',
                id="Where filter inside where query param",
            ),
        ],
    )
    def test_invalid_count_dataset_files_endpoint(
        self, flask_test_app_search_api, pid, request_filter,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/datasets/{pid}/files/count"
            f"?where={request_filter}",
        )

        assert test_response.status_code == 400
