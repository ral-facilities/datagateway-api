import pytest

from datagateway_api.src.common.exceptions import (
    AuthenticationError,
    MissingCredentialsError,
)
from datagateway_api.src.common.helpers import get_session_id_from_auth_header


class TestGetSessionIDFromAuthHeader:
    def test_invalid_no_credentials_in_header(self, flask_test_app_db):
        with flask_test_app_db:
            flask_test_app_db.get("/")
            with pytest.raises(MissingCredentialsError):
                get_session_id_from_auth_header()

    def test_invalid_header(self, flask_test_app_db, invalid_credentials_header):
        with flask_test_app_db:
            flask_test_app_db.get("/", headers=invalid_credentials_header)
            with pytest.raises(AuthenticationError):
                get_session_id_from_auth_header()

    def test_valid_header(self, flask_test_app_db, valid_db_credentials_header):
        with flask_test_app_db:
            flask_test_app_db.get("/", headers=valid_db_credentials_header)
            session_id = valid_db_credentials_header["Authorization"].split()[1]

            assert session_id == get_session_id_from_auth_header()
