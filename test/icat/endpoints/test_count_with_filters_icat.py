import pytest


class TestICATCountWithFilters:
    @pytest.mark.usefixtures("single_investigation_test_data")
    def test_valid_count_with_filters(
        self, flask_test_app_icat, valid_icat_credentials_header,
    ):
        test_response = flask_test_app_icat.get(
            '/investigations/count?where={"title": {"like": "Test data for the Python'
            ' ICAT Backend on DataGateway API"}}',
            headers=valid_icat_credentials_header,
        )

        assert test_response.json == 1

    def test_valid_no_results_count_with_filters(
        self, flask_test_app_icat, valid_icat_credentials_header,
    ):
        test_response = flask_test_app_icat.get(
            '/investigations/count?where={"title": {"like": "This filter should cause a'
            '404 for testing purposes..."}}',
            headers=valid_icat_credentials_header,
        )

        assert test_response.json == 0
