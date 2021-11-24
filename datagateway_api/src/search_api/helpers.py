import logging

from datagateway_api.src.search_api.session_handler import (
    SessionHandler,
    client_manager,
)


log = logging.getLogger()


# TODO - Make filters mandatory, if no filters are in a request an empty list will be
# given to these functions
@client_manager
def get_search(entity_name, filters=None):
    # TODO - Remove this debug logging when implementing the endpoints, this is just to
    # show the client handling works
    log.debug(
        "Client: %s, Session ID: %s",
        SessionHandler.client,
        SessionHandler.client.sessionId,
    )


@client_manager
def get_with_id(entity_name, id, filters=None):
    pass


@client_manager
def get_count(entity_name, filters=None):
    pass


@client_manager
def get_files(entity_name, filters=None):
    pass


@client_manager
def get_files_count(entity_name, id, filters=None):
    pass
