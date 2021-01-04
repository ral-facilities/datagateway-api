import pytest


class TestDBGetWithFilters:
    def test_valid_get_with_filters(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        single_investigation_test_data_db,
    ):
        test_response = flask_test_app_db.get(
            '/investigations?where={"TITLE": {"like": "Title for DataGateway API'
            ' Testing (DB)"}}',
            headers=valid_db_credentials_header,
        )

        assert test_response.json == [single_investigation_test_data_db.to_dict()]

    def test_valid_no_results_get_with_filters(
        self, flask_test_app_db, valid_db_credentials_header,
    ):
        test_response = flask_test_app_db.get(
            '/investigations?where={"TITLE": {"eq": "This filter should cause a 404 for'
            'testing purposes..."}}',
            headers=valid_db_credentials_header,
        )

        assert test_response.json == []

    @pytest.mark.usefixtures("multiple_investigation_test_data_db")
    def test_valid_get_with_filters_distinct(
        self, flask_test_app_db, valid_db_credentials_header,
    ):
        test_response = flask_test_app_db.get(
            '/investigations?where={"TITLE": {"like": "Title for DataGateway API'
            ' Testing (DB)"}}&distinct="TITLE"',
            headers=valid_db_credentials_header,
        )

        expected = [
            {"TITLE": f"Title for DataGateway API Testing (DB) {i}"} for i in range(5)
        ]

        for title in expected:
            assert title in test_response.json

    def test_limit_skip_merge_get_with_filters(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        multiple_investigation_test_data_db,
    ):
        skip_value = 1
        limit_value = 2

        test_response = flask_test_app_db.get(
            '/investigations?where={"TITLE": {"like": "Title for DataGateway API'
            ' Testing (DB)"}}'
            f'&skip={skip_value}&limit={limit_value}&order="ID ASC"',
            headers=valid_db_credentials_header,
        )

        # Copy required to ensure data is deleted at the end of the test
        investigation_test_data_copy = multiple_investigation_test_data_db.copy()
        filtered_investigation_data = []
        filter_count = 0
        while filter_count < limit_value:
            filtered_investigation_data.append(
                investigation_test_data_copy.pop(skip_value).to_dict(),
            )
            filter_count += 1

        assert test_response.json == filtered_investigation_data
