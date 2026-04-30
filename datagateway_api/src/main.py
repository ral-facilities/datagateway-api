import logging


from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from datagateway_api.src.common.config import Config
from datagateway_api.src.common.exceptions import ApiError
from datagateway_api.src.common.logger_setup import LOGGING_CONFIG_FILE_PATH, setup_logger

# Check which APIs are enabled
datagateway_api_enabled = Config.config.datagateway_api is not None
search_api_enabled = Config.config.search_api is not None

if datagateway_api_enabled:
    from datagateway_api.src.datagateway_api.build_models import build_datagateway_api_model
    from datagateway_api.src.datagateway_api.icat.icat_client_pool import create_client_pool
    from datagateway_api.src.datagateway_api.icat.python_icat import PythonICAT
    from datagateway_api.src.datagateway_api.routers.entity import create_collection_router
    from datagateway_api.src.datagateway_api.routers.ping import ping_endpoint
    from datagateway_api.src.datagateway_api.routers.sessions import sessions_endpoints
    from datagateway_api.src.auth.session_bearer import SessionBearer
    from datagateway_api.src.common.entity_endpoint_dict import endpoints

if search_api_enabled:
    from datagateway_api.src.search_api.routers.entity import create_search_collection_router
    from datagateway_api.src.common.search_api_entity_endpoint_dict import search_api_entity_endpoints

setup_logger()
logger = logging.getLogger()
enabled_apis = []
if datagateway_api_enabled:
    enabled_apis.append("datagateway-api")
if search_api_enabled:
    enabled_apis.append("search-api")
logger.info("Logging now setup: %s", ", ".join(enabled_apis))


async def custom_api_error_handler(_: Request, exc: ApiError) -> JSONResponse:
    logger.exception(exc)
    return JSONResponse(
        status_code=getattr(exc, "status_code", ApiError.status_code),
        content={"message": str(exc)},
    )


# catch-all for unexpected exceptions
async def custom_general_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    Handles all uncaught exceptions to prevent internal server errors from leaking.
    """
    logger.exception(exc)
    return JSONResponse(
        status_code=500,
        content={"message": "Something went wrong"},
    )


def register_common_handlers(fastapi_app: FastAPI) -> None:
    fastapi_app.add_exception_handler(ApiError, custom_api_error_handler)
    fastapi_app.add_exception_handler(Exception, custom_general_exception_handler)


def enable_cors(fastapi_app: FastAPI) -> None:
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_datagateway_app() -> FastAPI | None:
    if datagateway_api_enabled:
        datagateway_app = FastAPI(
            title="DataGateway API",
            separate_input_output_schemas=False,
        )

        enable_cors(datagateway_app)
        register_common_handlers(datagateway_app)

        python_icat = PythonICAT()
        icat_client_pool = create_client_pool()
        dg_models = build_datagateway_api_model(client_pool=icat_client_pool)

        for endpoint_name, entity_name in endpoints.items():
            router = create_collection_router(
                endpoint_name,
                entity_name,
                dg_models,
                python_icat,
                client_pool=icat_client_pool,
            )
            datagateway_app.include_router(
                router,
                dependencies=[Depends(SessionBearer())],
            )

        datagateway_app.include_router(ping_endpoint(python_icat, client_pool=icat_client_pool))
        datagateway_app.include_router(sessions_endpoints(python_icat, client_pool=icat_client_pool))

        return datagateway_app
    return None


def create_search_api_app() -> FastAPI | None:
    if search_api_enabled:
        search_api_app = FastAPI(
            title="Search API",
            separate_input_output_schemas=False,
        )

        enable_cors(search_api_app)
        register_common_handlers(search_api_app)

        for endpoint_name, entity_name in search_api_entity_endpoints.items():
            router = create_search_collection_router(
                entity_name,
                endpoint_name,
                add_file_endpoints=(entity_name == "Dataset"),
            )
            search_api_app.include_router(router)

        return search_api_app
    return None


if datagateway_api_enabled and search_api_enabled:
    app = FastAPI(
        title="DataGateway",
        root_path=Config.config.url_prefix,
        separate_input_output_schemas=False,
    )

    app.mount(
        Config.config.datagateway_api.extension,
        create_datagateway_app(),
    )
    app.mount(
        Config.config.search_api.extension,
        create_search_api_app(),
    )

elif datagateway_api_enabled:
    app = create_datagateway_app()
    app.root_path = f"{Config.config.url_prefix}{Config.config.datagateway_api.extension}"

elif search_api_enabled:
    app = create_search_api_app()
    app.root_path = f"{Config.config.url_prefix}{Config.config.search_api.extension}"


if __name__ == "__main__":
    uvicorn.run(
        "datagateway_api.src.main:app",
        host=Config.config.host,
        port=Config.config.port,
        reload=Config.config.reload,
        log_config=LOGGING_CONFIG_FILE_PATH,
    )
