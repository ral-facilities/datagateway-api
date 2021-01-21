from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

from common.config import config
from common.logger_setup import setup_logger
from src.resources.entities.entity_endpoint import (
    get_endpoint,
    get_id_endpoint,
    get_count_endpoint,
    get_find_one_endpoint,
)
from src.resources.entities.entity_map import endpoints
from src.resources.non_entities.sessions_endpoints import *
from src.resources.table_endpoints.table_endpoints import (
    InstrumentsFacilityCycles,
    InstrumentsFacilityCyclesCount,
    InstrumentsFacilityCyclesInvestigations,
    InstrumentsFacilityCyclesInvestigationsCount,
)
from common.exceptions import ApiError
from apispec import APISpec
from pathlib import Path
import json
from src.swagger.apispec_flask_restful import RestfulPlugin
from src.swagger.initialise_spec import initialise_spec


spec = APISpec(
    title="DataGateway API",
    version="1.0",
    openapi_version="3.0.3",
    plugins=[RestfulPlugin()],
    security=[{"session_id": []}],
)

app = Flask(__name__)
cors = CORS(app)
app.url_map.strict_slashes = False
api = Api(app)


def handle_error(e):
    return str(e), e.status_code


app.register_error_handler(ApiError, handle_error)


swaggerui_blueprint = get_swaggerui_blueprint(
    "", "/openapi.json", config={"app_name": "DataGateway API OpenAPI Spec"},
)

app.register_blueprint(swaggerui_blueprint, url_prefix="/")

setup_logger()
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
        entity_name, endpoints[entity_name]
    )
    api.add_resource(get_count_endpoint_resource, f"/{entity_name.lower()}/count")
    spec.path(resource=get_count_endpoint_resource, api=api)

    get_find_one_endpoint_resource = get_find_one_endpoint(
        entity_name, endpoints[entity_name]
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
    InstrumentsFacilityCyclesCount, "/instruments/<int:id_>/facilitycycles/count"
)
spec.path(resource=InstrumentsFacilityCyclesCount, api=api)
api.add_resource(
    InstrumentsFacilityCyclesInvestigations,
    "/instruments/<int:instrument_id>/facilitycycles/<int:cycle_id>/investigations",
)
spec.path(resource=InstrumentsFacilityCyclesInvestigations, api=api)
api.add_resource(
    InstrumentsFacilityCyclesInvestigationsCount,
    "/instruments/<int:instrument_id>/facilitycycles/<int:cycle_id>/investigations/count",
)
spec.path(resource=InstrumentsFacilityCyclesInvestigationsCount, api=api)

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
        host=config.get_host(), port=config.get_port(), debug=config.is_debug_mode()
    )
