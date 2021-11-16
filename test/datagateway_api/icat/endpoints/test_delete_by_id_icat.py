from datagateway_api.src.common.config import config


class TestDeleteByID:
    def test_valid_delete_with_id(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        single_investigation_test_data,
    ):
        test_response = flask_test_app_icat.delete(
            f"{config.datagateway_api.extension}/investigations"
            f'/{single_investigation_test_data[0]["id"]}',
            headers=valid_icat_credentials_header,
        )

        assert test_response.status_code == 204

    def test_invalid_delete_with_id(
        self, flask_test_app_icat, valid_icat_credentials_header,
    ):
        """Request with a non-existent ID"""

        final_investigation_result = flask_test_app_icat.get(
            f"{config.datagateway_api.extension}/investigations"
            '/findone?order="id DESC"',
            headers=valid_icat_credentials_header,
        )
        test_data_id = final_investigation_result.json["id"]

        # Adding 100 onto the ID to the most recent result should ensure a 404
        test_response = flask_test_app_icat.delete(
            f"{config.datagateway_api.extension}/investigations/{test_data_id + 100}",
            headers=valid_icat_credentials_header,
        )

        assert test_response.status_code == 404
