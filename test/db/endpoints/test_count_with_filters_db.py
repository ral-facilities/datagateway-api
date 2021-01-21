import pytest


class TestDBCountWithFilters:
    @pytest.mark.usefixtures("single_investigation_test_data_db")
    def test_valid_count_with_filters(
        self, flask_test_app_db, valid_db_credentials_header,
    ):
        test_response = flask_test_app_db.get(
            '/investigations/count?where={"TITLE": {"like": "Title for DataGateway API'
            ' Testing (DB)"}}',
            headers=valid_db_credentials_header,
        )

        assert test_response.json == 1

    def test_valid_no_results_count_with_filters(
        self, flask_test_app_db, valid_db_credentials_header,
    ):
        test_response = flask_test_app_db.get(
            '/investigations/count?where={"TITLE": {"like": "This filter should cause a'
            '404 for testing purposes..."}}',
            headers=valid_db_credentials_header,
        )

        assert test_response.json == 0
