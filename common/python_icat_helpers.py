from functools import wraps
import logging
from datetime import datetime, timedelta


from icat.exception import ICATSessionError
from common.exceptions import AuthenticationError

log = logging.getLogger()

def requires_session_id(method):
    """
    Decorator for Python ICAT backend methods that looks out for session errors when using the API.
    The API call runs and an ICATSessionError may be raised due to an expired session, invalid 
    session ID etc.
    It expects that session_id is the second argument supplied to the function  
    :param method: The method for the backend operation
    :raises AuthenticationError, if a valid session_id is not provided with the request
    """

    @wraps(method)
    def wrapper_requires_session(*args, **kwargs):
        try:
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

