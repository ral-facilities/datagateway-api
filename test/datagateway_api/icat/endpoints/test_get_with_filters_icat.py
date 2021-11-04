import pytest

from test.datagateway_api.icat.test_query import prepare_icat_data_for_assertion


class TestICATGetWithFilters:
    def test_valid_get_with_filters(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        single_investigation_test_data,
    ):
        test_response = flask_test_app_icat.get(
            '/investigations?where={"title": {"like": "Test data for the Python ICAT'
            ' Backend on DataGateway API"}}',
            headers=valid_icat_credentials_header,
        )
        response_json = prepare_icat_data_for_assertion(test_response.json)

        assert response_json == single_investigation_test_data

    def test_valid_no_results_get_with_filters(
        self, flask_test_app_icat, valid_icat_credentials_header,
    ):
        test_response = flask_test_app_icat.get(
            '/investigations?where={"title": {"eq": "This filter should cause a 404 for'
            'testing purposes..."}}',
            headers=valid_icat_credentials_header,
        )

        assert test_response.json == []

    @pytest.mark.usefixtures("multiple_investigation_test_data")
    def test_valid_get_with_filters_distinct(
        self, flask_test_app_icat, valid_icat_credentials_header,
    ):
        test_response = flask_test_app_icat.get(
            '/investigations?where={"title": {"like": "Test data for the Python ICAT'
            ' Backend on DataGateway API"}}&distinct="title"',
            headers=valid_icat_credentials_header,
        )

        expected = [
            {"title": f"Test data for the Python ICAT Backend on DataGateway API {i}"}
            for i in range(5)
        ]

        for title in expected:
            assert title in test_response.json

    def test_limit_skip_merge_get_with_filters(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        multiple_investigation_test_data,
    ):
        skip_value = 1
        limit_value = 2

        test_response = flask_test_app_icat.get(
            '/investigations?where={"title": {"like": "Test data for the Python ICAT'
            ' Backend on DataGateway API"}}'
            f'&skip={skip_value}&limit={limit_value}&order="id ASC"',
            headers=valid_icat_credentials_header,
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
