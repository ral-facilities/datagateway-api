from datetime import datetime

from icat.client import Client
import pytest

from datagateway_api.common.config import config
from datagateway_api.common.icat.filters import PythonICATWhereFilter


class TestSessionHandling:
    def test_session_id_decorator(self):
        pass

    def test_get_valid_session_details(self, flask_test_app, valid_credentials_header):
        session_details = flask_test_app.get(
            "/sessions", headers=valid_credentials_header,
        )

        print(f"JSON: {session_details.json}, Code: {session_details.status_code}")

        # Check username is correct
        assert (
            session_details.json["USERNAME"] == f"{config.get_test_mechanism()}/"
            f"{config.get_test_user_credentials()['username']}"
        )
        # Check session ID matches the header from the request
        assert (
            session_details.json["ID"]
            == valid_credentials_header["Authorization"].split()[1]
        )

        session_expiry_datetime = datetime.strptime(
            session_details.json["EXPIREDATETIME"], "%Y-%m-%d %H:%M:%S.%f",
        )
        current_datetime = datetime.now()
        time_diff = abs(session_expiry_datetime - current_datetime)
        time_diff_minutes = time_diff.seconds / 60

        # Allows a bit of leeway for slow test execution
        assert time_diff_minutes < 120 and time_diff_minutes >= 118

    def test_get_invalid_session_details(
        self, invalid_credentials_header, flask_test_app,
    ):
        session_details = flask_test_app.get(
            "/sessions", headers=invalid_credentials_header,
        )

        assert session_details.status_code == 403

    def test_refresh_session(self, valid_credentials_header, flask_test_app):
        pre_refresh_session_details = flask_test_app.get(
            "/sessions", headers=valid_credentials_header,
        )

        refresh_session = flask_test_app.put(
            "/sessions", headers=valid_credentials_header,
        )
        assert refresh_session.status_code == 200

        post_refresh_session_details = flask_test_app.get(
            "/sessions", headers=valid_credentials_header,
        )

        assert (
            pre_refresh_session_details.json["EXPIREDATETIME"]
            != post_refresh_session_details.json["EXPIREDATETIME"]
        )

    @pytest.mark.usefixtures("single_investigation_test_data")
    def test_valid_login(self, flask_test_app, icat_client, icat_query):
        user_credentials = config.get_test_user_credentials()

        login_json = {
            "username": user_credentials["username"],
            "password": user_credentials["password"],
            "mechanism": config.get_test_mechanism(),
        }
        login_response = flask_test_app.post("/sessions", json=login_json)

        icat_client.sessionId = login_response.json["sessionID"]
        icat_query.setAggregate("COUNT")
        title_filter = PythonICATWhereFilter(
            "title", "Test data for the Python ICAT Backend on DataGateway API", "eq",
        )
        title_filter.apply_filter(icat_query)

        test_query = icat_client.search(icat_query)

        assert test_query == [1] and login_response.status_code == 201

    def test_invalid_login(self, flask_test_app):
        login_json = {
            "username": "Invalid Username",
            "password": "InvalidPassword",
            "mechanism": config.get_test_mechanism(),
        }
        login_response = flask_test_app.post("/sessions", json=login_json)

        assert login_response.status_code == 403

    def test_valid_logout(self, flask_test_app):
        client = Client(config.get_icat_url(), checkCert=config.get_icat_check_cert())
        client.login(config.get_test_mechanism(), config.get_test_user_credentials())
        creds_header = {"Authorization": f"Bearer {client.sessionId}"}

        logout_response = flask_test_app.delete("/sessions", headers=creds_header)

        assert logout_response.status_code == 200

    def test_invalid_logout(self, invalid_credentials_header, flask_test_app):
        logout_response = flask_test_app.delete(
            "/sessions", headers=invalid_credentials_header,
        )

        assert logout_response.status_code == 403
