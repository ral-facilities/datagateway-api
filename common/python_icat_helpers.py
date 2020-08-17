from functools import wraps
import logging
from datetime import datetime, timedelta


import icat.client
from icat.exception import ICATSessionError

from common.exceptions import AuthenticationError
from common.config import config

log = logging.getLogger()


def requires_session_id(method):
    """
    Decorator for Python ICAT backend methods that looks out for session errors when using the API.
    The API call runs and an ICATSessionError may be raised due to an expired session, invalid 
    session ID etc.

    The session ID from the request is set here, so there is no requirement for a user to use the
    login endpoint, they can go straight into using the API so long as they have a valid session ID
    (be it created from this API, or from an alternative such as scigateway-auth).

    This assumes the session ID is the second argument of the function where this decorator is
    applied, which is reasonable to assume considering the current method signatures of all the
    endpoints.

    :param method: The method for the backend operation
    :raises AuthenticationError, if a valid session_id is not provided with the request
    """

    @wraps(method)
    def wrapper_requires_session(*args, **kwargs):
        try:
            client = create_client()
            client.sessionId = args[1]
            # Client object put into kwargs so it can be accessed by backend functions
            kwargs["client"] = client

            # Find out if session has expired
            session_time = client.getRemainingMinutes()
            log.info("Session time: {}".format(session_time))

            if session_time < 0:
                raise AuthenticationError("Forbidden")
            else:
                return method(*args, **kwargs)
        except ICATSessionError:
            raise AuthenticationError("Forbidden")

    return wrapper_requires_session


def queries_records(method):
    """
    Docstring
    """

    @wraps(method)
    def wrapper_gets_records(*args, **kwargs):
        pass

    return wrapper_gets_records


def create_client():
    client = icat.client.Client(
        config.get_icat_url(), checkCert=config.get_icat_check_cert()
    )
    return client


def get_session_details_helper(client):
    # Remove rounding
    session_time_remaining = client.getRemainingMinutes()
    session_expiry_time = datetime.now() + timedelta(minutes=session_time_remaining)

    username = client.getUserName()

    return {
        "ID": client.sessionId,
        "EXPIREDATETIME": str(session_expiry_time),
        "USERNAME": username,
    }


def logout_icat_client(client):
    client.logout()


def refresh_client_session(client):
    client.refresh()
