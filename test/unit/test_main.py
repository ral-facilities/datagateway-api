from unittest.mock import patch

import pytest

from datagateway_api.main import config, create_app


class TestMain:
    @pytest.mark.parametrize(
        ["datagateway_api_enabled", "read_only_api_enabled", "search_api_enabled", "root_path"],
        [
            pytest.param(True, False, False, "/datagateway-api", id="datagateway_api_enabled"),
            pytest.param(False, True, False, "/read-only-api", id="read_only_api_enabled"),
            pytest.param(False, False, True, "/search-api", id="search_api_enabled"),
        ],
    )
    def test_create_app(
        self,
        datagateway_api_enabled: bool,
        read_only_api_enabled: bool,
        search_api_enabled: bool,
        root_path: str,
    ) -> None:
        with (
            patch.object(config, "multi_api_count", new=1),
            patch("datagateway_api.main.datagateway_api_enabled", datagateway_api_enabled),
            patch("datagateway_api.main.read_only_api_enabled", read_only_api_enabled),
            patch("datagateway_api.main.search_api_enabled", search_api_enabled),
        ):
            app = create_app()

        assert app.root_path == root_path