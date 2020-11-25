from test.icat.test_query import prepare_icat_data_for_assertion


class TestUpdateByID:
    def test_valid_update_with_id(
        self, flask_test_app, valid_credentials_header, single_investigation_test_data,
    ):
        expected_doi = "Test Data Identifier"
        expected_summary = "Test Summary"

        update_data_json = {
            "doi": expected_doi,
            "summary": expected_summary,
        }
        single_investigation_test_data[0]["doi"] = expected_doi
        single_investigation_test_data[0]["summary"] = expected_summary

        test_response = flask_test_app.patch(
            f"/investigations/{single_investigation_test_data[0]['id']}",
            headers=valid_credentials_header,
            json=update_data_json,
        )
        response_json = prepare_icat_data_for_assertion([test_response.json])

        assert response_json == single_investigation_test_data

    def test_invalid_update_with_id(
        self, flask_test_app, valid_credentials_header, single_investigation_test_data,
    ):
        """This test will attempt to put `icatdb` into an invalid state"""

        # DOI cannot be over 255 characters, which this string is
        invalid_update_json = {
            "doi": "__________________________________________________________________"
            "_________________________________________________________________________"
            "_________________________________________________________________________"
            "_________________________________________________________________________",
        }

        test_response = flask_test_app.patch(
            f"/investigations/{single_investigation_test_data[0]['id']}",
            headers=valid_credentials_header,
            json=invalid_update_json,
        )

        assert test_response.status_code == 400
