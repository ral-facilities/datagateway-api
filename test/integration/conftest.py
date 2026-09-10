from datetime import datetime, timedelta

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from icat.client import Client

from datagateway_api.common.config import config
from datagateway_api.datagateway_api.icat.models import Session
from datagateway_api.main import app, register_common_handlers
from test.mock_data import TEST_MECHANISM, TEST_USER_CREDENTIALS


@pytest.fixture(scope="package")
def icat_client():
    client = Client(url=config.icat.url, checkCert=config.icat.check_cert)
    client.login(TEST_MECHANISM, TEST_USER_CREDENTIALS)
    return client


@pytest.fixture(scope="package")
def valid_icat_credentials_header(icat_client: Client) -> dict[str, str]:
    return {"Authorization": f"Bearer {icat_client.sessionId}"}


@pytest.fixture(name="test_client")
def fixture_test_client() -> TestClient:
    """
    Fixture for creating a test client for the application.

    :return: The test client.
    """
    return TestClient(app)


@pytest.fixture(name="local_auth_client")
def fixture_auth_test_client() -> TestClient:
    """
    Isolated TestClient for auth tests.
    """

    auth_app = FastAPI()
    register_common_handlers(auth_app)
    return TestClient(auth_app)


@pytest.fixture()
def valid_credentials_header():
    session = Session(
        id="Test",
        expireDateTime=datetime.now() + timedelta(hours=1),
        username="Test User",
    )

    yield {"Authorization": f"Bearer {session.id}"}
