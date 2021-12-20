import logging

from datagateway_api.src.datagateway_api.filter_order_handler import FilterOrderHandler
from datagateway_api.src.search_api.query import SearchAPIQuery
from datagateway_api.src.search_api.session_handler import (
    client_manager,
    SessionHandler,
)


log = logging.getLogger()


# TODO - Make filters mandatory, if no filters are in a request an empty list will be
# given to these functions
@client_manager
def get_search(endpoint_name, entity_name, filters=[]):
    log.debug("Entity Name: %s, Filters: %s", entity_name, filters)

    query = SearchAPIQuery(entity_name)

    filter_handler = FilterOrderHandler()
    filter_handler.add_filters(filters)
    filter_handler.add_query_to_where_filters(query)
    filter_handler.apply_filters(query)

    log.debug("Python ICAT Query: %s", query.query.query)
    # TODO - `getApiVersion()` used as a placeholder for testing client handling
    # Replace with endpoint functionality when implementing the endpoints
    return SessionHandler.client.getApiVersion()


@client_manager
def get_with_id(endpoint_name, entity_name, id_, filters=None):
    pass


@client_manager
def get_count(endpoint_name, entity_name, filters=None):
    pass


@client_manager
def get_files(endpoint_name, entity_name, filters=None):
    pass


@client_manager
def get_files_count(endpoint_name, entity_name, id_, filters=None):
    pass
