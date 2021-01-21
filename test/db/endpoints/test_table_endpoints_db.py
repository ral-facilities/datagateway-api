class TestDBTableEndpoints:
    """
    This class tests the endpoints defined in table_endpoints.py, commonly referred to
    as the ISIS specific endpoints
    """

    def test_valid_get_facility_cycles_with_filters(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        isis_specific_endpoint_data_db,
    ):
        test_response = flask_test_app_db.get(
            f"/instruments/{int(isis_specific_endpoint_data_db[0])}/facilitycycles",
            headers=valid_db_credentials_header,
        )

        assert test_response.json == [isis_specific_endpoint_data_db[1].to_dict()]

    def test_invalid_get_facility_cycles_with_filters(
        self, flask_test_app_db, valid_db_credentials_header, final_instrument_id,
    ):
        test_response = flask_test_app_db.get(
            f"/instruments/{final_instrument_id + 100}/facilitycycles",
            headers=valid_db_credentials_header,
        )

        assert test_response.json == []

    def test_valid_get_facility_cycles_count_with_filters(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        isis_specific_endpoint_data_db,
    ):
        test_response = flask_test_app_db.get(
            f"/instruments/{isis_specific_endpoint_data_db[0]}/facilitycycles/count",
            headers=valid_db_credentials_header,
        )

        assert test_response.json == 1

    def test_invalid_get_facility_cycles_count_with_filters(
        self, flask_test_app_db, valid_db_credentials_header, final_instrument_id,
    ):
        test_response = flask_test_app_db.get(
            f"/instruments/{final_instrument_id + 100}/facilitycycles/count",
            headers=valid_db_credentials_header,
        )

        assert test_response.json == 0

    def test_valid_get_investigations_with_filters(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        isis_specific_endpoint_data_db,
    ):
        test_response = flask_test_app_db.get(
            f"/instruments/{isis_specific_endpoint_data_db[0]}/facilitycycles/"
            f"{isis_specific_endpoint_data_db[1].to_dict()['ID']}/investigations",
            headers=valid_db_credentials_header,
        )

        assert test_response.json == [isis_specific_endpoint_data_db[2].to_dict()]

    def test_invalid_get_investigations_with_filters(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        final_instrument_id,
        final_facilitycycle_id,
    ):
        test_response = flask_test_app_db.get(
            f"/instruments/{final_instrument_id + 100}/facilitycycles/"
            f"{final_facilitycycle_id + 100}/investigations",
            headers=valid_db_credentials_header,
        )

        assert test_response.json == []

    def test_valid_get_investigations_count_with_filters(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        isis_specific_endpoint_data_db,
    ):
        test_response = flask_test_app_db.get(
            f"/instruments/{isis_specific_endpoint_data_db[0]}/facilitycycles/"
            f"{isis_specific_endpoint_data_db[1].to_dict()['ID']}/investigations/count",
            headers=valid_db_credentials_header,
        )

        assert test_response.json == 1

    def test_invalid_get_investigations_count_with_filters(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        final_instrument_id,
        final_facilitycycle_id,
    ):
        test_response = flask_test_app_db.get(
            f"/instruments/{final_instrument_id + 100}/facilitycycles/"
            f"{final_facilitycycle_id + 100}/investigations/count",
            headers=valid_db_credentials_header,
        )

        assert test_response.json == 0
