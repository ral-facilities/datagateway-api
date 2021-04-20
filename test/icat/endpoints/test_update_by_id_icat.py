from test.icat.test_query import prepare_icat_data_for_assertion


class TestUpdateByID:
    def test_valid_update_with_id(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        single_investigation_test_data,
    ):
        update_data_json = {
            "doi": "Test Data Identifier",
            "summary": "Test Summary",
            "startDate": "2019-01-04 01:01:01+00:00",
        }
        single_investigation_test_data[0].update(update_data_json)

        test_response = flask_test_app_icat.patch(
            f"/investigations/{single_investigation_test_data[0]['id']}",
            headers=valid_icat_credentials_header,
            json=update_data_json,
        )
        response_json = prepare_icat_data_for_assertion([test_response.json])

        assert response_json == single_investigation_test_data

    def test_invalid_update_with_id(
        self,
        flask_test_app_icat,
        valid_icat_credentials_header,
        single_investigation_test_data,
    ):
        """This test will attempt to put `icatdb` into an invalid state"""

        # DOI cannot be over 255 characters, which this string is
        invalid_update_json = {
            "doi": "_" * 256,
        }

        test_response = flask_test_app_icat.patch(
            f"/investigations/{single_investigation_test_data[0]['id']}",
            headers=valid_icat_credentials_header,
            json=invalid_update_json,
        )

        assert test_response.status_code == 400
