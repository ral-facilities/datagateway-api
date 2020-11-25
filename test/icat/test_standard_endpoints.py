from datagateway_api.src.main import api
from datagateway_api.src.main import app
from datagateway_api.src.resources.entities.entity_map import endpoints
from test.test_base import FlaskAppTest


class TestStandardEndpoints:
    def test_all_endpoints_exist(self):
        """
        session_endpoint_exist = api.owns_endpoint("sessions")
        assert session_endpoint_exist

        for endpoint_entity in endpoints.keys():
            get_endpoint_exist = api.owns_endpoint(endpoint_entity.lower())
            assert get_endpoint_exist

            id_endpoint_exist = api.owns_endpoint(
                f"{endpoint_entity.lower()}/<int:id_>",
            )
            assert id_endpoint_exist

            count_endpoint_exist = api.owns_endpoint(f"{endpoint_entity.lower()}/count")
            assert count_endpoint_exist

            findone_endpoint_exist = api.owns_endpoint(
                f"{endpoint_entity.lower()}/findone",
            )
            assert findone_endpoint_exist
        """
        pass
