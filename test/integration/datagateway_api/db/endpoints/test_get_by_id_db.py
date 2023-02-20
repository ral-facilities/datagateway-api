from datagateway_api.src.common.config import Config


class TestDBGetByID:
    def test_valid_get_with_id(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        single_investigation_test_data_db,
    ):
        # Need to identify the ID given to the test data
        investigation_data = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/investigations?where="
            '{"title": {"like": "Title for DataGateway API Testing (DB)"}}',
            headers=valid_db_credentials_header,
        )
        test_data_id = investigation_data.json[0]["id"]

        test_response = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/investigations/{test_data_id}",
            headers=valid_db_credentials_header,
        )

        assert test_response.json == single_investigation_test_data_db.to_dict()

    def test_invalid_get_with_id(
        self, flask_test_app_db, valid_db_credentials_header,
    ):
        final_investigation_result = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/investigations/findone?order="
            '"id DESC"',
            headers=valid_db_credentials_header,
        )
        test_data_id = final_investigation_result.json["id"]

        # Adding 100 onto the ID to the most recent result should ensure a 404
        test_response = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/investigations"
            f"/{test_data_id + 100}",
            headers=valid_db_credentials_header,
        )

        assert test_response.status_code == 404
