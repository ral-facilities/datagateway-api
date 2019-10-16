from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from common.config import config
from common.logger_setup import setup_logger
from src.resources.entities.entity_endpoint import get_endpoint, get_id_endpoint, get_count_endpoint, \
    get_find_one_endpoint
from src.resources.entities.entity_map import endpoints
from src.resources.non_entities.sessions_endpoints import *
from src.resources.table_endpoints.table_endpoints import UsersInvestigations, UsersInvestigationsCount, \
    InstrumentsFacilityCycles, InstrumentsFacilityCyclesCount, InstrumentsFacilityCyclesInvestigations, \
    InstrumentsFacilityCyclesInvestigationsCount
from src.swagger.swagger_generator import swagger_gen

swagger_gen.write_swagger_spec()

app = Flask(__name__)
cors = CORS(app)
app.url_map.strict_slashes = False
api = Api(app)

setup_logger()

for entity_name in endpoints:
    api.add_resource(get_endpoint(entity_name, endpoints[entity_name]), f"/{entity_name.lower()}")
    api.add_resource(get_id_endpoint(entity_name, endpoints[entity_name]), f"/{entity_name.lower()}/<int:id>")
    api.add_resource(get_count_endpoint(entity_name, endpoints[entity_name]), f"{entity_name.lower()}/count")
    api.add_resource(get_find_one_endpoint(entity_name, endpoints[entity_name]), f"{entity_name.lower()}/findone")

# Session endpoint
api.add_resource(Sessions, "/sessions")

# Table specific endpoints
api.add_resource(UsersInvestigations, "/users/<int:id>/investigations")
api.add_resource(UsersInvestigationsCount, "/users/<int:id>/investigations/count")
api.add_resource(InstrumentsFacilityCycles, "/instruments/<int:id>/facilitycycles")
api.add_resource(InstrumentsFacilityCyclesCount, "/instruments/<int:id>/facilitycycles/count")
api.add_resource(InstrumentsFacilityCyclesInvestigations,
                 "/instruments/<int:instrument_id>/facilitycycles/<int:cycle_id>/investigations")
api.add_resource(InstrumentsFacilityCyclesInvestigationsCount,
                 "/instruments/<int:instrument_id>/facilitycycles/<int:cycle_id>/investigations/count")

if __name__ == "__main__":
    app.run(host=config.get_host(), port=config.get_port())
    app.run(debug=config.is_debug_mode())
