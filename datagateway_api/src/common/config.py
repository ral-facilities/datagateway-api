import logging
from pathlib import Path
import sys
from typing import Annotated, Optional

from pydantic import (
    AfterValidator,
    BaseModel,
    field_validator,
    StrictBool,
    StrictInt,
    StrictStr,
    ValidationError,
)
import yaml


log = logging.getLogger()


def validate_extension(extension):
    """
    Checks that the API extension starts and does not end with a '/'. An error is
    raised, at which point the application exits, if the extension does not meet
    these validation rules.

    :param extension: The extension for the API
    """
    extension = extension.strip()

    if extension:
        if not extension.startswith("/"):
            raise ValueError("must start with '/'")
        if extension.endswith("/") and len(extension) != 1:
            raise ValueError("must not end with '/'")
        if extension == "/":
            extension = ""

    return extension


DataGatewayAPIExtension = Annotated[StrictStr, AfterValidator(validate_extension)]


class UseReaderForPerformance(BaseModel):
    enabled: StrictBool
    reader_mechanism: StrictStr
    reader_username: StrictStr
    reader_password: StrictStr


class DataGatewayAPI(BaseModel):
    """
    Configuration model class that implements pydantic's BaseModel class to allow for
    validation of the DataGatewayAPI config data using Python type annotations.
    """

    client_cache_size: StrictInt
    client_pool_init_size: StrictInt
    client_pool_max_size: StrictInt
    extension: DataGatewayAPIExtension
    icat_check_cert: StrictBool
    icat_url: StrictStr
    use_reader_for_performance: Optional[UseReaderForPerformance] = None

    def __getitem__(self, item):
        return getattr(self, item)


class SearchScoring(BaseModel):
    enabled: StrictBool
    api_url: StrictStr
    api_request_timeout: StrictInt
    group: StrictStr
    limit: StrictInt


class SearchAPI(BaseModel):
    """
    Configuration model class that implements pydantic's BaseModel class to allow for
    validation of the SearchAPI config data using Python type annotations.
    """

    extension: DataGatewayAPIExtension
    icat_check_cert: StrictBool
    icat_url: StrictStr
    mechanism: StrictStr
    username: StrictStr
    password: StrictStr
    search_scoring: SearchScoring

    def __getitem__(self, item):
        return getattr(self, item)


class TestUserCredentials(BaseModel):
    username: StrictStr
    password: StrictStr


class APIConfig(BaseModel):
    """
    Configuration model class that implements pydantic's BaseModel class to allow for
    validation of the API config data using Python type annotations. It ensures that
    all required config options exist before getting too far into the setup of the API.

    If a mandatory config option is missing or misspelled, or has a wrong value type,
    Pydantic raises a validation error with a breakdown of what was wrong and the
    application is exited.

    Config options used for testing are not checked here as they should only be used
    during tests, not in the typical running of the API.

    Some options used when running the API (host, debug_mode etc.) aren't mandatory
    when running the API in production (these options aren't used in the `wsgi.py`
    entrypoint). As a result, they're not present in `config_keys`. However, they
    are required when using `main.py` as an entrypoint. In any case of these
    specific missing config options when using that entrypoint, they are checked at
    API startup so any missing options will be caught quickly.
    """

    datagateway_api: Optional[DataGatewayAPI] = None
    debug_mode: Optional[StrictBool] = None
    generate_swagger: StrictBool
    host: Optional[StrictStr] = None
    log_level: StrictStr
    log_location: StrictStr
    port: Optional[StrictStr] = None
    search_api: Optional[SearchAPI] = None
    test_mechanism: Optional[StrictStr] = None
    url_prefix: DataGatewayAPIExtension
    test_user_credentials: Optional[TestUserCredentials] = None

    def __getitem__(self, item):
        return getattr(self, item)

    @classmethod
    def load(cls, path=None):
        """
        Loads the config data from the JSON file and returns it as a APIConfig pydantic
        model. Exits the application if it fails to locate the JSON config file or
        the APIConfig model validation fails.

        :param cls: :class:`APIConfig` pointer
        :param path: path to the configuration file
        :return: APIConfig model object that contains the config data
        """
        if path is None:
            path = Path(__file__).parent.parent.parent / "config.yaml"

        try:
            with open(path, encoding="utf-8") as target:
                data = yaml.safe_load(target)

                if "datagateway_api" not in data and "search_api" not in data:
                    log.warning(
                        "There is no API specified in the configuration file",
                    )

                return cls(**data)
        except (IOError, ValidationError) as error:
            sys.exit(f"An error occurred while trying to load the config data: {error}")

    @field_validator("search_api")
    @classmethod
    def validate_api_extensions(cls, value, info):  # noqa: B902, N805
        """
        Checks that the DataGateway API and Search API extensions are not the same. An
        error is raised, at which point the application exits, if the extensions are the
        same.

        :param cls: :class:`APIConfig` pointer
        :param value: The value of the given config field
        :param info: The config field values loaded before the given config field
        """
        if (
            "datagateway_api" in info.data
            and info.data["datagateway_api"] is not None
            and value is not None
            and info.data["datagateway_api"].extension == value.extension
        ):
            raise ValueError(
                "extension cannot be the same as datagateway_api extension",
            )

        return value


class Config:
    """Class containing config as a class variable so it can mocked during testing"""

    config = APIConfig.load()
