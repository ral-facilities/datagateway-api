import logging

from datagateway_api.src.common.filter_order_handler import FilterOrderHandler
from datagateway_api.src.datagateway_api.icat.filters import PythonICATIncludeFilter
from datagateway_api.src.search_api.panosc_mappings import mappings
from datagateway_api.src.search_api.query import SearchAPIQuery
from datagateway_api.src.search_api.session_handler import (
    client_manager,
    SessionHandler,
)


log = logging.getLogger()


@client_manager
def get_search(endpoint_name, entity_name, filters):
    log.debug("Entity Name: %s, Filters: %s", entity_name, filters)

    icat_relations = mappings.get_icat_relations_for_panosc_non_related_fields(
        entity_name,
    )
    # Remove any duplicate ICAT relations
    icat_relations = list(dict.fromkeys(icat_relations))
    if icat_relations:
        filters.append(PythonICATIncludeFilter(icat_relations))

    query = SearchAPIQuery(entity_name)

    filter_handler = FilterOrderHandler()
    filter_handler.add_filters(filters)
    filter_handler.apply_filters(query)

    log.debug("Python ICAT Query: %s", query.icat_query.query)
    # TODO - `getApiVersion()` used as a placeholder for testing client handling
    # Replace with endpoint functionality when implementing the endpoints
    return SessionHandler.client.getApiVersion()


@client_manager
def get_with_id(endpoint_name, entity_name, id_, filters):
    pass


@client_manager
def get_count(endpoint_name, entity_name, filters):
    pass


@client_manager
def get_files(endpoint_name, entity_name, filters):
    pass


@client_manager
def get_files_count(endpoint_name, entity_name, id_, filters):
    pass
