import logging

from flask_restful import Resource

from datagateway_api.src.common.helpers import get_filters_from_query_string
from datagateway_api.src.search_api.helpers import (
    get_count,
    get_files,
    get_files_count,
    get_search,
    get_with_id,
)

log = logging.getLogger()


def get_search_endpoint(endpoint_name, entity_name):
    """
    TODO - Add docstring
    """

    class Endpoint(Resource):
        def get(self):
            filters = get_filters_from_query_string("search_api", entity_name)
            log.debug("Filters: %s", filters)
            return get_search(endpoint_name, entity_name, filters), 200

        # TODO - Add `get.__doc__`

    Endpoint.__name__ = entity_name
    return Endpoint


def get_single_endpoint(endpoint_name, entity_name):
    """
    TODO - Add docstring
    """

    class EndpointWithID(Resource):
        def get(self, pid):
            filters = get_filters_from_query_string("search_api", entity_name)
            log.debug("Filters: %s", filters)
            return get_with_id(entity_name, pid), 200

        # TODO - Add `get.__doc__`

    EndpointWithID.__name__ = entity_name
    return EndpointWithID


def get_number_count_endpoint(endpoint_name, entity_name):
    """
    TODO - Add docstring
    """

    class CountEndpoint(Resource):
        def get(self):
            # Only WHERE included on count endpoints
            filters = get_filters_from_query_string("search_api", entity_name)
            log.debug("Filters: %s", filters)
            return get_count(entity_name), 200

        # TODO - Add `get.__doc__`

    CountEndpoint.__name__ = entity_name
    return CountEndpoint


def get_files_endpoint(endpoint_name, entity_name):
    """
    TODO - Add docstring
    """

    class FilesEndpoint(Resource):
        def get(self, pid):
            filters = get_filters_from_query_string("search_api", entity_name)
            log.debug("Filters: %s", filters)
            return get_files(entity_name), 200

        # TODO - Add `get.__doc__`

    FilesEndpoint.__name__ = entity_name
    return FilesEndpoint


def get_number_count_files_endpoint(endpoint_name, entity_name):
    """
    TODO - Add docstring
    """

    class CountFilesEndpoint(Resource):
        def get(self, pid):
            # Only WHERE included on count endpoints
            filters = get_filters_from_query_string("search_api", entity_name)
            log.debug("Filters: %s", filters)
            return get_files_count(entity_name, pid)

        # TODO - Add `get.__doc__`

    CountFilesEndpoint.__name__ = entity_name
    return CountFilesEndpoint
