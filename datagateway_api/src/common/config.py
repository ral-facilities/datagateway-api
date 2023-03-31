import logging
from pathlib import Path
import sys
from typing import Optional

from pydantic import (
    BaseModel,
    StrictBool,
    StrictInt,
    StrictStr,
    ValidationError,
    validator,
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


class DataGatewayAPI(BaseModel):
    """
    Configuration model class that implements pydantic's BaseModel class to allow for
    validation of the DataGatewayAPI config data using Python type annotations. It takes
    the backend into account, meaning only the config options for the backend used are
    required.
    """

    backend: StrictStr
    client_cache_size: Optional[StrictInt]
    client_pool_init_size: Optional[StrictInt]
    client_pool_max_size: Optional[StrictInt]
    db_url: Optional[StrictStr]
    extension: StrictStr
    icat_check_cert: Optional[StrictBool]
    icat_url: Optional[StrictStr]

    _validate_extension = validator("extension", allow_reuse=True)(validate_extension)

    def __getitem__(self, item):
        return getattr(self, item)

    @validator("db_url", always=True)
    def require_db_config_value(cls, value, values):  # noqa: B902, N805
        """
        By default the `db_url` config field is optional so that it does not have to be
        present in the config file if `backend` is set to `python_icat`. However, if the
        `backend` is set to `db`, this validator esentially makes the `db_url` config
        field mandatory. This means that an error is raised, at which point the
        application exits, if a `db_url` config value is not present in the config file.

        :param cls: :class:`DataGatewayAPI` pointer
        :param value: The value of the given config field
        :param values: The config field values loaded before the given config field
        """
        if "backend" in values and values["backend"] == "db" and value is None:
            raise TypeError("field required")
        return value

    @validator(
        "client_cache_size",
        "client_pool_init_size",
        "client_pool_max_size",
        "icat_check_cert",
        "icat_url",
        always=True,
    )
    def require_icat_config_value(cls, value, values):  # noqa: B902, N805
        """
        By default the above config fields that are passed to the `@validator` decorator
        are optional so that they do not have to be present in the config file if
        `backend` is set to `db`. However, if the `backend` is set to `python_icat`,
        this validator esentially makes these config fields mandatory. This means that
        an error is raised, at which point the application exits, if any of these config
        values are not present in the config file.

        :param cls: :class:`DataGatewayAPI` pointer
        :param value: The value of the given config field
        :param values: The config field values loaded before the given config field
        """

        if "backend" in values and values["backend"] == "python_icat" and value is None:
            raise TypeError("field required")
        return value

    def set_backend_type(self, backend_type):
        """
        This setter is used as a way for automated tests to set the backend type. The
        API can detect if the Flask app setup is from an automated test by checking the
        app's config for a `TEST_BACKEND`. If this value exists (a KeyError will be
        raised when the API is run normally, which will then grab the backend type from
        `config.yaml`), it needs to be set using this function. This is required because
        creating filters in the `QueryFilterFactory` is backend-specific so the backend
        type must be fetched. This must be done using this module (rather than directly
        importing and checking the Flask app's config) to avoid circular import issues.
        """
        self.backend = backend_type

    class Config:
        """
        The behaviour of the BaseModel class can be controlled via this class.
        """

        # Enables assignment validation on the BaseModel fields. Useful for when the
        # backend type is changed using the set_backend_type function.
        validate_assignment = True


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

    extension: StrictStr
    icat_check_cert: StrictBool
    icat_url: StrictStr
    mechanism: StrictStr
    username: StrictStr
    password: StrictStr
    search_scoring: SearchScoring

    _validate_extension = validator("extension", allow_reuse=True)(validate_extension)

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

    datagateway_api: Optional[DataGatewayAPI]
    debug_mode: Optional[StrictBool]
    flask_reloader: Optional[StrictBool]
    generate_swagger: StrictBool
    host: Optional[StrictStr]
    log_level: StrictStr
    log_location: StrictStr
    port: Optional[StrictStr]
    search_api: Optional[SearchAPI]
    test_mechanism: Optional[StrictStr]
    test_user_credentials: Optional[TestUserCredentials]
    url_prefix: StrictStr

    _validate_extension = validator("url_prefix", allow_reuse=True)(validate_extension)

    def __getitem__(self, item):
        return getattr(self, item)

    @classmethod
    def load(cls, path=Path(__file__).parent.parent.parent / "config.yaml"):
        """
        Loads the config data from the JSON file and returns it as a APIConfig pydantic
        model. Exits the application if it fails to locate the JSON config file or
        the APIConfig model validation fails.

        :param cls: :class:`APIConfig` pointer
        :param path: path to the configuration file
        :return: APIConfig model object that contains the config data
        """
        try:
            with open(path, encoding="utf-8") as target:
                data = yaml.safe_load(target)

                if "datagateway_api" not in data and "search_api" not in data:
                    log.warning(
                        "   WARNING: There is no API specified in the "
                        "configuration file",
                    )

                return cls(**data)
        except (IOError, ValidationError) as error:
            sys.exit(f"An error occurred while trying to load the config data: {error}")

    @validator("search_api")
    def validate_api_extensions(cls, value, values):  # noqa: B902, N805
        """
        Checks that the DataGateway API and Search API extensions are not the same. An
        error is raised, at which point the application exits, if the extensions are the
        same.

        :param cls: :class:`APIConfig` pointer
        :param value: The value of the given config field
        :param values: The config field values loaded before the given config field
        """
        if (
            "datagateway_api" in values
            and values["datagateway_api"] is not None
            and value is not None
            and values["datagateway_api"].extension == value.extension
        ):
            raise ValueError(
                "extension cannot be the same as datagateway_api extension",
            )

        return value


class Config:
    """Class containing config as a class variable so it can mocked during testing"""

    config = APIConfig.load()
