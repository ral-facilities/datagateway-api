import pytest
from pydantic import ValidationError

from datagateway_api.common.config import config, validate_extension


class TestConfig:
    def test_load_with_invalid_api_extension_does_not_start_with_slash(
        self,
        test_config_data,
    ):
        test_config_data["datagateway_api"]["extension"] = "datagateway-api"

        with pytest.raises(ValidationError):
            config.model_validate(test_config_data)

    def test_load_with_invalid_api_extension_ends_with_slash(
        self,
        test_config_data,
    ):
        test_config_data["search_api"]["extension"] = "/search-api/"

        with pytest.raises(ValidationError):
            config.model_validate(test_config_data)

    def test_load_with_same_api_extensions(self, test_config_data):
        test_config_data["search_api"]["extension"] = "/datagateway-api"

        with pytest.raises(ValidationError):
            config.model_validate(test_config_data)

    @pytest.mark.parametrize(
        "input_extension, expected_extension",
        [
            pytest.param("/", "", id="Slash"),
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
