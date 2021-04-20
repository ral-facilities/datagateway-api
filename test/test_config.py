from pathlib import Path
import tempfile

import pytest

from datagateway_api.common.config import APIConfigOptions, Config


@pytest.fixture()
def test_config():
    return Config(
        path=Path(__file__).parent.parent / "datagateway_api" / "config.json.example",
    )


class TestConfig:
    def test_valid_get_config_value(self, test_config):
        backend_type = test_config.get_config_value(APIConfigOptions.BACKEND)
        assert backend_type == "db"

    def test_invalid_get_config_value(self, test_config):
        del test_config._config["backend"]
        with pytest.raises(SystemExit):
            test_config.get_config_value(APIConfigOptions.BACKEND)

    @pytest.mark.parametrize(
        "backend_type",
        [
            pytest.param("python_icat", id="Python ICAT Backend"),
            pytest.param("db", id="Database Backend"),
        ],
    )
    def test_valid_config_items_exist(self, backend_type):
        test_config = Config(
            path=Path(__file__).parent.parent
            / "datagateway_api"
            / "config.json.example",
        )
        test_config._config["backend"] = backend_type

        # Just want to check no SysExit's, so no assert is needed
        test_config._check_config_items_exist()

    def test_invalid_config_items_exist(self):
        blank_config_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".json")
        blank_config_file.write("{}")
        blank_config_file.seek(0)

        with pytest.raises(SystemExit):
            Config(path=blank_config_file.name)

    def test_valid_set_backend_type(self, test_config):
        test_config.set_backend_type("backend_name_changed")

        assert test_config._config["backend"] == "backend_name_changed"

    def test_valid_icat_properties(self, test_config):
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

        icat_properties = test_config.get_icat_properties()
        # Values could vary across versions, less likely that keys will
        assert icat_properties.keys() == example_icat_properties.keys()
