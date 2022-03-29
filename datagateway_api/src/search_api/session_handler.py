from functools import wraps
import logging
from datagateway_api.src.common.config import Config
from icat.exception import ICATSessionError

from datagateway_api.src.datagateway_api.icat.icat_client_pool import ICATClient

log = logging.getLogger()


class SessionHandler:
    """
    Class to store Python ICAT client to be used within the search API. As the API
    requires no authentication, the same client object can be used which logs in as the
    anon user
    """

    client = ICATClient(client_use="search_api")


def client_manager(method):
    """
    Decorator to manage the client object at the beginning of each request. This
    decorator checks if the client has a valid session, and if not, logs in as the anon
    user

    :param method: The function used to process an incoming request
    """

    @wraps(method)
    def wrapper_client_manager(*args, **kwargs):
        try:
            SessionHandler.client.getRemainingMinutes()
        except ICATSessionError as e:
            log.debug("Current client session expired: %s", e.args)
            SessionHandler.client.login(Config.config.search_api.plugin, {"username": Config.config.search_api.username, "password" : Config.config.search_api.password})
        return method(*args, **kwargs)

    return wrapper_client_manager
