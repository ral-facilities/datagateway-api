from datagateway_api.src.common.config import Config


class TestUpdateByID:
    def test_valid_update_with_id(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        single_investigation_test_data_db,
    ):
        update_data_json = {
            "doi": "DB Test Data Identifier",
            "summary": "DB Test Summary",
            "startDate": "2019-01-04 01:01:01",
        }

        single_investigation_test_data = single_investigation_test_data_db.to_dict()

        single_investigation_test_data.update(update_data_json)
        test_response = flask_test_app_db.patch(
            f"{Config.config.datagateway_api.extension}/investigations"
            f"/{single_investigation_test_data['id']}",
            headers=valid_db_credentials_header,
            json=update_data_json,
        )

        response_json = test_response.json

        # The DB returns times with timezone indicators,
        # but does not accept them being created.
        # This strips the timezone indicators out so that the results can be compared.
        response_json["startDate"] = response_json["startDate"][:-6]

        assert response_json == single_investigation_test_data

    def test_invalid_update_with_id(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        single_investigation_test_data_db,
    ):
        """This test will attempt to put the DB in an invalid state"""

        invalid_update_json = {
            "doi": "_" * 300,
        }

        single_investigation_test_data = single_investigation_test_data_db.to_dict()

        test_response = flask_test_app_db.patch(
            f"{Config.config.datagateway_api.extension}/investigations"
            f"/{single_investigation_test_data['id']}",
            headers=valid_db_credentials_header,
            json=invalid_update_json,
        )

        print(
            "If this test is failing "
            "you may need to set sql_mode to "
            "STRICT_ALL_TABLES",
        )

        # If this test is failing
        # you may need to set sql_mode to
        # STRICT_ALL_TABLES
        assert test_response.status_code == 400
