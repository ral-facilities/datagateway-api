from datetime import datetime, timedelta
import json
from unittest.mock import mock_open, patch

from flask import Flask
from icat.client import Client
from icat.query import Query
import pytest

from datagateway_api.src.api_start_utils import (
    create_api_endpoints,
    create_app_infrastructure,
)
from datagateway_api.src.common.config import APIConfig, Config
from datagateway_api.src.datagateway_api.database.helpers import (
    delete_row_by_id,
    insert_row_into_table,
)
from datagateway_api.src.datagateway_api.database.models import SESSION


@pytest.fixture(scope="package")
def icat_client():
    client = Client(
        Config.config.datagateway_api.icat_url,
        checkCert=Config.config.datagateway_api.icat_check_cert,
    )
    client.login(
        Config.config.test_mechanism, Config.config.test_user_credentials.dict(),
    )
    return client


@pytest.fixture()
def icat_query(icat_client):
    return Query(icat_client, "Investigation")


@pytest.fixture()
def bad_credentials_header():
    return {"Authorization": "Bearer Invalid"}


@pytest.fixture()
def invalid_credentials_header():
    return {"Authorization": "Test"}


@pytest.fixture(scope="package")
def flask_test_app():
    """This is used to check the endpoints exist and have the correct HTTP methods"""
    test_app = Flask(__name__)
    api, spec = create_app_infrastructure(test_app)
    create_api_endpoints(test_app, api, spec)

    yield test_app


@pytest.fixture(scope="package")
def flask_test_app_db():
    """
    This is in the common conftest file because this test app is also used in
    non-backend specific tests
    """
    db_app = Flask(__name__)
    db_app.config["TESTING"] = True
    db_app.config["TEST_BACKEND"] = "db"

    api, spec = create_app_infrastructure(db_app)
    create_api_endpoints(db_app, api, spec)
    db_app.app_context().push()

    yield db_app.test_client()


@pytest.fixture()
def valid_db_credentials_header():
    session = SESSION()
    session.id = "Test"
    session.expireDateTime = datetime.now() + timedelta(hours=1)
    session.username = "Test User"

    insert_row_into_table(SESSION, session)

    yield {"Authorization": f"Bearer {session.id}"}

    delete_row_by_id(SESSION, "Test")


@pytest.fixture()
def test_config_data():
    return {
        "datagateway_api": {
            "extension": "/datagateway-api",
            "backend": "db",
            "client_cache_size": 5,
            "client_pool_init_size": 2,
            "client_pool_max_size": 5,
            "db_url": "mysql+pymysql://icatdbuser:icatdbuserpw@localhost:3306/icatdb",
            "icat_url": "https://localhost:8181",
            "icat_check_cert": False,
        },
        "search_api": {
            "extension": "/search-api",
            "icat_url": "https://localhost.testdomain:8181",
            "icat_check_cert": True,
        },
        "flask_reloader": False,
        "log_level": "WARN",
        "log_location": "/home/runner/work/datagateway-api/datagateway-api/logs.log",
        "debug_mode": False,
        "generate_swagger": False,
        "host": "127.0.0.1",
        "port": "5000",
        "test_user_credentials": {"username": "root", "password": "pw"},
        "test_mechanism": "simple",
    }


@pytest.fixture()
def test_config(test_config_data):
    with patch("builtins.open", mock_open(read_data=json.dumps(test_config_data))):
        return APIConfig.load("test/path")


@pytest.fixture()
def test_config_without_search_api(test_config_data):
    del test_config_data["search_api"]
    with patch("builtins.open", mock_open(read_data=json.dumps(test_config_data))):
        return APIConfig.load("test/path")
