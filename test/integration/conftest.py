from datetime import datetime, timedelta
import json
from unittest.mock import mock_open, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
from icat.client import Client
import pytest


from datagateway_api.src.common.config import APIConfig, Config
from datagateway_api.src.datagateway_api.icat.models import Session
from datagateway_api.src.main import main_app, register_common_handlers


@pytest.fixture(scope="package")
def icat_client():
    client = Client(
        Config.config.datagateway_api.icat_url,
        checkCert=Config.config.datagateway_api.icat_check_cert,
    )
    client.login(
        Config.config.test_mechanism,
        Config.config.test_user_credentials.model_dump(),
    )
    return client


@pytest.fixture(name="test_client")
def fixture_test_client() -> TestClient:
    """
    Fixture for creating a test client for the application.

    :return: The test client.
    """
    return TestClient(main_app)


@pytest.fixture(name="local_auth_client")
def fixture_auth_test_client() -> TestClient:
    """
    Isolated TestClient for auth tests.
    """

    app = FastAPI()
    register_common_handlers(app)
    return TestClient(app)


@pytest.fixture()
def valid_credentials_header():
    session = Session(
        id="Test",
        expireDateTime=datetime.now() + timedelta(hours=1),
        username="Test User",
    )

    yield {"Authorization": f"Bearer {session.id}"}


@pytest.fixture()
def test_config(test_config_data):
    with patch("builtins.open", mock_open(read_data=json.dumps(test_config_data))):
        return APIConfig.load("test/path")


@pytest.fixture()
def test_config_without_search_api(test_config_data):
    del test_config_data["search_api"]
    with patch("builtins.open", mock_open(read_data=json.dumps(test_config_data))):
        return APIConfig.load("test/path")
