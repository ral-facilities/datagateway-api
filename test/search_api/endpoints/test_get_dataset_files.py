import pytest

from datagateway_api.src.common.config import Config


class TestSearchAPIGetDatasetFilesEndpoint:
    @pytest.mark.parametrize(
        "pid, request_filter, expected_json",
        [
            pytest.param(
                "0-8401-1070-7",
                '{"limit": 2}',
                [
                    {
                        "id": "1",
                        "name": "Datafile 1",
                        "path": "/hit/consumer/red.jpg",
                        "size": 199643799,
                        "dataset": None,
                    },
                    {
                        "id": "10060",
                        "name": "Datafile 10060",
                        "path": "/the/current/next.jpg",
                        "size": 124327237,
                        "dataset": None,
                    },
                ],
                id="Basic /datasets/{pid}/files request",
            ),
        ],
    )
    def test_valid_get_dataset_files_endpoint(
        self, flask_test_app_search_api, pid, request_filter, expected_json,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/datasets/{pid}/files"
            f"?filter={request_filter}",
        )

        print(test_response)
        print(test_response.json)

        assert test_response.status_code == 200
        assert test_response.json == expected_json

    def test_invalid_get_dataset_files_endpoint(self):
        # TODO - test bad filter and bad pid
        pass
