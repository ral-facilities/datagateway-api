from enum import Enum
import json
import logging
from pathlib import Path
import sys

import requests


log = logging.getLogger()


class APIConfigOptions(Enum):
    """
    Class to map config keys to variables in Python - implemented for ease of
    development (IntelliSense in IDEs)
    """

    BACKEND = "backend"
    DB_URL = "db_url"
    DEBUG_MODE = "debug_mode"
    FLASK_RELOADER = "flask_reloader"
    GENERATE_SWAGGER = "generate_swagger"
    HOST = "host"
    ICAT_CHECK_CERT = "icat_check_cert"
    ICAT_URL = "icat_url"
    LOG_LEVEL = "log_level"
    LOG_LOCATION = "log_location"
    PORT = "port"
    TEST_MECHANISM = "test_mechanism"
    TEST_USER_CREDENTIALS = "test_user_credentials"


class Config(object):
    def __init__(self, path=Path(__file__).parent.parent / "config.json"):
        self.path = path
        with open(self.path) as target:
            self._config = json.load(target)

        self._check_config_items_exist()

    def _check_config_items_exist(self):
        """
        A function to check that all config options exist before getting too far into
        the setup of the API. This check takes the backend into account, meaning only
        the config options for the backend used is required

        Config options used for testing are not checked here as they should only be used
        during tests, not in the typical running of the API

        If a config option is missing, this will be picked up in `get_config_value()` by
        exiting the application
        """
        # These keys are non-backend specific and therefore are mandatory for all uses
        config_keys = [
            APIConfigOptions.BACKEND,
            APIConfigOptions.DEBUG_MODE,
            APIConfigOptions.FLASK_RELOADER,
            APIConfigOptions.GENERATE_SWAGGER,
            APIConfigOptions.HOST,
            APIConfigOptions.LOG_LEVEL,
            APIConfigOptions.LOG_LOCATION,
            APIConfigOptions.PORT,
        ]

        if self.get_config_value(APIConfigOptions.BACKEND) == "python_icat":
            icat_backend_specific_config_keys = [
                APIConfigOptions.ICAT_CHECK_CERT,
                APIConfigOptions.ICAT_URL,
            ]
            config_keys.extend(icat_backend_specific_config_keys)
        elif self.get_config_value(APIConfigOptions.BACKEND) == "db":
            db_backend_specific_config_keys = [APIConfigOptions.DB_URL]
            config_keys.extend(db_backend_specific_config_keys)

        for key in config_keys:
            self.get_config_value(key)

    def get_config_value(self, config_key):
        """
        Given a config key, the corresponding config value is returned

        :param config_key: Enum of a configuration key that's in `config.json`
        :type config_key: :class:`APIConfigOptions`
        :return: Config value of the given key
        """
        try:
            return self._config[config_key.value]
        except KeyError:
            sys.exit(f"Missing config value: {config_key}")

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
        self._config["backend"] = backend_type

    def get_icat_properties(self):
        """
        ICAT properties can be retrieved using Python ICAT's client object, however this
        requires the client object to be authenticated which may not always be the case
        when requesting these properties, hence a HTTP request is sent as an alternative
        """
        properties_url = (
            f"{config.get_config_value(APIConfigOptions.ICAT_URL)}/icat/properties"
        )
        r = requests.request(
            "GET",
            properties_url,
            verify=config.get_config_value(APIConfigOptions.ICAT_CHECK_CERT),
        )
        icat_properties = r.json()

        return icat_properties


config = Config()
