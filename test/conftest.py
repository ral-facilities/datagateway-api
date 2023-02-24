import json
from unittest.mock import mock_open, patch

from icat.query import Query
import pytest

from datagateway_api.src.common.config import APIConfig


@pytest.fixture()
def icat_query(icat_client):
    return Query(icat_client, "Investigation")


@pytest.fixture()
def bad_credentials_header():
    return {"Authorization": "Bearer Invalid"}


@pytest.fixture()
def invalid_credentials_header():
    return {"Authorization": "Test"}


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
            "mechanism": "anon",
            "username": "",
            "password": "",
            "search_scoring": {
                "enabled": False,
                "api_url": "http://localhost:9000/score",
                "api_request_timeout": 5,
                "group": "documents",
                "limit": 1000,
            },
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
