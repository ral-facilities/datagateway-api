import json
from unittest.mock import mock_open, patch

import pytest

from datagateway_api.src.common.config import APIConfig, validate_extension


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

    @pytest.mark.parametrize(
        "input_extension, expected_extension",
        [
            pytest.param("/", "/", id="Slash"),
            pytest.param("", "", id="Empty string, implied slash"),
            pytest.param("/datagateway-api", "/datagateway-api", id="DataGateway API"),
            pytest.param(
                "   /datagateway-api   ",
                "/datagateway-api",
                id="DataGateway API with trailing and leading spaces",
            ),
            pytest.param("/search-api", "/search-api", id="Search API"),
            pytest.param(
                "   /search-api   ",
                "/search-api",
                id="Search API with trailing and leading spaces",
            ),
        ],
    )
    def test_valid_extension_validation(self, input_extension, expected_extension):
        test_extension = validate_extension(input_extension)

        assert test_extension == expected_extension

    @pytest.mark.parametrize(
        "input_extension",
        [
            pytest.param("datagateway-api", id="DataGateway API with no leading slash"),
            pytest.param("search-api", id="Search API with no leading slash"),
            pytest.param("/my-extension/", id="Extension with trailing slash"),
        ],
    )
    def test_invalid_extension_validation(self, input_extension):
        with pytest.raises(ValueError):
            validate_extension(input_extension)
