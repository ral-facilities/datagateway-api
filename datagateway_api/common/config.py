import logging
import sys
from functools import cached_property
from pathlib import Path
from typing import Annotated, Optional, Self

import yaml
from pydantic import (
    AfterValidator,
    BaseModel,
    Field,
    SecretStr,
    ValidationError,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

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


DataGatewayAPIExtension = Annotated[str, AfterValidator(validate_extension)]


class APIConfig(BaseModel):
    """
    Configuration model for the API.
    """

    title: str = "Datagateway API"
    description: str = "This is the API for the Datagateway"
    url_prefix: DataGatewayAPIExtension
    reload: bool | None = None
    host: str | None = None
    port: int | None = None
    allowed_cors_headers: list[str]
    allowed_cors_origins: list[str]
    allowed_cors_methods: list[str]


class TestUserCredentials(BaseModel):
    username: str
    password: str


class TestConfig(BaseModel):
    """
    Configuration model for the tests
    """

    mechanism: str | None = None
    user_credentials: TestUserCredentials | None = None


class UseReaderForPerformance(BaseModel):
    enabled: bool
    reader_mechanism: str
    reader_username: str
    reader_password: SecretStr
    maxsize: int = Field(
        default=128,
        description="Each cacheable function will store up to this many results in memory.",
    )
    ttl: float = Field(
        default=600,
        description="Time-to-live for each of the cacheable functions in seconds.",
    )


class DataGatewayAPI(BaseModel):
    """
    Configuration model class that implements pydantic's BaseModel class to allow for
    validation of the DataGatewayAPI config data using Python type annotations.
    """

    client_cache_size: int
    client_pool_init_size: int
    client_pool_max_size: int
    extension: DataGatewayAPIExtension
    icat_check_cert: bool
    icat_url: str
    use_reader_for_performance: Optional[UseReaderForPerformance] = None

    def __getitem__(self, item):
        return getattr(self, item)


class SearchScoring(BaseModel):
    enabled: bool
    api_url: str
    api_request_timeout: int
    group: str
    limit: int


class SearchAPI(BaseModel):
    """
    Configuration model class that implements pydantic's BaseModel class to allow for
    validation of the SearchAPI config data using Python type annotations.
    """

    extension: DataGatewayAPIExtension
    icat_check_cert: bool
    icat_url: str
    mechanism: str
    username: str
    password: str
    search_scoring: SearchScoring

    def __getitem__(self, item):
        return getattr(self, item)


class Config(BaseSettings):
    """
    Overall configuration model for the application.

    It includes attributes for the API, authentication and database configurations. The class inherits from
    `BaseSettings` and automatically reads environment variables. If values are not passed in form of system environment
    variables at runtime, it will attempt to read them from the .env file.
    """

    api: APIConfig
    datagateway_api: DataGatewayAPI | None = None
    search_api: SearchAPI | None = None
    test: TestConfig | None = None

    def __getitem__(self, item):
        return getattr(self, item)

    @computed_field
    @cached_property
    def multi_api_count(self) -> int:
        return (self.datagateway_api is not None) + (self.search_api is not None)

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
            path = Path(__file__).parent.parent / "config.yaml"

        try:
            with open(path, encoding="utf-8") as target:
                data = yaml.safe_load(target)

                if "datagateway_api" not in data and "search_api" not in data:
                    log.warning(
                        "There is no API specified in the configuration file",
                    )

                return cls(**data)
        except (OSError, ValidationError) as error:
            sys.exit(f"An error occurred while trying to load the config data: {error}")

    @staticmethod
    def _validate_api_extension(
        extensions: set[DataGatewayAPIExtension],
        sub_api_config: DataGatewayAPI | SearchAPI,
    ) -> bool:
        if sub_api_config is not None:
            if sub_api_config.extension in extensions:
                raise ValueError("All api extensions must be unique.")

            extensions.add(sub_api_config.extension)

    @model_validator(mode="after")
    def _validate_api_extensions(self) -> Self:
        """
        Checks that the API extensions are not the same.
        An error is raised, at which point the application exits, if the extensions are the same.
        """
        extensions = set()
        Config._validate_api_extension(extensions=extensions, sub_api_config=self.datagateway_api)
        Config._validate_api_extension(extensions=extensions, sub_api_config=self.search_api)
        if self.multi_api_count == 0:
            raise ValueError("At least 1 API must be enabled.")
        elif self.multi_api_count > 1 and "" in extensions:
            raise ValueError("No API extension can be '/' when multiple APIs enabled.")

        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        hide_input_in_errors=True,
    )


config = Config()

print(config.model_dump_json())
