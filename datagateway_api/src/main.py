import logging


from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from datagateway_api.src.auth.session_bearer import SessionBearer
from datagateway_api.src.common.config import Config
from datagateway_api.src.common.entity_endpoint_dict import endpoints
from datagateway_api.src.common.exceptions import ApiError
from datagateway_api.src.common.logger_setup import LOGGING_CONFIG_FILE_PATH, setup_logger
from datagateway_api.src.common.search_api_entity_endpoint_dict import search_api_entity_endpoints
from datagateway_api.src.datagateway_api.build_models import build_datagateway_api_model
from datagateway_api.src.datagateway_api.icat.icat_client_pool import create_client_pool
from datagateway_api.src.datagateway_api.icat.python_icat import PythonICAT
from datagateway_api.src.datagateway_api.routers.entity import create_collection_router
from datagateway_api.src.datagateway_api.routers.ping import ping_endpoint
from datagateway_api.src.datagateway_api.routers.sessions import sessions_endpoints
from datagateway_api.src.search_api.routers.entity import create_search_collection_router

datagateway_app = FastAPI(
    title="Datagateway API",
    root_path=Config.config.datagateway_api.extension,
    separate_input_output_schemas=False,
)


search_api_app = FastAPI(
    title="Search API",
    docs_url=f"{Config.config.search_api.extension}/docs",
    separate_input_output_schemas=False,
)

datagateway_app.mount(Config.config.search_api.extension, search_api_app)

setup_logger()
logger = logging.getLogger()
logger.info("Logging now setup : %s", Config.config.datagateway_api.extension)


# Exception handler for all ApiError subclasses
async def custom_api_error_handler(_: Request, exc: ApiError) -> JSONResponse:
    """
    Handles all ApiError exceptions and subclasses.
    Logs the exception and returns JSON with the correct status code and message.
    """
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


def register_common_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApiError, custom_api_error_handler)
    app.add_exception_handler(Exception, custom_general_exception_handler)


register_common_handlers(datagateway_app)
register_common_handlers(search_api_app)


datagateway_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

python_icat = PythonICAT()
# Create client pool
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

datagateway_app.include_router(
    ping_endpoint(python_icat, client_pool=icat_client_pool),
)
datagateway_app.include_router(
    sessions_endpoints(python_icat, client_pool=icat_client_pool),
)

for endpoint_name, entity_name in search_api_entity_endpoints.items():
    router = create_search_collection_router(
        entity_name,
        endpoint_name,
        add_file_endpoints=(entity_name == "Dataset"),
    )

    search_api_app.include_router(
        router,
    )


if __name__ == "__main__":
    uvicorn.run(
        "datagateway_api.src.main:datagateway_app",
        host=Config.config.host,
        port=Config.config.port,
        reload=Config.config.reload,
        log_config=LOGGING_CONFIG_FILE_PATH,
    )
