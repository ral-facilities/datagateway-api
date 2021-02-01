import json
import logging
from pathlib import Path

from apispec import APISpec
from flask_cors import CORS
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

from datagateway_api.common.backends import create_backend
from datagateway_api.common.config import config
from datagateway_api.src.resources.entities.entity_endpoint import (
    get_count_endpoint,
    get_endpoint,
    get_find_one_endpoint,
    get_id_endpoint,
)
from datagateway_api.src.resources.entities.entity_endpoint_dict import endpoints
from datagateway_api.src.resources.non_entities.sessions_endpoints import (
    session_endpoints,
)
from datagateway_api.src.resources.table_endpoints.table_endpoints import (
    count_instrument_facility_cycles_endpoint,
    count_instrument_investigation_endpoint,
    instrument_facility_cycles_endpoint,
    instrument_investigation_endpoint,
)
from datagateway_api.src.swagger.apispec_flask_restful import RestfulPlugin
from datagateway_api.src.swagger.initialise_spec import initialise_spec

log = logging.getLogger()


class CustomErrorHandledApi(Api):
    """
    This class overrides `handle_error` function from the API class from `flask_restful`
    to correctly return response codes and exception messages from uncaught exceptions
    """

    def handle_error(self, e):
        return str(e), e.status_code


def create_app_infrastructure(flask_app):
    swaggerui_blueprint = get_swaggerui_blueprint(
        "", "/openapi.json", config={"app_name": "DataGateway API OpenAPI Spec"},
    )
    flask_app.register_blueprint(swaggerui_blueprint, url_prefix="/")
    spec = APISpec(
        title="DataGateway API",
        version="1.0",
        openapi_version="3.0.3",
        plugins=[RestfulPlugin()],
        security=[{"session_id": []}],
    )

    CORS(flask_app)
    flask_app.url_map.strict_slashes = False
    api = CustomErrorHandledApi(flask_app)

    initialise_spec(spec)

    return (api, spec)


def create_api_endpoints(flask_app, api, spec):
    try:
        backend_type = flask_app.config["TEST_BACKEND"]
        config.set_backend_type(backend_type)
    except KeyError:
        backend_type = config.get_backend_type()

    backend = create_backend(backend_type)

    for entity_name in endpoints:
        get_endpoint_resource = get_endpoint(
            entity_name, endpoints[entity_name], backend,
        )
        api.add_resource(get_endpoint_resource, f"/{entity_name.lower()}")
        spec.path(resource=get_endpoint_resource, api=api)

        get_id_endpoint_resource = get_id_endpoint(
            entity_name, endpoints[entity_name], backend,
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
    spec.path(resource=session_endpoint_resource, api=api)

    # Table specific endpoints
    instrument_facility_cycle_resource = instrument_facility_cycles_endpoint(backend)
    api.add_resource(
        instrument_facility_cycle_resource, "/instruments/<int:id_>/facilitycycles",
    )
    spec.path(resource=instrument_facility_cycle_resource, api=api)

    count_instrument_facility_cycle_res = count_instrument_facility_cycles_endpoint(
        backend,
    )
    api.add_resource(
        count_instrument_facility_cycle_res,
        "/instruments/<int:id_>/facilitycycles/count",
    )
    spec.path(resource=count_instrument_facility_cycle_res, api=api)

    instrument_investigation_resource = instrument_investigation_endpoint(backend)
    api.add_resource(
        instrument_investigation_resource,
        "/instruments/<int:instrument_id>/facilitycycles/<int:cycle_id>/investigations",
    )
    spec.path(resource=instrument_investigation_resource, api=api)

    count_instrument_investigation_resource = count_instrument_investigation_endpoint(
        backend,
    )
    api.add_resource(
        count_instrument_investigation_resource,
        "/instruments/<int:instrument_id>/facilitycycles/<int:cycle_id>/investigations"
        "/count",
    )
    spec.path(resource=count_instrument_investigation_resource, api=api)


def openapi_config(spec):
    # Reorder paths (e.g. get, patch, post) so openapi.yaml only changes when there's a
    # change to the Swagger docs, rather than changing on each startup
    if config.is_generate_swagger():
        log.debug("Reordering OpenAPI docs to alphabetical order")
        for entity_data in spec._paths.values():
            for endpoint_name in sorted(entity_data.keys()):
                entity_data.move_to_end(endpoint_name)

    openapi_spec_path = Path(__file__).parent / "swagger/openapi.yaml"
    with open(openapi_spec_path, "w") as f:
        f.write(spec.to_yaml())


def create_openapi_endpoint(app, api_spec):
    @app.route("/openapi.json")
    def specs():
        resp = app.make_response(json.dumps(api_spec.to_dict(), indent=2))
        resp.mimetype = "application/json"
        return resp
