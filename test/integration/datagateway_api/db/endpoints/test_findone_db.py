from datagateway_api.src.common.config import Config


class TestDBFindone:
    def test_valid_findone_with_filters(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        single_investigation_test_data_db,
    ):
        test_response = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/investigations/findone?where="
            '{"title": {"like": "Title for DataGateway API Testing (DB)"}}',
            headers=valid_db_credentials_header,
        )

        assert test_response.json == single_investigation_test_data_db.to_dict()

    def test_valid_no_results_findone_with_filters(
        self, flask_test_app_db, valid_db_credentials_header,
    ):
        test_response = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/investigations/findone?where="
            '{"title": {"eq": "This filter should cause a404 for testing '
            'purposes..."}}',
            headers=valid_db_credentials_header,
        )

        assert test_response.status_code == 404
