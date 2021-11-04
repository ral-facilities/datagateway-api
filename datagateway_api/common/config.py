import json
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


log = logging.getLogger()


class TestUserCredentials(BaseModel):
    username: StrictStr
    password: StrictStr


class APIConfig(BaseModel):
    """
    Configuration model class that implements pydantic's BaseModel class to allow for
    validation of the API config data using Python type annotations. It ensures that
    all config options exist before getting too far into the setup of the API. It takes
    the backend into account, meaning only the config options for the backend used is
    required.

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

    backend: StrictStr
    client_cache_size: Optional[StrictInt]
    client_pool_init_size: Optional[StrictInt]
    client_pool_max_size: Optional[StrictInt]
    db_url: Optional[StrictStr]
    debug_mode: StrictBool
    flask_reloader: StrictBool
    generate_swagger: StrictBool
    host: StrictStr
    icat_check_cert: Optional[StrictBool]
    icat_url: Optional[StrictStr]
    log_level: StrictStr
    log_location: StrictStr
    port: StrictStr
    test_mechanism: StrictStr
    test_user_credentials: TestUserCredentials

    @classmethod
    def load(cls, path=Path(__file__).parent.parent / "config.json"):
        """
        Loads the config data from the JSON file and returns it as a APIConfig pydantic
        model. Exits the application if it fails to locate the JSON config file or
        the APIConfig model validation fails.

        :param path: path to the configuration file
        :return: APIConfig model object that contains the config data
        """
        try:
            with open(path, encoding="utf-8") as target:
                data = json.load(target)
                return cls(**data)
        except (IOError, ValidationError) as error:
            sys.exit(f"An error occurred while trying to load the config data: {error}")

    @validator("db_url", always=True)
    def require_db_config_value(cls, value, values):  # noqa: B902, N805
        """
        By default the `db_url` config field is optional so that it does not have to be
        present in the config file if `backend` is set to `python_icat`. However, if the
        `backend` is set to `db`, this validator esentially makes the `db_url` config
        field mandatory. This means that if the an error is raised, at which point the
        application exits, if a `db_url` config value is not present in the config file.

        :param cls: :class:`APIConfig` pointer
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
        are optional so that they not have to be present in the config file if `backend`
        is set to `db`. However, if the `backend` is set to `python_icat`, this
        validator esentially makes these config fields mandatory. This means that an
        error is raised, at which point the application exits, if any of these config
        values are not present in the config file.

        :param cls: :class:`APIConfig` pointer
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
        `config.json`), it needs to be set using this function. This is required because
        creating filters in the `QueryFilterFactory` is backend-specific so the backend
        type must be fetched. This must be done using this module (rather than directly
        importing and checking the Flask app's config) to avoid circular import issues.
        """
        self.backend = backend_type

    class Config:
        validate_assignment = True


config = APIConfig.load()
