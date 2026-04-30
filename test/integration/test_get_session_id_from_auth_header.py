from fastapi import Request


from datagateway_api.src.common.exceptions import (
    AuthenticationError,
    MissingCredentialsError,
)
from datagateway_api.src.common.helpers import get_session_id_from_auth_header


class TestGetSessionIDFromAuthHeader:
    def test_invalid_no_credentials_in_header(self, local_auth_client):
        app = local_auth_client.app

        @app.get("/")
        def test_headers_route(request: Request):  # pylint:disable=unused-variable
            get_session_id_from_auth_header(request)

        response = local_auth_client.get("/")
        assert response.status_code == MissingCredentialsError().status_code

    def test_invalid_header(self, local_auth_client, invalid_credentials_header):
        app = local_auth_client.app

        @app.get("/")
        def test_headers_route(request: Request):  # pylint:disable=unused-variable
            get_session_id_from_auth_header(request)

        response = local_auth_client.get("/", headers=invalid_credentials_header)
        assert response.status_code == AuthenticationError().status_code

    def test_valid_header(self, local_auth_client, valid_credentials_header):
        app = local_auth_client.app

        @app.get("/")
        def test_headers_route(request: Request):  # pylint:disable=unused-variable
            session_id = valid_credentials_header["Authorization"].split()[1]
            assert session_id == get_session_id_from_auth_header(request)

        response = local_auth_client.get("/", headers=valid_credentials_header)
        assert response.status_code == 200
