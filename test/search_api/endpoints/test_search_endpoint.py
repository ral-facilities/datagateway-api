import pytest

from datagateway_api.src.common.config import Config


class TestSearchAPISearchEndpoint:
    @pytest.mark.parametrize(
        "endpoint_name, request_filter, expected_json",
        [
            pytest.param(
                "datasets",
                '{"limit": 2}',
                [
                    {
                        "pid": "0-449-78690-0",
                        "title": "DATASET 1",
                        "creationDate": "2002-11-27T06:20:36+00:00",
                        "size": None,
                        "documents": [],
                        "techniques": [],
                        "instrument": None,
                        "files": [],
                        "parameters": [],
                        "samples": [],
                    },
                    {
                        "pid": "0-8401-1070-7",
                        "title": "DATASET 2",
                        "creationDate": "2013-04-01T10:56:52+00:00",
                        "size": None,
                        "documents": [],
                        "techniques": [],
                        "instrument": None,
                        "files": [],
                        "parameters": [],
                        "samples": [],
                    },
                ],
                id="Basic /datasets request",
            ),
            pytest.param(
                "documents", '{"limit": 2}', [{}, {}], id="Basic /documents request",
            ),
            # TODO - test data will need changing once facility has been fixed
            pytest.param(
                "instruments",
                '{"limit": 2}',
                [
                    {"pid": 1, "name": "INSTRUMENT 1", "datasets": None},
                    {"pid": 2, "name": "INSTRUMENT 2", "datasets": None},
                ],
                id="Basic /instruments request",
            ),
        ],
    )
    def test_valid_search_endpoint(
        self, flask_test_app_search_api, endpoint_name, request_filter, expected_json,
    ):
        print(f"RF: {request_filter}")
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/{endpoint_name}?filter="
            f"{request_filter}",
        )
        print(test_response)
        print(test_response.json)

        assert test_response.json == expected_json

    def test_invalid_search_endpoint(self):
        # TODO - test for bad filters
        pass
