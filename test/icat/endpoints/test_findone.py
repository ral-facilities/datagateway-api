from test.icat.test_query import prepare_icat_data_for_assertion


class TestFindone:
    def test_valid_findone_with_filters(
        self, flask_test_app, valid_credentials_header, single_investigation_test_data,
    ):
        test_response = flask_test_app.get(
            '/investigations/findone?where={"title": {"eq": "Test data for the Python'
            ' ICAT Backend on DataGateway API"}}',
            headers=valid_credentials_header,
        )
        response_json = prepare_icat_data_for_assertion([test_response.json])

        assert response_json == single_investigation_test_data

    def test_valid_no_results_findone_with_filters(
        self, flask_test_app, valid_credentials_header,
    ):
        test_response = flask_test_app.get(
            '/investigations/findone?where={"title": {"eq": "This filter should cause a'
            '404 for testing purposes..."}}',
            headers=valid_credentials_header,
        )

        assert test_response.status_code == 404
