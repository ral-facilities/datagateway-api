from pathlib import Path
import tempfile

import pytest

from datagateway_api.common.config import APIConfigOptions, Config


@pytest.fixture()
def valid_config():
    return Config(
        path=Path(__file__).parent.parent / "datagateway_api" / "config.json.example",
    )


@pytest.fixture()
def invalid_config():
    blank_config_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".json")
    blank_config_file.write("{}")
    blank_config_file.seek(0)

    return Config(path=blank_config_file.name)


class TestGetBackendType:
    def test_valid_backend_type(self, valid_config):
        backend_type = valid_config.get_config_value(APIConfigOptions.BACKEND)
        assert backend_type == "db"

    def test_invalid_backend_type(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_config_value(APIConfigOptions.BACKEND)


class TestGetDBURL:
    def test_valid_db_url(self, valid_config):
        db_url = valid_config.get_config_value(APIConfigOptions.DB_URL)
        assert db_url == "mysql+pymysql://icatdbuser:icatdbuserpw@localhost:3306/icatdb"

    def test_invalid_db_url(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_config_value(APIConfigOptions.DB_URL)


class TestIsFlaskReloader:
    def test_valid_flask_reloader(self, valid_config):
        flask_reloader = valid_config.get_config_value(APIConfigOptions.FLASK_RELOADER)
        assert flask_reloader is False

    def test_invalid_flask_reloader(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_config_value(APIConfigOptions.FLASK_RELOADER)


class TestICATURL:
    def test_valid_icat_url(self, valid_config):
        icat_url = valid_config.get_config_value(APIConfigOptions.ICAT_URL)
        assert icat_url == "https://localhost:8181"

    def test_invalid_icat_url(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_config_value(APIConfigOptions.ICAT_URL)


class TestICATCheckCert:
    def test_valid_icat_check_cert(self, valid_config):
        icat_check_cert = valid_config.get_config_value(
            APIConfigOptions.ICAT_CHECK_CERT
        )
        assert icat_check_cert is False

    def test_invalid_icat_check_cert(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_config_value(APIConfigOptions.ICAT_CHECK_CERT)


class TestGetLogLevel:
    def test_valid_log_level(self, valid_config):
        log_level = valid_config.get_config_value(APIConfigOptions.LOG_LEVEL)
        assert log_level == "WARN"

    def test_invalid_log_level(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_config_value(APIConfigOptions.LOG_LEVEL)


class TestGetLogLocation:
    def test_valid_log_location(self, valid_config):
        log_location = valid_config.get_config_value(APIConfigOptions.LOG_LOCATION)
        assert (
            log_location == "/home/runner/work/datagateway-api/datagateway-api/logs.log"
        )

    def test_invalid_log_location(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_config_value(APIConfigOptions.LOG_LOCATION)


class TestIsDebugMode:
    def test_valid_debug_mode(self, valid_config):
        debug_mode = valid_config.get_config_value(APIConfigOptions.DEBUG_MODE)
        assert debug_mode is False

    def test_invalid_debug_mode(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_config_value(APIConfigOptions.DEBUG_MODE)


class TestIsGenerateSwagger:
    def test_valid_generate_swagger(self, valid_config):
        generate_swagger = valid_config.get_config_value(
            APIConfigOptions.GENERATE_SWAGGER
        )
        assert generate_swagger is False

    def test_invalid_generate_swagger(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_config_value(APIConfigOptions.GENERATE_SWAGGER)


class TestGetHost:
    def test_valid_host(self, valid_config):
        host = valid_config.get_config_value(APIConfigOptions.HOST)
        assert host == "127.0.0.1"

    def test_invalid_host(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_config_value(APIConfigOptions.HOST)


class TestGetPort:
    def test_valid_port(self, valid_config):
        port = valid_config.get_config_value(APIConfigOptions.PORT)
        assert port == "5000"

    def test_invalid_port(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_config_value(APIConfigOptions.PORT)


class TestGetTestUserCredentials:
    def test_valid_test_user_credentials(self, valid_config):
        test_user_credentials = valid_config.get_config_value(
            APIConfigOptions.TEST_USER_CREDENTIALS
        )
        assert test_user_credentials == {"username": "root", "password": "pw"}

    def test_invalid_test_user_credentials(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_config_value(APIConfigOptions.TEST_USER_CREDENTIALS)


class TestGetTestMechanism:
    def test_valid_test_mechanism(self, valid_config):
        test_mechanism = valid_config.get_config_value(APIConfigOptions.TEST_MECHANISM)
        assert test_mechanism == "simple"

    def test_invalid_test_mechanism(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_config_value(APIConfigOptions.TEST_MECHANISM)


class TestGetICATProperties:
    def test_valid_icat_properties(self, valid_config):
        example_icat_properties = {
            "maxEntities": 10000,
            "lifetimeMinutes": 120,
            "authenticators": [
                {
                    "mnemonic": "simple",
                    "keys": [{"name": "username"}, {"name": "password", "hide": True}],
                    "friendly": "Simple",
                },
            ],
            "containerType": "Glassfish",
        }

        icat_properties = valid_config.get_icat_properties()
        # Values could vary across versions, less likely that keys will
        assert icat_properties.keys() == example_icat_properties.keys()
