import json
from unittest.mock import mock_open, patch

import pytest

from datagateway_api.common.config import APIConfig


@pytest.fixture()
def test_config_data():
    return {
        "backend": "db",
        "client_cache_size": 5,
        "client_pool_init_size": 2,
        "client_pool_max_size": 5,
        "db_url": "mysql+pymysql://icatdbuser:icatdbuserpw@localhost:3306/icatdb",
        "flask_reloader": False,
        "icat_url": "https://localhost:8181",
        "icat_check_cert": False,
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


class TestAPIConfig:
    def test_load_with_valid_config_data(self, test_config):
        backend_type = test_config.backend
        assert backend_type == "db"

    def test_load_with_no_config_data(self):
        with patch("builtins.open", mock_open(read_data="{}")):
            with pytest.raises(SystemExit):
                APIConfig.load("test/path")

    def test_load_with_missing_mandatory_config_data(self, test_config_data):
        del test_config_data["backend"]
        with patch("builtins.open", mock_open(read_data=json.dumps(test_config_data))):
            with pytest.raises(SystemExit):
                APIConfig.load("test/path")

    def test_load_with_db_backend_and_missing_db_config_data(self, test_config_data):
        del test_config_data["db_url"]
        with patch("builtins.open", mock_open(read_data=json.dumps(test_config_data))):
            with pytest.raises(SystemExit):
                APIConfig.load("test/path")

    def test_load_with_python_icat_backend_and_missing_python_icat_config_data(
        self, test_config_data,
    ):
        test_config_data["backend"] = "python_icat"
        del test_config_data["icat_url"]
        with patch("builtins.open", mock_open(read_data=json.dumps(test_config_data))):
            with pytest.raises(SystemExit):
                APIConfig.load("test/path")

    def test_set_backend_type(self, test_config):
        test_config.set_backend_type("backend_name_changed")

        assert test_config.backend == "backend_name_changed"
