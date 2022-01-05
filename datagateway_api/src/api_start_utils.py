import json
import logging
from pathlib import Path

from apispec import APISpec
from flask_cors import CORS
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

from datagateway_api.src.common.config import Config

# Only attempt to create a DataGateway API backend if the datagateway_api object
# is present in the config. This ensures that the API does not error on startup
# due to an AttributeError exception being thrown if the object is missing.
if Config.config.datagateway_api:
    from datagateway_api.src.datagateway_api.backends import create_backend
from datagateway_api.src.datagateway_api.database.helpers import db  # noqa: I202
from datagateway_api.src.datagateway_api.icat.icat_client_pool import create_client_pool
from datagateway_api.src.resources.entities.entity_endpoint import (
    get_count_endpoint,
    get_endpoint,
    get_find_one_endpoint,
    get_id_endpoint,
)
from datagateway_api.src.resources.entities.entity_endpoint_dict import endpoints
from datagateway_api.src.resources.non_entities.ping_endpoint import ping_endpoint
from datagateway_api.src.resources.non_entities.sessions_endpoints import (
    session_endpoints,
)

if Config.config.search_api:
    from datagateway_api.src.resources.search_api_endpoints import (
        get_files_endpoint,
        get_number_count_endpoint,
        get_number_count_files_endpoint,
        get_search_endpoint,
        get_single_endpoint,
    )
