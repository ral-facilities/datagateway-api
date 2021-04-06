from pathlib import Path
import tempfile

import pytest

from datagateway_api.common.config import Config


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
        backend_type = valid_config.get_backend_type()
        assert backend_type == "db"

    def test_invalid_backend_type(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_backend_type()


class TestGetDBURL:
    def test_valid_db_url(self, valid_config):
        db_url = valid_config.get_db_url()
        assert db_url == "mysql+pymysql://icatdbuser:icatdbuserpw@localhost:3306/icatdb"

    def test_invalid_db_url(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_db_url()


class TestICATURL:
    def test_valid_icat_url(self, valid_config):
        icat_url = valid_config.get_icat_url()
        assert icat_url == "https://localhost:8181"

    def test_invalid_icat_url(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_icat_url()


class TestICATCheckCert:
    def test_valid_icat_check_cert(self, valid_config):
        icat_check_cert = valid_config.get_icat_check_cert()
        assert icat_check_cert is False

    def test_invalid_icat_check_cert(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_icat_check_cert()


class TestGetLogLevel:
    def test_valid_log_level(self, valid_config):
        log_level = valid_config.get_log_level()
        assert log_level == "WARN"

    def test_invalid_log_level(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_log_level()


class TestGetLogLocation:
    def test_valid_log_location(self, valid_config):
        log_location = valid_config.get_log_location()
        assert (
            log_location == "/home/runner/work/datagateway-api/datagateway-api/logs.log"
        )

    def test_invalid_log_location(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_log_location()


class TestIsDebugMode:
    def test_valid_debug_mode(self, valid_config):
        debug_mode = valid_config.is_debug_mode()
        assert debug_mode is False

    def test_invalid_debug_mode(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.is_debug_mode()


class TestIsGenerateSwagger:
    def test_valid_generate_swagger(self, valid_config):
        generate_swagger = valid_config.is_generate_swagger()
        assert generate_swagger is False

    def test_invalid_generate_swagger(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.is_generate_swagger()


class TestGetHost:
    def test_valid_host(self, valid_config):
        host = valid_config.get_host()
        assert host == "127.0.0.1"

    def test_invalid_host(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_host()


class TestGetPort:
    def test_valid_port(self, valid_config):
        port = valid_config.get_port()
        assert port == "5000"

    def test_invalid_port(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_port()


class TestGetTestUserCredentials:
    def test_valid_test_user_credentials(self, valid_config):
        test_user_credentials = valid_config.get_test_user_credentials()
        assert test_user_credentials == {"username": "root", "password": "pw"}

    def test_invalid_test_user_credentials(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_test_user_credentials()


class TestGetTestMechanism:
    def test_valid_test_mechanism(self, valid_config):
        test_mechanism = valid_config.get_test_mechanism()
        assert test_mechanism == "simple"

    def test_invalid_test_mechanism(self, invalid_config):
        with pytest.raises(SystemExit):
            invalid_config.get_test_mechanism()


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
