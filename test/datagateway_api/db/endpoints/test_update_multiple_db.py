import pytest
from datagateway_api.src.common.config import Config


class TestUpdateMultipleEntities:
    def test_valid_multiple_update_data(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        multiple_investigation_test_data_db,
    ):
        expected_doi = "DB Test Data Identifier"
        expected_summary = "DB Test summary"

        update_data_list = []
        test_data_list = []

        for investigation_object in multiple_investigation_test_data_db:
            investigation = investigation_object.to_dict()
            investigation["doi"] = expected_doi
            investigation["summary"] = expected_summary

            update_entity = {
                "id": investigation["id"],
                "doi": expected_doi,
                "summary": expected_summary,
            }
            update_data_list.append(update_entity)
            test_data_list.append(investigation)

        test_response = flask_test_app_db.patch(
            f"{Config.config.datagateway_api.extension}/investigations",
            headers=valid_db_credentials_header,
            json=update_data_list,
        )

        assert test_response.json == test_data_list

    def test_valid_boundary_update_data(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        single_investigation_test_data_db,
    ):
        """ Request body is a dictionary, not a list of dictionaries"""

        expected_doi = "Test Data Identifier"
        expected_summary = "Test Summary"
        single_investigation_test_data = single_investigation_test_data_db.to_dict()

        update_data_json = {
            "id": single_investigation_test_data["id"],
            "doi": expected_doi,
            "summary": expected_summary,
        }
        single_investigation_test_data["doi"] = expected_doi
        single_investigation_test_data["summary"] = expected_summary

        test_response = flask_test_app_db.patch(
            f"{Config.config.datagateway_api.extension}/investigations",
            headers=valid_db_credentials_header,
            json=update_data_json,
        )

        assert test_response.json == [single_investigation_test_data]

    def test_invalid_missing_update_data(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        single_investigation_test_data_db,
    ):
        """There should be an ID in the request body to know which entity to update"""

        update_data_json = {
            "doi": "Test Data Identifier",
            "summary": "Test Summary",
        }

        test_response = flask_test_app_db.patch(
            f"{Config.config.datagateway_api.extension}/investigations",
            headers=valid_db_credentials_header,
            json=update_data_json,
        )

        assert test_response.status_code == 400

    @pytest.mark.parametrize(
        "update_key, update_value",
        [
            pytest.param("invalidAttr", "Some Value", id="invalid attribute"),
            pytest.param("modId", "simple/root", id="meta attribute update"),
        ],
    )
    def test_invalid_attribute_update(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        single_investigation_test_data_db,
        update_key,
        update_value,
    ):

        single_investigation_test_data = single_investigation_test_data_db.to_dict()
        invalid_update_data_json = {
            "id": single_investigation_test_data["id"],
            update_key: update_value,
        }

        test_response = flask_test_app_db.patch(
            f"{Config.config.datagateway_api.extension}/investigations",
            headers=valid_db_credentials_header,
            json=invalid_update_data_json,
        )

        assert test_response.status_code == 400
