from fastapi.routing import APIRoute, Mount
import pytest

from datagateway_api.src.common.config import Config
from datagateway_api.src.common.entity_endpoint_dict import endpoints


def collect_routes(app):
    """
    Recursively collect all APIRoute paths and their methods from a FastAPI app,
    including any mounted sub-apps.
    """
    routes = []

    for route in app.routes:
        if isinstance(route, APIRoute):
            routes.append((route.path, route.methods))
        elif isinstance(route, Mount):
            sub_app = route.app
            routes.extend(collect_routes(sub_app))

    return routes


class TestEndpointRules:
    @pytest.mark.parametrize(
        "endpoint_ending, expected_methods",
        [
            pytest.param("/findone", {"GET"}, id="findone"),
            pytest.param("/count", {"GET"}, id="count"),
            pytest.param("/{id_}", {"DELETE", "GET", "PATCH"}, id="id"),
            pytest.param("", {"GET", "PATCH", "POST"}, id="typical endpoints"),
        ],
    )
    def test_entity_endpoints(self, test_client, endpoint_ending, expected_methods):
        routes = [r for r in test_client.app.routes if isinstance(r, APIRoute)]

        for endpoint_entity in endpoints.keys():
            expected_path = f"{Config.config.datagateway_api.extension}/{endpoint_entity.lower()}{endpoint_ending}"

            matching_routes = [r for r in routes if r.path == expected_path]

            assert matching_routes, f"Endpoint not found: {expected_path}"

            actual_methods = set()
            for route in matching_routes:
                actual_methods |= route.methods

            for method in expected_methods:
                assert method in actual_methods

    @pytest.mark.parametrize(
        "endpoint_name, expected_methods",
        [
            pytest.param(
                f"{Config.config.datagateway_api.extension}/sessions",
                {"DELETE", "GET", "POST", "PUT"},
                id="sessions",
            ),
            pytest.param(
                f"{Config.config.datagateway_api.extension}{Config.config.search_api.extension}/Datasets",
                {"GET"},
                id="search-datasets",
            ),
            pytest.param(
                f"{Config.config.datagateway_api.extension}{Config.config.search_api.extension}/Documents",
                {"GET"},
                id="search-documents",
            ),
            pytest.param(
                f"{Config.config.datagateway_api.extension}{Config.config.search_api.extension}/Instruments",
                {"GET"},
                id="search-instruments",
            ),
            pytest.param(
                f"{Config.config.datagateway_api.extension}{Config.config.search_api.extension}/Datasets/{{pid}}",
                {"GET"},
                id="search-single-dataset",
            ),
            pytest.param(
                f"{Config.config.datagateway_api.extension}{Config.config.search_api.extension}/Documents/{{pid}}",
                {"GET"},
                id="search-single-document",
            ),
            pytest.param(
                f"{Config.config.datagateway_api.extension}{Config.config.search_api.extension}/Instruments/{{pid}}",
                {"GET"},
                id="search-single-instrument",
            ),
            pytest.param(
                f"{Config.config.datagateway_api.extension}{Config.config.search_api.extension}/Datasets/count",
                {"GET"},
                id="search-dataset-count",
            ),
            pytest.param(
                f"{Config.config.datagateway_api.extension}{Config.config.search_api.extension}/Documents/count",
                {"GET"},
                id="search-document-count",
            ),
            pytest.param(
                f"{Config.config.datagateway_api.extension}{Config.config.search_api.extension}/Instruments/count",
                {"GET"},
                id="search-instrument-count",
            ),
            pytest.param(
                f"{Config.config.datagateway_api.extension}{Config.config.search_api.extension}/Datasets/{{pid}}/files",
                {"GET"},
                id="search-dataset-files",
            ),
            pytest.param(
                f"{Config.config.datagateway_api.extension}{Config.config.search_api.extension}/Datasets/{{pid}}/files/count",
                {"GET"},
                id="search-dataset-files-count",
            ),
        ],
    )
    def test_non_entity_endpoints(self, test_client, endpoint_name, expected_methods):
        all_routes = collect_routes(test_client.app)

        print(all_routes)

        matching_routes = [methods for path, methods in all_routes if path == endpoint_name]

        assert matching_routes, f"Endpoint not found: {endpoint_name}"

        actual_methods = set()
        for methods in matching_routes:
            actual_methods |= methods

        assert expected_methods <= actual_methods, f"{endpoint_name}: expected {expected_methods}, got {actual_methods}"
