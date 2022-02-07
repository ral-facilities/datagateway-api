import pytest

from datagateway_api.src.common.config import Config


class TestSearchAPICountEndpoint:
    @pytest.mark.parametrize(
        "endpoint_name, request_filter, expected_json",
        [
            pytest.param(
                "datasets",
                "{}",
                {"count": 479},
                id="Basic /datasets/count request",
                # Skipped because empty dict for filter doesn't work on where
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "documents",
                "{}",
                {"count": 239},
                id="Basic /documents/count request",
                # Skipped because empty dict for filter doesn't work on where
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "instruments",
                "{}",
                {"count": 14},
                id="Basic /instruments/count request",
                # Skipped because empty dict for filter doesn't work on where
                marks=pytest.mark.skip,
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
