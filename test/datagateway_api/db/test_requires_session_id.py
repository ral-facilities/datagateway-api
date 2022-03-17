from datagateway_api.src.common.config import Config


class TestRequiresSessionID:
    """
    This class tests the session decorator used for the database backend. The equivalent
    decorator for the Python ICAT backend is tested in `test_session_handling.py`
    """

    def test_invalid_missing_credentials(self, flask_test_app_db):
        test_response = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/datafiles",
        )

        assert test_response.status_code == 401

    def test_invalid_credentials(self, flask_test_app_db, invalid_credentials_header):
        test_response = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/datafiles",
            headers=invalid_credentials_header,
        )

        assert test_response.status_code == 403

    def test_bad_credentials(self, flask_test_app_db, bad_credentials_header):
        test_response = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/datafiles",
            headers=bad_credentials_header,
        )

        assert test_response.status_code == 403

    def test_valid_credentials(self, flask_test_app_db, valid_db_credentials_header):
        test_response = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/datafiles?limit=0",
            headers=valid_db_credentials_header,
        )

        assert test_response.status_code == 200
