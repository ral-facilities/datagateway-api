import pytest

from datagateway_api.src.main import app
from datagateway_api.src.resources.entities.entity_map import endpoints


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
    def test_entity_endpoints(self, endpoint_ending, expected_methods):
        for endpoint_entity in endpoints.keys():
            endpoint_found = False

            for rule in app.url_map.iter_rules():
                if f"/{endpoint_entity.lower()}{endpoint_ending}" == rule.rule:
                    endpoint_found = True

                    for method_name in expected_methods:
                        # Can't do a simple equality check as .methods contains other
                        # methods not added by the API which aren't utilised
                        assert method_name in rule.methods

            assert endpoint_found

    @pytest.mark.parametrize(
        "endpoint_name, expected_methods",
        [
            pytest.param("/sessions", ["DELETE", "GET", "POST", "PUT"], id="sessions"),
            pytest.param(
                "/instruments/<int:id_>/facilitycycles",
                ["GET"],
                id="ISIS instrument's facility cycles",
            ),
            pytest.param(
                "/instruments/<int:id_>/facilitycycles/count",
                ["GET"],
                id="count ISIS instrument's facility cycles",
            ),
            pytest.param(
                "/instruments/<int:instrument_id>/facilitycycles/<int:cycle_id>"
                "/investigations",
                ["GET"],
                id="ISIS investigations",
            ),
            pytest.param(
                "/instruments/<int:instrument_id>/facilitycycles/<int:cycle_id>"
                "/investigations/count",
                ["GET"],
                id="count ISIS investigations",
            ),
        ],
    )
    def test_non_entity_endpoints(self, endpoint_name, expected_methods):
        endpoint_found = False

        for rule in app.url_map.iter_rules():
            if endpoint_name == rule.rule:
                endpoint_found = True

                for method_name in expected_methods:
                    assert method_name in rule.methods

        assert endpoint_found
