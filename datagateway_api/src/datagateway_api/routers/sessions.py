from datetime import datetime
import logging
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Request, status
from pydantic import BaseModel, ConfigDict, Field

from datagateway_api.src.auth.session_bearer import SessionBearer
from datagateway_api.src.common.helpers import get_session_id_from_auth_header

log = logging.getLogger()


class LoginRequest(BaseModel):
    username: str
    password: str
    mechanism: Optional[str] = "simple"


class SessionResponse(BaseModel):
    sessionID: str  # noqa: N815


class SessionDetailsResponse(BaseModel):
    id_: str = Field(alias="id")
    expireDateTime: datetime  # noqa: N815
    username: str

    model_config = ConfigDict(populate_by_name=True)


def sessions_endpoints(python_icat, **kwargs) -> APIRouter:
    """
    Generate a FastAPI APIRouter using python ICAT. In main.py
    these generated routers are included with the API e.g.
    `app.include_router(session_endpoints(python_icat), prefix="/sessions")`

    :param python_icat: The python ICAT instance used for processing requests
    :type python_icat: :class:`PythonICAT`
    :return: FastAPI APIRouter
    """

    router = APIRouter(prefix="/sessions", tags=["Sessions"])

    session_auth = SessionBearer()

    @router.post(
        "",
        summary="Login",
        description="Generates a sessionID if the user has correct credentials",
        status_code=status.HTTP_201_CREATED,
        responses={
            201: {
                "description": "Success - returns a session ID",
                "content": {"application/json": {"example": {"sessionID": "xxxxxx-yyyyyyy-zzzzzz"}}},
            },
            403: {"description": "Forbidden - User credentials were invalid"},
        },
    )
    def post(request: LoginRequest) -> SessionResponse:
        """
        Generates a sessionID if the user has correct credentials
        :return: String - SessionID
        """
        return {"sessionID": python_icat.login(request.model_dump(), **kwargs)}

    @router.delete(
        "",
        summary="Delete session",
        description="Deletes a users sessionID when they logout",
        responses={
            200: {"description": "Success - User's session was successfully deleted"},
            400: {"description": "Bad request - something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "Not Found - Unable to find session ID"},
        },
    )
    def delete(request: Request, _: Annotated[str, Depends(session_auth)]):
        """
        Deletes a users sessionID when they logout
        :return: Blank response, 200
        """

        python_icat.logout(get_session_id_from_auth_header(request), **kwargs)
        return ""

    @router.get(
        "",
        summary="Get session details",
        description="Gives details of a user's session",
        responses={
            200: {
                "description": "Success - a user's session details",
                "content": {
                    "application/json": {
                        "example": {
                            "id": "xxxxxx-yyyyyyy-zzzzzz",
                            "expiredDateTime": "2017-07-21T17:32:28Z",
                            "username": "user1",
                        },
                    },
                },
            },
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
        },
    )
    def get(request: Request, _: Annotated[str, Depends(session_auth)]) -> SessionDetailsResponse:
        """
        Gives details of a user's session
        :return: Session details
        """
        return python_icat.get_session_details(get_session_id_from_auth_header(request), **kwargs)

    @router.put(
        "",
        summary="Refresh session",
        description="Refreshes a user's session",
        responses={
            200: {
                "description": "Success - the user's session ID that has been refreshed",
            },
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
        },
    )
    def put(request: Request, _: Annotated[str, Depends(session_auth)]):
        """
        Refreshes a user's session
        :return: The session ID that has been refreshed
        """

        python_icat.refresh(get_session_id_from_auth_header(request), **kwargs)
        return ""

    return router
