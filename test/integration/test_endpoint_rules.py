import pytest

from datagateway_api.src.common.config import Config
from datagateway_api.src.resources.entities.entity_endpoint_dict import endpoints


class TestEndpointRules:
    """
    Test class to ensure all endpoints on the API exist & have the correct HTTP methods
    """

    @pytest.mark.parametrize(
        "endpoint_ending, expected_methods",
        [
            pytest.param("/findone", ["GET"], id="findone"),
            pytest.param("/count", ["GET"], id="count"),
            pytest.param("/<int:id_>", ["DELETE", "GET", "PATCH"], id="id"),
            pytest.param("", ["GET", "PATCH", "POST"], id="typical endpoints"),
        ],
    )
    def test_entity_endpoints(self, flask_test_app, endpoint_ending, expected_methods):
        for endpoint_entity in endpoints.keys():
            endpoint_found = False

            for rule in flask_test_app.url_map.iter_rules():
                if (
                    f"{Config.config.datagateway_api.extension}"
                    f"/{endpoint_entity.lower()}{endpoint_ending}" == rule.rule
                ):
                    endpoint_found = True

                    for method_name in expected_methods:
                        # Can't do a simple equality check as .methods contains other
                        # methods not added by the API which aren't utilised
                        assert method_name in rule.methods

            assert endpoint_found

    @pytest.mark.parametrize(
        "endpoint_name, expected_methods",
        [
            pytest.param(
                f"{Config.config.datagateway_api.extension}/sessions",
                ["DELETE", "GET", "POST", "PUT"],
                id="sessions",
            ),
            pytest.param(
                f"{Config.config.search_api.extension}/Datasets",
                ["GET"],
                id="Search API search datasets",
            ),
            pytest.param(
                f"{Config.config.search_api.extension}/Documents",
                ["GET"],
                id="Search API search documents",
            ),
            pytest.param(
                f"{Config.config.search_api.extension}/Instruments",
                ["GET"],
                id="Search API search instruments",
            ),
            pytest.param(
                f"{Config.config.search_api.extension}/Datasets/<string:pid>",
                ["GET"],
                id="Search API get single dataset",
            ),
            pytest.param(
                f"{Config.config.search_api.extension}/Documents/<string:pid>",
                ["GET"],
                id="Search API get single document",
            ),
            pytest.param(
                f"{Config.config.search_api.extension}/Instruments/<string:pid>",
                ["GET"],
                id="Search API get single instrument",
            ),
            pytest.param(
                f"{Config.config.search_api.extension}/Datasets/count",
                ["GET"],
                id="Search API dataset count",
            ),
            pytest.param(
                f"{Config.config.search_api.extension}/Documents/count",
                ["GET"],
                id="Search API document count",
            ),
            pytest.param(
                f"{Config.config.search_api.extension}/Instruments/count",
                ["GET"],
                id="Search API instrument count",
            ),
            pytest.param(
                f"{Config.config.search_api.extension}/Datasets/<string:pid>/files",
                ["GET"],
                id="Search API get dataset files",
            ),
            pytest.param(
                f"{Config.config.search_api.extension}/Datasets/<string:pid>/files"
                "/count",
                ["GET"],
                id="Search API dataset files count",
            ),
        ],
    )
    def test_non_entity_endpoints(
        self, flask_test_app, endpoint_name, expected_methods,
    ):
        endpoint_found = False

        for rule in flask_test_app.url_map.iter_rules():
            if endpoint_name == rule.rule:
                endpoint_found = True

                for method_name in expected_methods:
                    assert method_name in rule.methods

        assert endpoint_found
