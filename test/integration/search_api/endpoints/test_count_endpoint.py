import pytest

from datagateway_api.src.common.config import Config


class TestSearchAPICountEndpoint:
    @pytest.mark.parametrize(
        "endpoint_name, request_filter, expected_json",
        [
            pytest.param(
                "Datasets",
                "{}",
                {"count": 479},
                id="Basic /Datasets/count request",
                # Skipped because empty dict for filter doesn't work on where
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "Documents",
                "{}",
                {"count": 239},
                id="Basic /Documents/count request",
                # Skipped because empty dict for filter doesn't work on where
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "Instruments",
                "{}",
                {"count": 14},
                id="Basic /Instruments/count request",
                # Skipped because empty dict for filter doesn't work on where
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "Datasets",
                '{"title": "DATASET 30"}',
                {"count": 1},
                id="Dataset count with basic where",
            ),
            pytest.param(
                "Documents",
                '{"title": "INVESTIGATION 2"}',
                {"count": 1},
                id="Document count with basic where",
            ),
            pytest.param(
                "Instruments",
                '{"name": "INSTRUMENT 12"}',
                {"count": 1},
                id="Instrument count with basic where",
            ),
            pytest.param(
                "Datasets",
                '{"title": {"like": "DATASET 3"}}',
                {"count": 11},
                id="Dataset count with where (operator specified)",
            ),
            pytest.param(
                "Documents",
                '{"summary": {"ilike": "nature"}}',
                {"count": 1},
                id="Document count with where (operator specified)",
            ),
            pytest.param(
                "Instruments",
                '{"name": {"nilike": "INSTRUMENT 5"}}',
                {"count": 13},
                id="Instrument count with where (operator specified)",
            ),
            pytest.param(
                "Instruments",
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
                "Datasets",
                '{"isPublic": true}',
                {"count": 119},
                id="Dataset count with isPublic condition (True)",
            ),
            pytest.param(
                "Documents",
                '{"isPublic": true}',
                {"count": 59},
                id="Document count with isPublic condition (True)",
            ),
            pytest.param(
                "Datasets",
                '{"isPublic": false}',
                {"count": 0},
                id="Dataset count with isPublic condition (False)",
                # Skipped due to skip filter causing issue on count endpoints
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "Documents",
                '{"isPublic": false}',
                {"count": 0},
                id="Document count with isPublic condition (False)",
                # Skipped due to skip filter causing issue on count endpoints
                marks=pytest.mark.skip,
            ),
        ],
    )
    def test_valid_count_endpoint_is_public_field(
        self, flask_test_app_search_api, endpoint_name, request_filter, expected_json,
    ):
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
            f"{Config.config.search_api.extension}/Datasets/count"
            f"?where={request_filter}",
        )

        assert test_response.status_code == 400
