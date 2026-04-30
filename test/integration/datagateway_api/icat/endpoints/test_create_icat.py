import pytest

from test.integration.datagateway_api.icat.test_query import (
    prepare_icat_data_for_assertion,
)
from test.mock_data import LARGE_INVESTIGATION_POST


class TestICATCreateData:
    investigation_name_prefix = "Test Data for API Testing, Data Creation"

    @pytest.mark.usefixtures("remove_test_created_investigation_data")
    def test_valid_create_data(
        self,
        test_client,
        valid_icat_credentials_header,
    ):
        create_investigations_json = [
            {
                "name": f"{self.investigation_name_prefix} {i}",
                "title": "Test data for Python ICAT on DataGateway API",
                "summary": "Test data for DataGateway API testing",
                "releaseDate": "2020-03-03 08:00:08+00:00",
                "startDate": "2020-02-02 09:00:09+00:00",
                "endDate": "2020-02-03 10:00:10+00:00",
                "visitId": "Data Creation Visit",
                "doi": "DataGateway API Test DOI",
                "facility": 1,
                "type": 1,
                "fileCount": 1,
                "fileSize": 6,
            }
            for i in range(2)
        ]

        create_investigations_json.append(
            {
                **LARGE_INVESTIGATION_POST,
                "releaseDate": "2020-03-03 08:00:08+00:00",
                "startDate": "2020-02-02 09:00:09+00:00",
            },
        )

        test_response = test_client.post(
            "/datagateway-api/investigations",
            headers=valid_icat_credentials_header,
            json=create_investigations_json,
        )

        optional_keys_to_remove = (
            "facility",
            "type",
            "datasets",
            "investigationFacilityCycles",
            "investigationUsers",
            "publications",
            "samples",
            "studyInvestigations",
        )

        for investigation_request in create_investigations_json:
            for key in optional_keys_to_remove:
                investigation_request.pop(key, None)

        response_json = prepare_icat_data_for_assertion(
            test_response.json(),
            remove_id=True,
        )

        assert create_investigations_json == response_json

    @pytest.mark.usefixtures("remove_test_created_investigation_data")
    def test_valid_boundary_create_data(
        self,
        test_client,
        valid_icat_credentials_header,
    ):
        """Create a single investigation, as opposed to multiple"""

        create_investigation_json = [
            {
                "name": f"{self.investigation_name_prefix} 0",
                "title": "Test data for Python ICAT on the API",
                "summary": "Test data for DataGateway API testing",
                "releaseDate": "2020-03-03 08:00:08+00:00",
                "startDate": "2020-02-02 09:00:09+00:00",
                "endDate": "2020-02-03 10:00:10+00:00",
                "visitId": "Data Creation Visit",
                "doi": "DataGateway API Test DOI",
                "facility": 1,
                "type": 1,
                "fileCount": 3,
                "fileSize": 2,
            },
        ]

        test_response = test_client.post(
            "/datagateway-api/investigations",
            headers=valid_icat_credentials_header,
            json=create_investigation_json,
        )

        create_investigation_json[0].pop("facility")
        create_investigation_json[0].pop("type")

        response_json = prepare_icat_data_for_assertion(
            test_response.json(),
            remove_id=True,
        )

        assert create_investigation_json == response_json

    def test_invalid_create_data(
        self,
        test_client,
        valid_icat_credentials_header,
    ):
        """An investigation requires a minimum of: name, visitId, facility, type"""

        invalid_request_body = [
            {
                "title": "Test Title for DataGateway API Python ICAT testing",
            },
        ]

        test_response = test_client.post(
            "/datagateway-api/investigations",
            headers=valid_icat_credentials_header,
            json=invalid_request_body,
        )

        assert test_response.status_code == 400

    def test_invalid_existing_data_create(
        self,
        test_client,
        valid_icat_credentials_header,
        single_investigation_test_data,
    ):
        """This test targets raising ICATObjectExistsError, causing a 400"""

        # entity.as_dict() removes details about facility and type, hence they're
        # hardcoded here instead of using sinle_investigation_test_data
        existing_object_json = [
            {
                "name": single_investigation_test_data[0]["name"],
                "title": single_investigation_test_data[0]["title"],
                "visitId": single_investigation_test_data[0]["visitId"],
                "facility": 1,
                "type": 1,
            },
        ]

        test_response = test_client.post(
            "/datagateway-api/investigations",
            headers=valid_icat_credentials_header,
            json=existing_object_json,
        )

        assert test_response.status_code == 400

    def test_valid_rollback_behaviour(
        self,
        test_client,
        valid_icat_credentials_header,
    ):
        request_body = [
            {
                "name": "Test Investigation DG API Testing Name Test",
                "title": "My New Investigation with Title",
                "visitId": "Visit ID for Testing",
                "facility": 1,
                "type": 1,
            },
            {
                "name": "Invalid Investigation for testing",
                "title": "My New Investigation with Title",
                "visitId": "Visit ID for Testing",
                "doi": "_" * 256,
                "facility": 1,
                "type": 1,
            },
        ]

        create_response = test_client.post(
            "/datagateway-api/investigations",
            headers=valid_icat_credentials_header,
            json=request_body,
        )

        get_response = test_client.get(
            "/datagateway-api/investigations?where="  # noqa: B907
            '{"title": {"eq": "'
            f'{request_body[0]["title"]}'
            '"}}',
            headers=valid_icat_credentials_header,
        )
        get_response_json = prepare_icat_data_for_assertion(get_response.json())

        assert create_response.status_code == 400
        assert get_response_json == []
