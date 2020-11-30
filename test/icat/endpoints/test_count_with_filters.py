import pytest


class TestCountWithFilters:
    @pytest.mark.usefixtures("single_investigation_test_data")
    def test_valid_count_with_filters(self, flask_test_app, valid_credentials_header):
        test_response = flask_test_app.get(
            '/investigations/count?where={"title": {"like": "Test data for the Python'
            ' ICAT Backend on DataGateway API"}}',
            headers=valid_credentials_header,
        )

        assert test_response.json == 1

    def test_valid_no_results_count_with_filters(
        self, flask_test_app, valid_credentials_header,
    ):
        test_response = flask_test_app.get(
            '/investigations/count?where={"title": {"like": "This filter should cause a'
            '404 for testing purposes..."}}',
            headers=valid_credentials_header,
        )

        assert test_response.json == 0
