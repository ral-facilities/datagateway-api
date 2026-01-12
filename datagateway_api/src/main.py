import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from datagateway_api.src.common.config import Config
from datagateway_api.src.common.logger_setup import setup_logger
from datagateway_api.src.datagateway_api.icat.icat_client_pool import create_client_pool
from datagateway_api.src.datagateway_api.icat.python_icat import PythonICAT
from datagateway_api.src.datagateway_api.routers.ping import ping_endpoint


app = FastAPI(title="Datagateway API", root_path=Config.config.url_prefix)

setup_logger()
logger = logging.getLogger()
logger.info("Logging now setup")


@app.exception_handler(Exception)
async def custom_general_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    Custom exception handler for FastAPI to handle uncaught exceptions. It logs the error and returns an appropriate
    response.

    :param _: Unused
    :param exc: The exception object that triggered this handler.
    :return: A JSON response indicating that something went wrong.
    """
    logger.exception(exc)
    return JSONResponse(
        content={"detail": "Something went wrong"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

python_icat = PythonICAT()

# Create client pool
icat_client_pool = create_client_pool()
app.include_router(
    ping_endpoint(python_icat, client_pool=icat_client_pool),
)
