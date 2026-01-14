import logging


from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from datagateway_api.src.auth.session_bearer import SessionBearer
from datagateway_api.src.common.config import Config
from datagateway_api.src.common.exceptions import ApiError
from datagateway_api.src.common.logger_setup import setup_logger
from datagateway_api.src.datagateway_api.icat.icat_client_pool import create_client_pool
from datagateway_api.src.datagateway_api.icat.python_icat import PythonICAT
from datagateway_api.src.datagateway_api.routers.entity import create_collection_router
from datagateway_api.src.datagateway_api.routers.ping import ping_endpoint
from datagateway_api.src.datagateway_api.routers.sessions import sessions_endpoints
from datagateway_api.src.resources.entities.entity_endpoint_dict import endpoints

datagateway_app = FastAPI(
    title="Datagateway API",
    docs_url=f"{Config.config.datagateway_api.extension}/docs",
    root_path=Config.config.url_prefix,
    separate_input_output_schemas=False,
)


setup_logger()
logger = logging.getLogger()
logger.info("Logging now setup : %s", Config.config.datagateway_api.extension)


# Exception handler for all ApiError subclasses
@datagateway_app.exception_handler(ApiError)
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
@datagateway_app.exception_handler(Exception)
async def custom_general_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    Handles all uncaught exceptions to prevent internal server errors from leaking.
    """
    logger.exception(exc)
    return JSONResponse(
        status_code=500,
        content={"message": "Something went wrong"},
    )


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


for entity_name in endpoints:
    router = create_collection_router(
        entity_name,
        endpoints[entity_name],
        python_icat,
        client_pool=icat_client_pool,
    )

    datagateway_app.include_router(
        router,
        prefix=Config.config.datagateway_api.extension,
        dependencies=[Depends(SessionBearer())],
    )

datagateway_app.include_router(
    ping_endpoint(python_icat, client_pool=icat_client_pool),
    prefix=Config.config.datagateway_api.extension,
)
datagateway_app.include_router(
    sessions_endpoints(python_icat, client_pool=icat_client_pool),
    prefix=Config.config.datagateway_api.extension,
)
