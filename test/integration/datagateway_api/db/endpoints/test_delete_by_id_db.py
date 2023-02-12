from datagateway_api.src.common.config import Config


class TestDeleteById:
    def test_valid_delete_with_id(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        single_investigation_test_data_db,
    ):
        single_investigation_test_data = single_investigation_test_data_db.to_dict()

        test_response = flask_test_app_db.delete(
            f"{Config.config.datagateway_api.extension}/investigations"
            f'/{single_investigation_test_data["id"]}',
            headers=valid_db_credentials_header,
        )

        assert test_response.status_code == 204

    def test_invalid_delete_with_id(
        self, flask_test_app_db, valid_db_credentials_header,
    ):
        """Request with a non-existent ID"""

        final_investigation_result = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/investigations"
            '/findone?order="id DESC"',
            headers=valid_db_credentials_header,
        )
        test_data_id = final_investigation_result.json["id"]

        # Adding 100 onto the ID to the most recent result should ensure a 404
        test_response = flask_test_app_db.delete(
            f"{Config.config.datagateway_api.extension}/investigations"
            f"/{test_data_id + 100}",
            headers=valid_db_credentials_header,
        )

        assert test_response.status_code == 404
