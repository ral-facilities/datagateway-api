import json
import logging
from pathlib import Path

from apispec import APISpec
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

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
from datagateway_api.src.resources.non_entities.sessions_endpoints import Sessions
from datagateway_api.src.resources.table_endpoints.table_endpoints import (
    InstrumentsFacilityCycles,
    InstrumentsFacilityCyclesCount,
    InstrumentsFacilityCyclesInvestigations,
    InstrumentsFacilityCyclesInvestigationsCount,
)
from datagateway_api.src.swagger.apispec_flask_restful import RestfulPlugin
from datagateway_api.src.swagger.initialise_spec import initialise_spec


spec = APISpec(
    title="DataGateway API",
    version="1.0",
    openapi_version="3.0.3",
    plugins=[RestfulPlugin()],
    security=[{"session_id": []}],
)


class CustomErrorHandledApi(Api):
    """
    This class overrides `handle_error` function from the API class from `flask_restful`
    to correctly return response codes and exception messages from uncaught exceptions
    """

    def handle_error(self, e):
        return str(e), e.status_code


app = Flask(__name__)
cors = CORS(app)
app.url_map.strict_slashes = False
api = CustomErrorHandledApi(app)

swaggerui_blueprint = get_swaggerui_blueprint(
    "", "/openapi.json", config={"app_name": "DataGateway API OpenAPI Spec"},
)

app.register_blueprint(swaggerui_blueprint, url_prefix="/")

setup_logger()
log = logging.getLogger()
log.info("Logging now setup")

initialise_spec(spec)

for entity_name in endpoints:
    get_endpoint_resource = get_endpoint(entity_name, endpoints[entity_name])
    api.add_resource(get_endpoint_resource, f"/{entity_name.lower()}")
    spec.path(resource=get_endpoint_resource, api=api)

    get_id_endpoint_resource = get_id_endpoint(entity_name, endpoints[entity_name])
    api.add_resource(get_id_endpoint_resource, f"/{entity_name.lower()}/<int:id_>")
    spec.path(resource=get_id_endpoint_resource, api=api)

    get_count_endpoint_resource = get_count_endpoint(
        entity_name, endpoints[entity_name],
    )
    api.add_resource(get_count_endpoint_resource, f"/{entity_name.lower()}/count")
    spec.path(resource=get_count_endpoint_resource, api=api)

    get_find_one_endpoint_resource = get_find_one_endpoint(
        entity_name, endpoints[entity_name],
    )
    api.add_resource(get_find_one_endpoint_resource, f"/{entity_name.lower()}/findone")
    spec.path(resource=get_find_one_endpoint_resource, api=api)


# Session endpoint
api.add_resource(Sessions, "/sessions")
spec.path(resource=Sessions, api=api)

# Table specific endpoints
api.add_resource(InstrumentsFacilityCycles, "/instruments/<int:id_>/facilitycycles")
spec.path(resource=InstrumentsFacilityCycles, api=api)
api.add_resource(
    InstrumentsFacilityCyclesCount, "/instruments/<int:id_>/facilitycycles/count",
)
spec.path(resource=InstrumentsFacilityCyclesCount, api=api)
api.add_resource(
    InstrumentsFacilityCyclesInvestigations,
    "/instruments/<int:instrument_id>/facilitycycles/<int:cycle_id>/investigations",
)
spec.path(resource=InstrumentsFacilityCyclesInvestigations, api=api)
api.add_resource(
    InstrumentsFacilityCyclesInvestigationsCount,
    "/instruments/<int:instrument_id>/facilitycycles/<int:cycle_id>/investigations"
    "/count",
)
spec.path(resource=InstrumentsFacilityCyclesInvestigationsCount, api=api)


if config.is_generate_swagger():
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
    app.run(
        host=config.get_host(), port=config.get_port(), debug=config.is_debug_mode(),
    )
