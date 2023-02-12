from datagateway_api.src.common.config import Config
from test.integration.datagateway_api.icat.test_query import (
    prepare_icat_data_for_assertion,
)


class TestICATGetByID:
    def test_valid_get_with_id(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        single_investigation_test_data,
    ):
        # Need to identify the ID given to the test data
        investigation_data = flask_test_app_icat.get(
            f"{Config.config.datagateway_api.extension}/investigations?where="
            '{"title": {"like": "Test data for the Python ICAT Backend on '
            'DataGateway API"}}',
            headers=valid_icat_credentials_header,
        )
        test_data_id = investigation_data.json[0]["id"]

        test_response = flask_test_app_icat.get(
            f"{Config.config.datagateway_api.extension}/investigations/{test_data_id}",
            headers=valid_icat_credentials_header,
        )
        # Get with ID gives a dictionary response (only ever one result from that kind
        # of request), so list around json is required for the call
        response_json = prepare_icat_data_for_assertion([test_response.json])

        assert response_json == single_investigation_test_data

    def test_invalid_get_with_id(
        self, flask_test_app_icat, valid_icat_credentials_header,
    ):
        """Request with a non-existent ID"""

        final_investigation_result = flask_test_app_icat.get(
            f"{Config.config.datagateway_api.extension}/investigations/findone?order="
            '"id DESC"',
            headers=valid_icat_credentials_header,
        )
        test_data_id = final_investigation_result.json["id"]

        # Adding 100 onto the ID to the most recent result should ensure a 404
        test_response = flask_test_app_icat.get(
            f"{Config.config.datagateway_api.extension}/investigations"
            f"/{test_data_id + 100}",
            headers=valid_icat_credentials_header,
        )

        assert test_response.status_code == 404
