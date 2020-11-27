class TestTableEndpoints:
    """
    This class tests the endpoints defined in table_endpoints.py, commonly referred to
    as the ISIS specific endpoints
    """

    def test_valid_get_facility_cycles_with_filters(self):
        pass

    def test_invalid_get_facility_cycles_with_filters(
        self, flask_test_app, valid_credentials_header,
    ):
        final_instrument_result = flask_test_app.get(
            '/instruments/findone?order="id DESC"', headers=valid_credentials_header,
        )
        final_instrument_id = final_instrument_result.json["id"]

        test_response = flask_test_app.get(
            f"/instruments/{final_instrument_id + 100}/facilitycycles",
            headers=valid_credentials_header,
        )

        assert test_response.status_code == 404

    def test_valid_get_facility_cycles_count_with_filters(self):
        pass

    def test_invalid_get_facility_cycles_count_with_filters(
        self, flask_test_app, valid_credentials_header,
    ):
        final_instrument_result = flask_test_app.get(
            '/instruments/findone?order="id DESC"', headers=valid_credentials_header,
        )
        final_instrument_id = final_instrument_result.json["id"]

        test_response = flask_test_app.get(
            f"/instruments/{final_instrument_id + 100}/facilitycycles/count",
            headers=valid_credentials_header,
        )

        assert test_response.json == 0

    def test_valid_get_investigations_with_filters(self):
        pass

    def test_invalid_get_investigations_with_filters(
        self, flask_test_app, valid_credentials_header,
    ):
        final_instrument_result = flask_test_app.get(
            '/instruments/findone?order="id DESC"', headers=valid_credentials_header,
        )
        final_instrument_id = final_instrument_result.json["id"]
        final_facilitycycle_result = flask_test_app.get(
            '/facilitycycles/findone?order="id DESC"', headers=valid_credentials_header,
        )
        final_facilitycycle_id = final_facilitycycle_result.json["id"]

        test_response = flask_test_app.get(
            f"/instruments/{final_instrument_id + 100}/facilitycycles/"
            f"{final_facilitycycle_id + 100}/investigations",
            headers=valid_credentials_header,
        )

        assert test_response.status_code == 404

    def test_valid_get_investigations_count_with_filters(self):
        pass

    def test_invalid_get_investigations_count_with_filters(
        self, flask_test_app, valid_credentials_header,
    ):
        final_instrument_result = flask_test_app.get(
            '/instruments/findone?order="id DESC"', headers=valid_credentials_header,
        )
        final_instrument_id = final_instrument_result.json["id"]
        final_facilitycycle_result = flask_test_app.get(
            '/facilitycycles/findone?order="id DESC"', headers=valid_credentials_header,
        )
        final_facilitycycle_id = final_facilitycycle_result.json["id"]

        test_response = flask_test_app.get(
            f"/instruments/{final_instrument_id + 100}/facilitycycles/"
            f"{final_facilitycycle_id + 100}/investigations/count",
            headers=valid_credentials_header,
        )

        assert test_response.json == 0
