class TestAPIConfig:
    def test_load_with_valid_config_data(self, test_config):
        backend_type = test_config.datagateway_api.backend
        assert backend_type == "db"

    def test_set_backend_type(self, test_config):
        test_config.datagateway_api.set_backend_type("backend_name_changed")

        assert test_config.datagateway_api.backend == "backend_name_changed"