from datagateway_api.src.resources.table_endpoints.table_endpoints import (  # noqa: I202, B950
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

    if Config.config.datagateway_api is not None:
        try:
            backend_type = flask_app.config["TEST_BACKEND"]
            Config.config.datagateway_api.set_backend_type(backend_type)
        except KeyError:
            backend_type = Config.config.datagateway_api.backend

        if backend_type == "db":
            flask_app.config[
                "SQLALCHEMY_DATABASE_URI"
            ] = Config.config.datagateway_api.db_url
            flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
            db.init_app(flask_app)

    initialise_spec(spec)

    return (api, spec)


def create_api_endpoints(flask_app, api, spec):
    # DataGateway API endpoints
    if Config.config.datagateway_api is not None:
        try:
            backend_type = flask_app.config["TEST_BACKEND"]
            Config.config.datagateway_api.set_backend_type(backend_type)
        except KeyError:
            backend_type = Config.config.datagateway_api.backend

        backend = create_backend(backend_type)

        icat_client_pool = None
        if backend_type == "python_icat":
            # Create client pool
            icat_client_pool = create_client_pool()

        datagateway_api_extension = Config.config.datagateway_api.extension
        for entity_name in endpoints:
            get_endpoint_resource = get_endpoint(
                entity_name,
                endpoints[entity_name],
                backend,
                client_pool=icat_client_pool,
            )
            api.add_resource(
                get_endpoint_resource,
                f"{datagateway_api_extension}/{entity_name.lower()}",
                endpoint=f"datagateway_get_{entity_name}",
            )
            spec.path(resource=get_endpoint_resource, api=api)

            get_id_endpoint_resource = get_id_endpoint(
                entity_name,
                endpoints[entity_name],
                backend,
                client_pool=icat_client_pool,
            )
            api.add_resource(
                get_id_endpoint_resource,
                f"{datagateway_api_extension}/{entity_name.lower()}/<int:id_>",
                endpoint=f"datagateway_get_id_{entity_name}",
            )
            spec.path(resource=get_id_endpoint_resource, api=api)

            get_count_endpoint_resource = get_count_endpoint(
                entity_name,
                endpoints[entity_name],
                backend,
                client_pool=icat_client_pool,
            )
            api.add_resource(
                get_count_endpoint_resource,
                f"{datagateway_api_extension}/{entity_name.lower()}/count",
                endpoint=f"datagateway_count_{entity_name}",
            )
            spec.path(resource=get_count_endpoint_resource, api=api)

            get_find_one_endpoint_resource = get_find_one_endpoint(
                entity_name,
                endpoints[entity_name],
                backend,
                client_pool=icat_client_pool,
            )
            api.add_resource(
                get_find_one_endpoint_resource,
                f"{datagateway_api_extension}/{entity_name.lower()}/findone",
                endpoint=f"datagateway_findone_{entity_name}",
            )
            spec.path(resource=get_find_one_endpoint_resource, api=api)

        # Session endpoint
        session_endpoint_resource = session_endpoints(
            backend, client_pool=icat_client_pool,
        )
        api.add_resource(
            session_endpoint_resource,
            f"{datagateway_api_extension}/sessions",
            endpoint="datagateway_sessions",
        )
        spec.path(resource=session_endpoint_resource, api=api)

        # Table specific endpoints
        instrument_facility_cycle_resource = instrument_facility_cycles_endpoint(
            backend, client_pool=icat_client_pool,
        )
        api.add_resource(
            instrument_facility_cycle_resource,
            f"{datagateway_api_extension}/instruments/<int:id_>/facilitycycles",
            endpoint="datagateway_isis_instrument_facility_cycle",
        )
        spec.path(resource=instrument_facility_cycle_resource, api=api)

        count_instrument_facility_cycle_res = count_instrument_facility_cycles_endpoint(
            backend, client_pool=icat_client_pool,
        )
        api.add_resource(
            count_instrument_facility_cycle_res,
            f"{datagateway_api_extension}/instruments/<int:id_>/facilitycycles/count",
            endpoint="datagateway_isis_count_instrument_facility_cycle",
        )
        spec.path(resource=count_instrument_facility_cycle_res, api=api)

        instrument_investigation_resource = instrument_investigation_endpoint(
            backend, client_pool=icat_client_pool,
        )
        api.add_resource(
            instrument_investigation_resource,
            f"{datagateway_api_extension}/instruments/<int:instrument_id>"
            f"/facilitycycles/<int:cycle_id>/investigations",
            endpoint="datagateway_isis_instrument_investigation",
        )
        spec.path(resource=instrument_investigation_resource, api=api)

        count_instrument_investigation_res = count_instrument_investigation_endpoint(
            backend, client_pool=icat_client_pool,
        )
        api.add_resource(
            count_instrument_investigation_res,
            f"{datagateway_api_extension}/instruments/<int:instrument_id>"
            f"/facilitycycles/<int:cycle_id>/investigations/count",
            endpoint="datagateway_isis_count_instrument_investigation",
        )
        spec.path(resource=count_instrument_investigation_res, api=api)

        # Ping endpoint
        ping_resource = ping_endpoint(backend, client_pool=icat_client_pool)
        api.add_resource(ping_resource, f"{datagateway_api_extension}/ping")
        spec.path(resource=ping_resource, api=api)

    # Search API endpoints
    if Config.config.search_api is not None:
        search_api_extension = Config.config.search_api.extension
        search_api_entity_endpoints = {
            "datasets": "Dataset",
            "documents": "Document",
            "instruments": "Instrument",
        }

        for endpoint_name, entity_name in search_api_entity_endpoints.items():
            get_search_endpoint_resource = get_search_endpoint(
                endpoint_name, entity_name,
            )
            api.add_resource(
                get_search_endpoint_resource,
                f"{search_api_extension}/{endpoint_name}",
                endpoint=f"search_api_get_{endpoint_name}",
            )
            spec.path(resource=get_search_endpoint_resource, api=api)

            get_single_endpoint_resource = get_single_endpoint(
                endpoint_name, entity_name,
            )
            api.add_resource(
                get_single_endpoint_resource,
                f"{search_api_extension}/{endpoint_name}/<int:pid>",
                endpoint=f"search_api_get_single_{endpoint_name}",
            )
            spec.path(resource=get_single_endpoint_resource, api=api)

            get_number_count_endpoint_resource = get_number_count_endpoint(
                endpoint_name, entity_name,
            )
            api.add_resource(
                get_number_count_endpoint_resource,
                f"{search_api_extension}/{endpoint_name}/count",
                endpoint=f"search_api_count_{endpoint_name}",
            )
            spec.path(resource=get_number_count_endpoint_resource, api=api)

        get_files_endpoint_resource = get_files_endpoint(
            search_api_entity_endpoints["datasets"], "datasets",
        )
        api.add_resource(
            get_files_endpoint_resource,
            f"{search_api_extension}/datasets/<int:pid>/files",
            endpoint="search_api_get_dataset_files",
        )
        spec.path(resource=get_files_endpoint_resource, api=api)

        get_number_count_files_endpoint_resource = get_number_count_files_endpoint(
            search_api_entity_endpoints["datasets"], "datasets",
        )
        api.add_resource(
            get_number_count_files_endpoint_resource,
            f"{search_api_extension}/datasets/<int:pid>/files/count",
            endpoint="search_api_count_dataset_files",
        )
        spec.path(resource=get_number_count_files_endpoint_resource, api=api)


def openapi_config(spec):
    # Reorder paths (e.g. get, patch, post) so openapi.yaml only changes when there's a
    # change to the Swagger docs, rather than changing on each startup
    if Config.config.generate_swagger:
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
