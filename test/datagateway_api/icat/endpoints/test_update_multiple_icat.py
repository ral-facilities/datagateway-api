import pytest

from test.datagateway_api.icat.test_query import prepare_icat_data_for_assertion


class TestUpdateMultipleEntities:
    def test_valid_multiple_update_data(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        multiple_investigation_test_data,
    ):
        expected_doi = "Test Data Identifier"
        expected_summary = "Test Summary"

        update_data_list = []

        for investigation in multiple_investigation_test_data:
            investigation["doi"] = expected_doi
            investigation["summary"] = expected_summary

            update_entity = {
                "id": investigation["id"],
                "doi": expected_doi,
                "summary": expected_summary,
            }
            update_data_list.append(update_entity)

        test_response = flask_test_app_icat.patch(
            "/investigations",
            headers=valid_icat_credentials_header,
            json=update_data_list,
        )
        response_json = prepare_icat_data_for_assertion(test_response.json)

        assert response_json == multiple_investigation_test_data

    def test_valid_boundary_update_data(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        single_investigation_test_data,
    ):
        """ Request body is a dictionary, not a list of dictionaries"""

        expected_doi = "Test Data Identifier"
        expected_summary = "Test Summary"

        update_data_json = {
            "id": single_investigation_test_data[0]["id"],
            "doi": expected_doi,
            "summary": expected_summary,
        }
        single_investigation_test_data[0]["doi"] = expected_doi
        single_investigation_test_data[0]["summary"] = expected_summary

        test_response = flask_test_app_icat.patch(
            "/investigations",
            headers=valid_icat_credentials_header,
            json=update_data_json,
        )
        response_json = prepare_icat_data_for_assertion(test_response.json)

        assert response_json == single_investigation_test_data

    def test_invalid_missing_update_data(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        single_investigation_test_data,
    ):
        """There should be an ID in the request body to know which entity to update"""

        update_data_json = {
            "doi": "Test Data Identifier",
            "summary": "Test Summary",
        }

        test_response = flask_test_app_icat.patch(
            "/investigations",
            headers=valid_icat_credentials_header,
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
        flask_test_app_icat,
        valid_icat_credentials_header,
        single_investigation_test_data,
        update_key,
        update_value,
    ):
        invalid_update_data_json = {
            "id": single_investigation_test_data[0]["id"],
            update_key: update_value,
        }

        test_response = flask_test_app_icat.patch(
            "/investigations",
            headers=valid_icat_credentials_header,
            json=invalid_update_data_json,
        )

        assert test_response.status_code == 400

    def test_valid_rollback_behaviour(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        multiple_investigation_test_data,
    ):
        """
        Testing the rollback functionality when an `ICATValidationError` is thrown when
        trying to update data as per the request body.

        In this test, the first dictionary in the request body contains valid data. This
        record should be successfully updated. The second dictionary contains data that
        will throw an ICAT related exception. At this point, the rollback behaviour
        should execute, restoring the state of the first record (i.e. un-updating it)
        """

        request_body = [
            {
                "id": multiple_investigation_test_data[0]["id"],
                "summary": "An example summary for an investigation used for testing.",
            },
            {"id": multiple_investigation_test_data[1]["id"], "doi": "_" * 256},
        ]

        update_response = flask_test_app_icat.patch(
            "/investigations", headers=valid_icat_credentials_header, json=request_body,
        )

        # Get first entity that would've been successfully updated to ensure the changes
        # were rolled back when the ICATValidationError occurred for the second entity
        # in the request body
        get_response = flask_test_app_icat.get(
            f"/investigations/{multiple_investigation_test_data[0]['id']}",
            headers=valid_icat_credentials_header,
        )
        get_response_json = prepare_icat_data_for_assertion([get_response.json])

        assert update_response.status_code == 500
        # RHS encased in a list as prepare_icat_data_for_assertion() always returns list
        assert get_response_json == [multiple_investigation_test_data[0]]
