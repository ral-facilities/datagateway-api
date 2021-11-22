from datetime import datetime
from unittest.mock import patch

from dateutil.tz import tzlocal
from icat.client import Client
import pytest

from datagateway_api.src.common.config import config
from datagateway_api.src.common.date_handler import DateHandler
from datagateway_api.src.common.exceptions import AuthenticationError
from datagateway_api.src.datagateway_api.backends import create_backend
from datagateway_api.src.datagateway_api.icat.filters import PythonICATWhereFilter
from datagateway_api.src.datagateway_api.icat.icat_client_pool import create_client_pool


class TestSessionHandling:
    def test_get_valid_session_details(
        self, flask_test_app_icat, valid_icat_credentials_header,
    ):
        session_details = flask_test_app_icat.get(
            "/sessions", headers=valid_icat_credentials_header,
        )

        session_expiry_datetime = DateHandler.str_to_datetime_object(
            session_details.json["expireDateTime"],
        )

        current_datetime = datetime.now(tzlocal())
        time_diff = abs(session_expiry_datetime - current_datetime)
        time_diff_minutes = time_diff.seconds / 60

        # Allows a bit of leeway for slow test execution
        assert time_diff_minutes < 120 and time_diff_minutes >= 118

        # Check username is correct
        test_mechanism = config.test_mechanism
        test_username = config.test_user_credentials.username
        assert session_details.json["username"] == f"{test_mechanism}/{test_username}"

        # Check session ID matches the header from the request
        assert (
            session_details.json["id"]
            == valid_icat_credentials_header["Authorization"].split()[1]
        )

    def test_get_invalid_session_details(
        self, bad_credentials_header, flask_test_app_icat,
    ):
        session_details = flask_test_app_icat.get(
            "/sessions", headers=bad_credentials_header,
        )

        assert session_details.status_code == 403

    def test_refresh_session(self, valid_icat_credentials_header, flask_test_app_icat):
        pre_refresh_session_details = flask_test_app_icat.get(
            "/sessions", headers=valid_icat_credentials_header,
        )

        refresh_session = flask_test_app_icat.put(
            "/sessions", headers=valid_icat_credentials_header,
        )

        post_refresh_session_details = flask_test_app_icat.get(
            "/sessions", headers=valid_icat_credentials_header,
        )

        assert refresh_session.status_code == 200

        assert (
            pre_refresh_session_details.json["expireDateTime"]
            != post_refresh_session_details.json["expireDateTime"]
        )

    @pytest.mark.usefixtures("single_investigation_test_data")
    @pytest.mark.parametrize(
        "request_body",
        [
            pytest.param(
                {
                    "username": config.test_user_credentials.username,
                    "password": config.test_user_credentials.password,
                    "mechanism": config.test_mechanism,
                },
                id="Normal request body",
            ),
            pytest.param(
                {
                    "username": config.test_user_credentials.username,
                    "password": config.test_user_credentials.password,
                },
                id="Missing mechanism in request body",
            ),
        ],
    )
    def test_valid_login(
        self, flask_test_app_icat, icat_client, icat_query, request_body,
    ):
        login_response = flask_test_app_icat.post("/sessions", json=request_body)

        icat_client.sessionId = login_response.json["sessionID"]
        icat_query.setAggregate("COUNT")
        title_filter = PythonICATWhereFilter(
            "title", "Test data for the Python ICAT Backend on DataGateway API", "like",
        )
        title_filter.apply_filter(icat_query)

        test_query = icat_client.search(icat_query)

        assert test_query == [1] and login_response.status_code == 201

    @pytest.mark.parametrize(
        "request_body, expected_response_code",
        [
            pytest.param(
                {
                    "username": "Invalid Username",
                    "password": "InvalidPassword",
                    "mechanism": config.test_mechanism,
                },
                403,
                id="Invalid credentials",
            ),
            pytest.param({}, 400, id="Missing credentials"),
        ],
    )
    def test_invalid_login(
        self, flask_test_app_icat, request_body, expected_response_code,
    ):
        login_response = flask_test_app_icat.post("/sessions", json=request_body)

        assert login_response.status_code == expected_response_code

    def test_expired_session(self):
        test_backend = create_backend("python_icat")
        client_pool = create_client_pool()
        with patch("icat.client.Client.getRemainingMinutes", return_value=-1):
            with pytest.raises(AuthenticationError):
                test_backend.get_session_details("session id", client_pool=client_pool)

    def test_valid_logout(self, flask_test_app_icat):
        client = Client(
            config.datagateway_api.icat_url,
            checkCert=config.datagateway_api.icat_check_cert,
        )
        client.login(
            config.test_mechanism, config.test_user_credentials.dict(),
        )
        creds_header = {"Authorization": f"Bearer {client.sessionId}"}

        logout_response = flask_test_app_icat.delete("/sessions", headers=creds_header)

        assert logout_response.status_code == 200

    def test_invalid_logout(self, bad_credentials_header, flask_test_app_icat):
        logout_response = flask_test_app_icat.delete(
            "/sessions", headers=bad_credentials_header,
        )

        assert logout_response.status_code == 403
