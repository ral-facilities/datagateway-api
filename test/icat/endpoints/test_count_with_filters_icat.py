import pytest


class TestICATCountWithFilters:
    @pytest.mark.parametrize(
        "query_params, expected_result",
        [
            pytest.param(
                '?where={"title": {"like": "Test data for the Python ICAT Backend on'
                ' on DataGateway API"}}',
                5,
                id="Filter on test data",
            ),
            pytest.param(
                '?where={"title": {"like": "Test data for the Python ICAT Backend on'
                ' on DataGateway API"}}&distinct=["startDate"]',
                1,
                id="Distinct test data",
            ),
        ],
    )
    @pytest.mark.usefixtures("multiple_investigation_test_data")
    def test_valid_count_with_filters(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        query_params,
        expected_result,
    ):
        test_response = flask_test_app_icat.get(
            f"/investigations/count{query_params}",
            headers=valid_icat_credentials_header,
        )

        assert test_response.json == expected_result

    def test_valid_no_results_count_with_filters(
        self, flask_test_app_icat, valid_icat_credentials_header,
    ):
        test_response = flask_test_app_icat.get(
            '/investigations/count?where={"title": {"like": "This filter should cause a'
            '404 for testing purposes..."}}',
            headers=valid_icat_credentials_header,
        )

        assert test_response.json == 0
