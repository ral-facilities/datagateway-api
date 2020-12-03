import json
import logging
from pathlib import Path

from apispec import APISpec
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

from datagateway_api.common.backends import create_backend
from datagateway_api.common.config import config
from datagateway_api.common.exceptions import ApiError
from datagateway_api.common.logger_setup import setup_logger
from datagateway_api.src.resources.entities.entity_endpoint import (
    get_count_endpoint,
    get_endpoint,
    get_find_one_endpoint,
    get_id_endpoint,
)
from datagateway_api.src.resources.entities.entity_map import endpoints
from datagateway_api.src.resources.non_entities.sessions_endpoints import (
    session_endpoints,
)
from datagateway_api.src.resources.table_endpoints.table_endpoints import (
    count_instrument_facility_cycles_endpoint,
    instrument_facility_cycles_endpoint,
    instrument_investigation_endpoint,
    count_instrument_investigation_endpoint,
)
from datagateway_api.src.swagger.apispec_flask_restful import RestfulPlugin
from datagateway_api.src.swagger.initialise_spec import initialise_spec

setup_logger()
log = logging.getLogger()
log.info("Logging now setup")

app = Flask(__name__)

swaggerui_blueprint = get_swaggerui_blueprint(
    "", "/openapi.json", config={"app_name": "DataGateway API OpenAPI Spec"},
)
app.register_blueprint(swaggerui_blueprint, url_prefix="/")


def create_app_infrastructure(app):
    spec = APISpec(
        title="DataGateway API",
        version="1.0",
        openapi_version="3.0.3",
        plugins=[RestfulPlugin()],
        security=[{"session_id": []}],
    )

    cors = CORS(app)
    app.url_map.strict_slashes = False
    api = Api(app)

    app.register_error_handler(ApiError, handle_error)

    initialise_spec(spec)

    return (api, spec)


def handle_error(e):
    return str(e), e.status_code


def create_api_endpoints(app, api, spec):
    try:
        backend_type = app.config["TEST_BACKEND"]
        config.set_backend_type(backend_type)
        print(f"test backend: {backend_type}")
    except KeyError:
        backend_type = config.get_backend_type()
        print(f"config backend: {backend_type}")

    # TODO - Add :param backend: to the endpoint functions
    backend = create_backend(backend_type)
    print(f"Backend: {backend}, Type: {type(backend)}")

    for entity_name in endpoints:
        get_endpoint_resource = get_endpoint(
            entity_name, endpoints[entity_name], backend
        )
        api.add_resource(get_endpoint_resource, f"/{entity_name.lower()}")
        spec.path(resource=get_endpoint_resource, api=api)

        get_id_endpoint_resource = get_id_endpoint(
            entity_name, endpoints[entity_name], backend
        )
        api.add_resource(get_id_endpoint_resource, f"/{entity_name.lower()}/<int:id_>")
        spec.path(resource=get_id_endpoint_resource, api=api)

        get_count_endpoint_resource = get_count_endpoint(
            entity_name, endpoints[entity_name], backend,
        )
        api.add_resource(get_count_endpoint_resource, f"/{entity_name.lower()}/count")
        spec.path(resource=get_count_endpoint_resource, api=api)

        get_find_one_endpoint_resource = get_find_one_endpoint(
            entity_name, endpoints[entity_name], backend,
        )
        api.add_resource(
            get_find_one_endpoint_resource, f"/{entity_name.lower()}/findone",
        )
        spec.path(resource=get_find_one_endpoint_resource, api=api)

    # Session endpoint
    session_endpoint_resource = session_endpoints(backend)
    api.add_resource(session_endpoint_resource, "/sessions")
    # spec.path(resource=session_endpoint_resource, api=api)

    # Table specific endpoints
    instrument_facility_cycle_resource = instrument_facility_cycles_endpoint(backend)
    api.add_resource(
        instrument_facility_cycle_resource, "/instruments/<int:id_>/facilitycycles"
    )
    # spec.path(resource=instrument_facility_cycle_resource, api=api)

    count_instrument_facility_cycle_resource = count_instrument_facility_cycles_endpoint(
        backend
    )
    api.add_resource(
        count_instrument_facility_cycle_resource,
        "/instruments/<int:id_>/facilitycycles/count",
    )
    # spec.path(resource=count_instrument_facility_cycle_resource, api=api)

    instrument_investigation_resource = instrument_investigation_endpoint(backend)
    api.add_resource(
        instrument_investigation_resource,
        "/instruments/<int:instrument_id>/facilitycycles/<int:cycle_id>/investigations",
    )
    # spec.path(resource=instrument_investigation_resource, api=api)

    count_instrument_investigation_resource = count_instrument_investigation_endpoint(
        backend
    )
    api.add_resource(
        count_instrument_investigation_resource,
        "/instruments/<int:instrument_id>/facilitycycles/<int:cycle_id>/investigations"
        "/count",
    )
    # spec.path(resource=count_instrument_investigation_resource, api=api)


def openapi_config(spec):
    # Reorder paths (e.g. get, patch, post) so openapi.yaml only changes when there's a
    # change to the Swagger docs, rather than changing on each startup
    log.debug("Reordering OpenAPI docs to alphabetical order")
    for entity_data in spec._paths.values():
        for endpoint_name in sorted(entity_data.keys()):
            entity_data.move_to_end(endpoint_name)

    openapi_spec_path = Path(__file__).parent / "swagger/openapi.yaml"
    with open(openapi_spec_path, "w") as f:
        f.write(spec.to_yaml())


@app.route("/openapi.json")
def specs():
    resp = app.make_response(json.dumps(spec.to_dict(), indent=2))
    resp.mimetype = "application/json"
    return resp


if __name__ == "__main__":
    api, spec = create_app_infrastructure(app)
    create_api_endpoints(app, api, spec)
    openapi_config(spec)
    app.run(
        host=config.get_host(), port=config.get_port(), debug=config.is_debug_mode(),
    )
