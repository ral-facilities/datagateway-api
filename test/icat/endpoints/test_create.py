from test.icat.test_query import prepare_icat_data_for_assertion


class TestCreateData:
    def test_valid_create_data(
        self, flask_test_app_icat, valid_icat_credentials_header
    ):
        create_investigations_json = [
            {
                "name": "Test Data for API Testing, Data Creation 1",
                "title": "Test data for the Python ICAT Backend on DataGateway API",
                "summary": "Test data for DataGateway API testing",
                "releaseDate": "2020-03-03 08:00:08",
                "startDate": "2020-02-02 09:00:09",
                "endDate": "2020-02-03 10:00:10",
                "visitId": "Data Creation Visit",
                "doi": "DataGateway API Test DOI",
                "facility": 1,
                "type": 1,
            },
            {
                "name": "Test Data for API Testing, Data Creation 2",
                "title": "Test data for the Python ICAT Backend on DataGateway API",
                "summary": "Test data for DataGateway API testing",
                "releaseDate": "2020-03-03 08:00:08",
                "startDate": "2020-02-02 09:00:09",
                "endDate": "2020-02-03 10:00:10",
                "visitId": "Data Creation Visit",
                "doi": "DataGateway API Test DOI",
                "facility": 1,
                "type": 1,
            },
        ]

        test_response = flask_test_app_icat.post(
            "/investigations",
            headers=valid_icat_credentials_header,
            json=create_investigations_json,
        )

        test_data_ids = []
        for investigation_request, investigation_response in zip(
            create_investigations_json, test_response.json,
        ):
            investigation_request.pop("facility")
            investigation_request.pop("type")
            test_data_ids.append(investigation_response["id"])

        response_json = prepare_icat_data_for_assertion(
            test_response.json, remove_id=True,
        )

        assert create_investigations_json == response_json

        # Delete the entities created by this test
        for investigation_id in test_data_ids:
            flask_test_app_icat.delete(
                f"/investigations/{investigation_id}",
                headers=valid_icat_credentials_header,
            )

    def test_valid_boundary_create_data(
        self, flask_test_app_icat, valid_icat_credentials_header,
    ):
        """Create a single investigation, as opposed to multiple"""

        create_investigation_json = {
            "name": "Test Data for API Testing, Data Creation 0",
            "title": "Test data for the Python ICAT Backend on the API",
            "summary": "Test data for DataGateway API testing",
            "releaseDate": "2020-03-03 08:00:08",
            "startDate": "2020-02-02 09:00:09",
            "endDate": "2020-02-03 10:00:10",
            "visitId": "Data Creation Visit",
            "doi": "DataGateway API Test DOI",
            "facility": 1,
            "type": 1,
        }

        test_response = flask_test_app_icat.post(
            "/investigations",
            headers=valid_icat_credentials_header,
            json=create_investigation_json,
        )

        create_investigation_json.pop("facility")
        create_investigation_json.pop("type")
        created_test_data_id = test_response.json[0]["id"]

        response_json = prepare_icat_data_for_assertion(
            test_response.json, remove_id=True,
        )

        assert [create_investigation_json] == response_json

        flask_test_app_icat.delete(
            f"/investigations/{created_test_data_id}",
            headers=valid_icat_credentials_header,
        )

    def test_invalid_create_data(
        self, flask_test_app_icat, valid_icat_credentials_header
    ):
        """An investigation requires a minimum of: name, visitId, facility, type"""

        invalid_request_body = {
            "title": "Test Title for DataGateway API Backend testing",
        }

        test_response = flask_test_app_icat.post(
            "/investigations",
            headers=valid_icat_credentials_header,
            json=invalid_request_body,
        )

        assert test_response.status_code == 400

    def test_invalid_existing_data_create(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        single_investigation_test_data,
    ):
        """This test targets raising ICATObjectExistsError, causing a 400"""

        # entity.as_dict() removes details about facility and type, hence they're
        # hardcoded here instead of using sinle_investigation_test_data
        existing_object_json = {
            "name": single_investigation_test_data[0]["name"],
            "title": single_investigation_test_data[0]["title"],
            "visitId": single_investigation_test_data[0]["visitId"],
            "facility": 1,
            "type": 1,
        }

        test_response = flask_test_app_icat.post(
            "/investigations",
            headers=valid_icat_credentials_header,
            json=existing_object_json,
        )

        assert test_response.status_code == 400
