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
            pytest.param(
                "0-8401-1070-7",
                '{"limit": 1, "skip": 5}',
                [
                    {
                        "id": "11976",
                        "name": "Datafile 11976",
                        "path": "/ahead/article/oil.jpg",
                        "size": 34418452,
                        "dataset": None,
                    },
                ],
                id="Get dataset files with skip",
            ),
            pytest.param(
                "0-8401-1070-7",
                '{"limit": 1, "where": {"name": "Datafile 10060"}}',
                [
                    {
                        "id": "10060",
                        "name": "Datafile 10060",
                        "path": "/the/current/next.jpg",
                        "size": 124327237,
                        "dataset": None,
                    },
                ],
                id="Get dataset files with name condition",
            ),
            pytest.param(
                "0-8401-1070-7",
                '{"limit": 1, "where": {"name": {"nilike": "Datafile 10060"}}}',
                [
                    {
                        "id": "1",
                        "name": "Datafile 1",
                        "path": "/hit/consumer/red.jpg",
                        "size": 199643799,
                        "dataset": None,
                    },
                ],
                id="Get dataset files with name condition (operator specified)",
            ),
            pytest.param(
                "0-8401-1070-7",
                '{"limit": 1, "where": {"size": {"gt": 5000000}}}',
                [
                    {
                        "id": "1",
                        "name": "Datafile 1",
                        "path": "/hit/consumer/red.jpg",
                        "size": 199643799,
                        "dataset": None,
                    },
                ],
                id="Get dataset files with size condition",
            ),
            pytest.param(
                "0-8401-1070-7",
                '{"limit": 1, "where": {"size": {"gt": 50000000000}}}',
                [],
                id="Get dataset files with condition to return empty list",
            ),
            pytest.param(
                "0-8401-1070-7",
                '{"limit": 1, "include": [{"relation": "dataset"}]}',
                [
                    {
                        "id": "1",
                        "name": "Datafile 1",
                        "path": "/hit/consumer/red.jpg",
                        "size": 199643799,
                        "dataset": {
                            "pid": "0-8401-1070-7",
                            "title": "DATASET 2",
                            "isPublic": True,
                            "creationDate": "2013-04-01T10:56:52.000Z",
                            "size": None,
                            "documents": [],
                            "techniques": [],
                            "instrument": None,
                            "files": [],
                            "parameters": [],
                            "samples": [],
                        },
                    },
                ],
                id="Get dataset files with include filter",
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

    @pytest.mark.parametrize(
        "pid, request_filter, expected_status_code",
        [
            pytest.param("0-8401-1070-7", '{"where": []}', 400, id="Bad where filter"),
            pytest.param("0-8401-1070-7", '{"limit": -1}', 400, id="Bad limit filter"),
            pytest.param("0-8401-1070-7", '{"skip": -100}', 400, id="Bad skip filter"),
            pytest.param(
                "0-8401-1070-7", '{"include": ""}', 400, id="Bad include filter",
            ),
            pytest.param(
                "my 404 test pid",
                "{}",
                404,
                id="Non-existent dataset pid",
                # Skipped because this actually returns 200
                marks=pytest.mark.skip,
            ),
        ],
    )
    def test_invalid_get_dataset_files_endpoint(
        self, flask_test_app_search_api, pid, request_filter, expected_status_code,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/datasets/{pid}/files"
            f"?filter={request_filter}",
        )

        assert test_response.status_code == expected_status_code
