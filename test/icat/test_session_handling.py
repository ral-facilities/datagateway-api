from datetime import datetime

from icat.client import Client
import pytest

from datagateway_api.common.config import config
from datagateway_api.common.icat.filters import PythonICATWhereFilter


class TestSessionHandling:
    def test_get_valid_session_details(
        self, flask_test_app_icat, valid_icat_credentials_header,
    ):
        session_details = flask_test_app_icat.get(
            "/sessions", headers=valid_icat_credentials_header,
        )

        session_expiry_datetime = datetime.strptime(
            session_details.json["EXPIREDATETIME"], "%Y-%m-%d %H:%M:%S.%f",
        )
        current_datetime = datetime.now()
        time_diff = abs(session_expiry_datetime - current_datetime)
        time_diff_minutes = time_diff.seconds / 60

        # Allows a bit of leeway for slow test execution
        assert time_diff_minutes < 120 and time_diff_minutes >= 118

        # Check username is correct
        assert (
            session_details.json["USERNAME"] == f"{config.get_test_mechanism()}/"
            f"{config.get_test_user_credentials()['username']}"
        )

        # Check session ID matches the header from the request
        assert (
            session_details.json["ID"]
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
            pre_refresh_session_details.json["EXPIREDATETIME"]
            != post_refresh_session_details.json["EXPIREDATETIME"]
        )

    @pytest.mark.usefixtures("single_investigation_test_data")
    def test_valid_login(self, flask_test_app_icat, icat_client, icat_query):
        user_credentials = config.get_test_user_credentials()

        login_json = {
            "username": user_credentials["username"],
            "password": user_credentials["password"],
            "mechanism": config.get_test_mechanism(),
        }
        login_response = flask_test_app_icat.post("/sessions", json=login_json)

        icat_client.sessionId = login_response.json["sessionID"]
        icat_query.setAggregate("COUNT")
        title_filter = PythonICATWhereFilter(
            "title", "Test data for the Python ICAT Backend on DataGateway API", "like",
        )
        title_filter.apply_filter(icat_query)

        test_query = icat_client.search(icat_query)

        assert test_query == [1] and login_response.status_code == 201

    def test_invalid_login(self, flask_test_app_icat):
        login_json = {
            "username": "Invalid Username",
            "password": "InvalidPassword",
            "mechanism": config.get_test_mechanism(),
        }
        login_response = flask_test_app_icat.post("/sessions", json=login_json)

        assert login_response.status_code == 403

    def test_valid_logout(self, flask_test_app_icat):
        client = Client(config.get_icat_url(), checkCert=config.get_icat_check_cert())
        client.login(config.get_test_mechanism(), config.get_test_user_credentials())
        creds_header = {"Authorization": f"Bearer {client.sessionId}"}

        logout_response = flask_test_app_icat.delete("/sessions", headers=creds_header)

        assert logout_response.status_code == 200

    def test_invalid_logout(self, bad_credentials_header, flask_test_app_icat):
        logout_response = flask_test_app_icat.delete(
            "/sessions", headers=bad_credentials_header,
        )

        assert logout_response.status_code == 403
