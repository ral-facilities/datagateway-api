from typing import Literal

from fastapi import APIRouter, HTTPException

from datagateway_api.src.common.constants import Constants


def ping_endpoint(python_icat, **kwargs) -> APIRouter:
    """
    Generate a FastAPI router using python ICAT.
    In main.py these routers are included e.g.
    `app.include_router(ping_endpoint(python_icat), prefix="/ping")`

    :param python_icat: The python ICAT instance used for processing requests
    :type python_icat: PythonICAT
    :return: FastAPI APIRouter
    """

    router = APIRouter(prefix="/ping", tags=["Ping"])

    @router.get(
        "",
        summary="Ping API connection method",
        description="Pings the API's connection method to check responsiveness",
        response_model=Literal[Constants.PING_OK_RESPONSE],
        response_description="OK message",
        responses={
            200: {
                "description": "Success - the API is responsive on the python ICAT server",
                "content": {"application/json": {"example": "DataGateway API OK"}},
            },
            500: {"description": "Pinging the API's connection method has gone wrong"},
        },
    )
    def ping():
        try:
            return python_icat.ping(**kwargs)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    return router
