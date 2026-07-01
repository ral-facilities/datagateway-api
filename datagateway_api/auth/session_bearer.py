import logging


from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

log = logging.getLogger()


class SessionBearer(HTTPBearer):
    """
    Extends FastAPI's HTTPBearer class to provide session ID authentication/authorization.

    Each request to protected endpoints requires a valid session ID in the Authorization header:
        Authorization: Bearer <session_id>

    A session ID is obtained by sending a POST request to /sessions.
    """

    def __init__(self, auto_error: bool = True) -> None:
        """
        Initialize the `SessionBearer`.

        :param auto_error: If True, automatically raises HTTPException if no Authorization header is provided.
        """
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        """
        Callable method for session authentication.

        This method is called when `SessionBearer` is used as a dependency in a FastAPI route.

        :param request: FastAPI Request object
        :return: The session ID if valid
        """
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        request.state.token = credentials.credentials

        return credentials.credentials
