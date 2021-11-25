import json
from unittest.mock import mock_open, patch

import pytest

from datagateway_api.src.common.config import APIConfig


class TestAPIConfig:
    def test_load_with_valid_config_data(self, test_config):
        backend_type = test_config.datagateway_api.backend
        assert backend_type == "db"

    def test_load_with_no_config_data(self):
        with patch("builtins.open", mock_open(read_data="{}")):
            with pytest.raises(SystemExit):
                APIConfig.load("test/path")

    def test_load_with_missing_mandatory_config_data(self, test_config_data):
        del test_config_data["log_location"]
        with patch("builtins.open", mock_open(read_data=json.dumps(test_config_data))):
            with pytest.raises(SystemExit):
                APIConfig.load("test/path")

    def test_load_with_datagateway_api_db_backend_and_missing_db_config_data(
        self, test_config_data,
    ):
        del test_config_data["datagateway_api"]["db_url"]
        with patch("builtins.open", mock_open(read_data=json.dumps(test_config_data))):
            with pytest.raises(SystemExit):
                APIConfig.load("test/path")

    def test_load_with_datagateway_api_icat_backend_and_missing_icat_config_data(
        self, test_config_data,
    ):
        test_config_data["datagateway_api"]["backend"] = "python_icat"
        del test_config_data["datagateway_api"]["icat_url"]
        with patch("builtins.open", mock_open(read_data=json.dumps(test_config_data))):
            with pytest.raises(SystemExit):
                APIConfig.load("test/path")

    def test_load_with_invalid_api_extension_does_not_start_with_slash(
        self, test_config_data,
    ):
        test_config_data["datagateway_api"]["extension"] = "datagateway-api"
        with patch("builtins.open", mock_open(read_data=json.dumps(test_config_data))):
            with pytest.raises(SystemExit):
                APIConfig.load("test/path")

    def test_load_with_invalid_api_extension_ends_with_slash(
        self, test_config_data,
    ):
        test_config_data["search_api"]["extension"] = "/search-api/"
        with patch("builtins.open", mock_open(read_data=json.dumps(test_config_data))):
            with pytest.raises(SystemExit):
                APIConfig.load("test/path")

    def test_load_with_same_api_extensions(self, test_config_data):
        test_config_data["search_api"]["extension"] = "/datagateway-api"
        with patch("builtins.open", mock_open(read_data=json.dumps(test_config_data))):
            with pytest.raises(SystemExit):
                APIConfig.load("test/path")

    def test_set_backend_type(self, test_config):
        test_config.datagateway_api.set_backend_type("backend_name_changed")

        assert test_config.datagateway_api.backend == "backend_name_changed"
