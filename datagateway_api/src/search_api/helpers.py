import logging

from datagateway_api.src.datagateway_api.filter_order_handler import FilterOrderHandler
from datagateway_api.src.search_api.query import SearchAPIQuery
from datagateway_api.src.search_api.session_handler import (
    client_manager,
    SessionHandler,
)


log = logging.getLogger()


@client_manager
def get_search(entity_name, filters):
    log.debug("Entity Name: %s, Filters: %s", entity_name, filters)

    query = SearchAPIQuery(entity_name)

    filter_handler = FilterOrderHandler()
    filter_handler.add_filters(filters)
    filter_handler.apply_filters(query)

    log.debug("Python ICAT Query: %s", query.icat_query.query)
    # TODO - `getApiVersion()` used as a placeholder for testing client handling
    # Replace with endpoint functionality when implementing the endpoints
    return SessionHandler.client.getApiVersion()


@client_manager
def get_with_pid(entity_name, pid, filters):
    pass


@client_manager
def get_count(entity_name, filters):
    pass


@client_manager
def get_files(entity_name, pid, filters):
    pass


@client_manager
def get_files_count(entity_name, filters, pid):
    pass
