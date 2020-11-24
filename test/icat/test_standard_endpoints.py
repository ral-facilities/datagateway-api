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

    @pytest.mark.usefixtures("multiple_investigation_test_data")
    def test_valid_get_with_filters_distinct(
        self, flask_test_app, valid_credentials_header,
    ):
        test_response = flask_test_app.get(
            '/investigations?where={"title": {"like": "Test data for the Python ICAT'
            ' Backend on DataGateway API"}}&distinct="title"',
            headers=valid_credentials_header,
        )

        expected = [
            {
                "title": f"Test data for the Python ICAT Backend on DataGateway API {i}"
                for i in range(5)
            },
        ]

        for title in expected:
            assert title in test_response.json

    def test_limit_skip_merge_get_with_filters(
        self,
        flask_test_app,
        valid_credentials_header,
        multiple_investigation_test_data,
    ):
        skip_value = 1
        limit_value = 2

        test_response = flask_test_app.get(
            '/investigations?where={"title": {"like": "Test data for the Python ICAT'
            ' Backend on DataGateway API"}}'
            f'&skip={skip_value}&limit={limit_value}&order="id ASC"',
            headers=valid_credentials_header,
        )
        response_json = prepare_icat_data_for_assertion(test_response.json)

        filtered_investigation_data = []
        filter_count = 0
        while filter_count < limit_value:
            filtered_investigation_data.append(
                multiple_investigation_test_data.pop(skip_value),
            )
            filter_count += 1

        assert response_json == filtered_investigation_data

    def test_valid_create_data(self):
        pass

    def test_invalid_create_data(self):
        # Invalid request body
        pass

    def test_invalid_create_data_1(self):
        # TODO - Rename function
        # Target ICATObjectExistsError
        pass

    def test_valid_multiple_update_data(
        self,
        flask_test_app,
        valid_credentials_header,
        multiple_investigation_test_data,
    ):
        expected_doi = "Test Data Identifier"
        expected_summary = "Test Summary"

        update_data_list = []

        for investigation in multiple_investigation_test_data:
            investigation["doi"] = expected_doi
            investigation["summary"] = expected_summary

            update_entity = {
                "id": investigation["id"],
                "doi": expected_doi,
                "summary": expected_summary,
            }
            update_data_list.append(update_entity)

        test_response = flask_test_app.patch(
            "/investigations", headers=valid_credentials_header, json=update_data_list,
        )
        response_json = prepare_icat_data_for_assertion(test_response.json)

        assert response_json == multiple_investigation_test_data

    def test_valid_boundary_update_data(
        self, flask_test_app, valid_credentials_header, single_investigation_test_data,
    ):
        """ Request body is a dictionary, not a list of dictionaries"""

        expected_doi = "Test Data Identifier"
        expected_summary = "Test Summary"

        update_data_json = {
            "id": single_investigation_test_data[0]["id"],
            "doi": expected_doi,
            "summary": expected_summary,
        }
        single_investigation_test_data[0]["doi"] = expected_doi
        single_investigation_test_data[0]["summary"] = expected_summary

        test_response = flask_test_app.patch(
            "/investigations", headers=valid_credentials_header, json=update_data_json,
        )
        response_json = prepare_icat_data_for_assertion(test_response.json)

        assert response_json == single_investigation_test_data

    def test_invalid_update_data(
        self, flask_test_app, valid_credentials_header, single_investigation_test_data,
    ):
        """There should be an ID in the request body to know which entity to update"""

        expected_doi = "Test Data Identifier"
        expected_summary = "Test Summary"

        update_data_json = {
            "doi": expected_doi,
            "summary": expected_summary,
        }
        single_investigation_test_data[0]["doi"] = expected_doi
        single_investigation_test_data[0]["summary"] = expected_summary

        test_response = flask_test_app.patch(
            "/investigations", headers=valid_credentials_header, json=update_data_json,
        )

        assert test_response.status_code == 400

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

    def test_invalid_get_with_id(self, flask_test_app, valid_credentials_header):
        # Do a get one with filters (order desc), extract the id of that, add 5 and do a
        # request for that
        # Need to identify the ID given to the test data
        final_investigation_result = flask_test_app.get(
            '/investigations/findone?order="id DESC"', headers=valid_credentials_header,
        )
        test_data_id = final_investigation_result.json["id"]

        # Adding 100 onto the ID to the most recent result should ensure a 404
        test_response = flask_test_app.get(
            f"/investigations/{test_data_id + 100}", headers=valid_credentials_header,
        )

        assert test_response.status_code == 404

    def test_valid_delete_with_id(self):
        pass

    def test_invalid_delete_with_id(self):
        # like invalid get, but try to delete
        pass

    def test_valid_update_with_id(
        self, flask_test_app, valid_credentials_header, single_investigation_test_data,
    ):
        expected_doi = "Test Data Identifier"
        expected_summary = "Test Summary"

        update_data_json = {
            "doi": expected_doi,
            "summary": expected_summary,
        }
        single_investigation_test_data[0]["doi"] = expected_doi
        single_investigation_test_data[0]["summary"] = expected_summary

        test_response = flask_test_app.patch(
            f"/investigations/{single_investigation_test_data[0]['id']}",
            headers=valid_credentials_header,
            json=update_data_json,
        )
        response_json = prepare_icat_data_for_assertion([test_response.json])

        assert response_json == single_investigation_test_data

    def test_invalid_update_with_id(self):
        pass
