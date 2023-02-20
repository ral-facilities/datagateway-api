from datagateway_api.src.common.config import Config
from test.integration.datagateway_api.icat.test_query import (
    prepare_icat_data_for_assertion,
)


class TestICATableEndpoints:
    """
    This class tests the endpoints defined in table_endpoints.py, commonly referred to
    as the ISIS specific endpoints
    """

    def test_valid_get_facility_cycles_with_filters(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        isis_specific_endpoint_data,
    ):
        test_response = flask_test_app_icat.get(
            f"{Config.config.datagateway_api.extension}/instruments"
            f"/{isis_specific_endpoint_data[0]}/facilitycycles",
            headers=valid_icat_credentials_header,
        )

        response_json = prepare_icat_data_for_assertion(test_response.json)

        assert response_json == isis_specific_endpoint_data[1]

    def test_invalid_get_facility_cycles_with_filters(
        self, flask_test_app_icat, valid_icat_credentials_header, final_instrument_id,
    ):
        test_response = flask_test_app_icat.get(
            f"{Config.config.datagateway_api.extension}/instruments"
            f"/{final_instrument_id + 100}/facilitycycles",
            headers=valid_icat_credentials_header,
        )

        assert test_response.json == []

    def test_valid_get_facility_cycles_count_with_filters(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        isis_specific_endpoint_data,
    ):
        test_response = flask_test_app_icat.get(
            f"{Config.config.datagateway_api.extension}/instruments"
            f"/{isis_specific_endpoint_data[0]}/facilitycycles/count",
            headers=valid_icat_credentials_header,
        )

        assert test_response.json == 1

    def test_invalid_get_facility_cycles_count_with_filters(
        self, flask_test_app_icat, valid_icat_credentials_header, final_instrument_id,
    ):
        test_response = flask_test_app_icat.get(
            f"{Config.config.datagateway_api.extension}/instruments"
            f"/{final_instrument_id + 100}/facilitycycles/count",
            headers=valid_icat_credentials_header,
        )

        assert test_response.json == 0

    def test_valid_get_investigations_with_filters(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        isis_specific_endpoint_data,
    ):
        test_response = flask_test_app_icat.get(
            f"{Config.config.datagateway_api.extension}/instruments"
            f"/{isis_specific_endpoint_data[0]}/facilitycycles"
            f"/{isis_specific_endpoint_data[2]}/investigations",
            headers=valid_icat_credentials_header,
        )

        response_json = prepare_icat_data_for_assertion(test_response.json)

        assert response_json == isis_specific_endpoint_data[3]

    def test_invalid_get_investigations_with_filters(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        final_instrument_id,
        final_facilitycycle_id,
    ):
        test_response = flask_test_app_icat.get(
            f"{Config.config.datagateway_api.extension}/instruments"
            f"/{final_instrument_id + 100}/facilitycycles"
            f"/{final_facilitycycle_id + 100}/investigations",
            headers=valid_icat_credentials_header,
        )

        assert test_response.json == []

    def test_valid_get_investigations_count_with_filters(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        isis_specific_endpoint_data,
    ):
        test_response = flask_test_app_icat.get(
            f"{Config.config.datagateway_api.extension}/instruments"
            f"/{isis_specific_endpoint_data[0]}/facilitycycles"
            f"/{isis_specific_endpoint_data[2]}/investigations/count",
            headers=valid_icat_credentials_header,
        )

        assert test_response.json == 1

    def test_invalid_get_investigations_count_with_filters(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        final_instrument_id,
        final_facilitycycle_id,
    ):
        test_response = flask_test_app_icat.get(
            f"{Config.config.datagateway_api.extension}/instruments"
            f"/{final_instrument_id + 100}/facilitycycles"
            f"/{final_facilitycycle_id + 100}/investigations/count",
            headers=valid_icat_credentials_header,
        )

        assert test_response.json == 0
