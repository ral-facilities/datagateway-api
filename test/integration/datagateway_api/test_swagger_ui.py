import json
from unittest.mock import mock_open, patch

from flask import Flask
import pytest
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

from datagateway_api.src.api_start_utils import (
    create_api_endpoints,
    create_app_infrastructure,
    create_openapi_endpoints,
)
from datagateway_api.src.common.config import APIConfig


@pytest.fixture(params=["", "/url-prefix"], ids=["No URL prefix", "Given a URL prefix"])
def test_config_swagger(test_config_data, request):
    test_config_data["url_prefix"] = request.param
    test_config_data["datagateway_api"]["extension"] = (
        "" if request.param == "" else "/datagateway-api"
    )
    test_config_data["search_api"]["extension"] = (
        "/search-api" if request.param == "" else ""
    )

    with patch("builtins.open", mock_open(read_data=json.dumps(test_config_data))):
        return APIConfig.load("test/path")


class TestSwaggerUI:
    @pytest.mark.parametrize(
        "api_type",
        [
            pytest.param("datagateway_api", id="DataGateway API"),
            pytest.param("search_api", id="Search API"),
        ],
    )
    def test_swagger_ui(self, test_config_swagger, api_type, request):
        # derived from the param IDs set above, used to assert the page title
        api_name = request.node.callspec.id.split("-")[1]
        with patch(
            "datagateway_api.src.common.config.Config.config", test_config_swagger,
        ):
            test_app = Flask(__name__)
            api, spec = create_app_infrastructure(test_app)
            create_api_endpoints(test_app, api, spec)
            create_openapi_endpoints(test_app, spec)
            test_app.wsgi_app = DispatcherMiddleware(
                Response("Not Found", status=404),
                {test_config_swagger.url_prefix: test_app.wsgi_app},
            )
            test_client = test_app.test_client()

            test_response = test_client.get(
                f"{test_config_swagger.url_prefix}{test_config_swagger[api_type].extension}",  # noqa: B950
            )

            test_response_string = test_response.get_data(as_text=True)

            assert f"{api_name} OpenAPI Spec" in test_response_string
            assert (
                f"{test_config_swagger.url_prefix}{test_config_swagger[api_type].extension}/swagger-ui"  # noqa: B950
                in test_response_string
            )
            assert (
                f"{test_config_swagger.url_prefix}/{api_type.replace('_', '-')}/openapi.json"  # noqa: B950
                in test_response_string
            )
