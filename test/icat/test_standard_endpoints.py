import pytest

from datagateway_api.src.main import api
from datagateway_api.src.main import app
from datagateway_api.src.resources.entities.entity_map import endpoints
from test.icat.test_query import prepare_icat_data_for_assertion
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

    def test_valid_get_with_filters(
        self, flask_test_app, valid_credentials_header, single_investigation_test_data,
    ):
        test_response = flask_test_app.get(
            '/investigations?where={"title": {"eq": "Test data for the Python ICAT'
            ' Backend on DataGateway API"}}',
            headers=valid_credentials_header,
        )
        response_json = prepare_icat_data_for_assertion(test_response.json)

        assert response_json == single_investigation_test_data

    def test_invalid_get_with_filters(self):
        # Invalid data?
        pass

    def test_valid_create_data(self):
        pass

    def test_invalid_create_data(self):
        # Invalid request body
        pass

    def test_invalid_create_data_1(self):
        # TODO - Rename function
        # Target ICATObjectExistsError
        pass

    def test_valid_update_data(self):
        pass

    def test_valid_boundary_update_data(self):
        """ Request body is a dictionary, not a list of dictionaries"""
        pass

    def test_invalid_update_data(self):
        # Exclude an ID at in one of the data pieces
        pass

    def test_valid_get_one_with_filters(
        self, flask_test_app, valid_credentials_header, single_investigation_test_data,
    ):
        test_response = flask_test_app.get(
            '/investigations/findone?where={"title": {"eq": "Test data for the Python'
            ' ICAT Backend on DataGateway API"}}',
            headers=valid_credentials_header,
        )
        response_json = prepare_icat_data_for_assertion([test_response.json])

        assert response_json == single_investigation_test_data

    @pytest.mark.usefixtures("single_investigation_test_data")
    def test_valid_count_with_filters(self, flask_test_app, valid_credentials_header):
        test_response = flask_test_app.get(
            '/investigations/count?where={"title": {"eq": "Test data for the Python'
            ' ICAT Backend on DataGateway API"}}',
            headers=valid_credentials_header,
        )

        assert test_response.json == 1

    def test_valid_get_with_id(
        self, flask_test_app, valid_credentials_header, single_investigation_test_data,
    ):
        # Need to identify the ID given to the test data
        investigation_data = flask_test_app.get(
            '/investigations?where={"title": {"eq": "Test data for the Python ICAT'
            ' Backend on DataGateway API"}}',
            headers=valid_credentials_header,
        )
        test_data_id = investigation_data.json[0]["id"]

        test_response = flask_test_app.get(
            f"/investigations/{test_data_id}", headers=valid_credentials_header,
        )
        # Get with ID gives a dictionary response (only ever one result from that kind
        # of request), so list around json is required for the call
        response_json = prepare_icat_data_for_assertion([test_response.json])

        assert response_json == single_investigation_test_data

    def test_invalid_get_with_id(self):
        # Do a get one with filters (order desc), extract the id of that, add 5 and do a
        # request for that
        pass

    def test_valid_delete_with_id(self):
        pass

    def test_invalid_delete_with_id(self):
        # like invalid get, but try to delete
        pass

    def test_valid_update_with_id(self):
        pass

    def test_invalid_update_with_id(self):
        pass
