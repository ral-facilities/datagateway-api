import logging

from flask_restful import Resource

from datagateway_api.src.common.helpers import get_filters_from_query_string
from datagateway_api.src.search_api.filters import SearchAPIScoringFilter
from datagateway_api.src.search_api.helpers import (
    get_count,
    get_files,
    get_files_count,
    get_search,
    get_with_pid,
    search_api_error_handling,
)
from datagateway_api.src.search_api.search_scoring import SearchScoring

log = logging.getLogger()


def get_search_endpoint(entity_name):
    """
    Given an entity name, generate a flask_restful `Resource` class. In
    `create_api_endpoints()`, these generated classes are registered with the API e.g.
    `api.add_resource(get_search_endpoint("Dataset"), "/Datasets")`

    :param entity_name: Name of the entity
    :type entity_name: :class:`str`
    :return: Generated endpoint class
    """

    class Endpoint(Resource):
        @search_api_error_handling
        def get(self):
            filters = get_filters_from_query_string("search_api", entity_name)
            results = get_search(entity_name, filters)
            scoring_filter = next(
                (
                    filter_
                    for filter_ in filters
                    if isinstance(filter_, SearchAPIScoringFilter)
                ),
                None,
            )
            if scoring_filter:
                scores = SearchScoring.get_score(scoring_filter.value)
                results = SearchScoring.add_scores_to_results(results, scores)

            return results, 200

        get.__doc__ = f"""
            ---
            summary: Get {entity_name}s
            description: Retrieves a list of {entity_name} objects
            tags:
                - {entity_name}
            parameters:
                - FILTER
            responses:
                200:
                    description: Success - returns {entity_name}s that satisfy the
                        filter
                    content:
                        application/json:
                            schema:
                                type: array
                                items:
                                  $ref:
                                    '#/components/schemas/{entity_name}'
                400:
                    description: Bad request - Something was wrong with the request
                404:
                    description: No such record - Unable to find a record in ICAT
            """

    Endpoint.__name__ = entity_name
    return Endpoint


def get_single_endpoint(entity_name):
    """
    Given an entity name, generate a flask_restful `Resource` class. In
    `create_api_endpoints()`, these generated classes are registered with the API e.g.
    `api.add_resource(get_single_endpoint("Dataset"), "/Datasets/<string:pid>")`

    :param entity_name: Name of the entity
    :type entity_name: :class:`str`
    :return: Generated endpoint class
    """

    class EndpointWithID(Resource):
        @search_api_error_handling
        def get(self, pid):
            filters = get_filters_from_query_string("search_api", entity_name)
            log.debug("Filters: %s", filters)
            return get_with_pid(entity_name, pid, filters), 200

        get.__doc__ = f"""
            ---
            summary: Find the {entity_name} matching the given pid
            description: Retrieves a {entity_name} object with the matching pid
            tags:
                - {entity_name}
            parameters:
                - in: path
                  required: true
                  name: pid
                  description: The pid of the entity to retrieve
                  schema:
                    oneOf:
                      - type: string
                - FILTER
            responses:
                200:
                    description: Success - the matching {entity_name}
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/{entity_name}'
                400:
                    description: Bad request - Something was wrong with the request
                404:
                    description: No such record - Unable to find a record in ICAT
            """

    EndpointWithID.__name__ = entity_name
    return EndpointWithID


def get_number_count_endpoint(entity_name):
    """
    Given an entity name, generate a flask_restful `Resource` class. In
    `create_api_endpoints()`, these generated classes are registered with the API e.g.
    `api.add_resource(get_number_count_endpoint("Dataset"), "/Datasets/count")`

    :param entity_name: Name of the entity
    :type entity_name: :class:`str`
    :return: Generated endpoint class
    """

    class CountEndpoint(Resource):
        @search_api_error_handling
        def get(self):
            # Only WHERE included on count endpoints
            filters = get_filters_from_query_string("search_api", entity_name)
            log.debug("Filters: %s", filters)
            return get_count(entity_name, filters), 200

        get.__doc__ = f"""
            ---
            summary: Count {entity_name}s
            description: Return the count of the {entity_name} objects that would be
                retrieved given the filters provided
            tags:
                - {entity_name}
            parameters:
                - WHERE_FILTER
            responses:
                200:
                    description: Success - The count of the {entity_name} objects
                    content:
                        application/json:
                            schema:
                                type: integer
                400:
                    description: Bad request - Something was wrong with the request
                404:
                    description: No such record - Unable to find a record in ICAT
            """

    CountEndpoint.__name__ = entity_name
    return CountEndpoint


def get_files_endpoint(entity_name):
    """
    Given an entity name, generate a flask_restful `Resource` class. In
    `create_api_endpoints()`, these generated classes are registered with the API e.g.
    `api.add_resource(get_files_endpoint("Dataset"), "/Datasets/<string:pid>/files")`

    :param entity_name: Name of the entity
    :type entity_name: :class:`str`
    :return: Generated endpoint class
    """

    class FilesEndpoint(Resource):
        @search_api_error_handling
        def get(self, pid):
            filters = get_filters_from_query_string("search_api", entity_name)
            log.debug("Filters: %s", filters)
            return get_files(entity_name, pid, filters), 200

        get.__doc__ = f"""
            ---
            summary: Get {entity_name}s for the given Dataset
            description: Retrieves a list of {entity_name} objects for a given Dataset
                object
            tags:
                - Dataset
            parameters:
                - in: path
                  required: true
                  name: pid
                  description: The pid of the entity to retrieve
                  schema:
                    oneOf:
                      - type: string
                - FILTER
            responses:
                200:
                    description: Success - returns {entity_name}s for the given Dataset
                        object that satisfy the filter
                    content:
                        application/json:
                            schema:
                                type: array
                                items:
                                  $ref:
                                    '#/components/schemas/{entity_name}'
                400:
                    description: Bad request - Something was wrong with the request
                404:
                    description: No such record - Unable to find a record in ICAT
            """

    FilesEndpoint.__name__ = entity_name
    return FilesEndpoint


def get_number_count_files_endpoint(entity_name):
    """
    Given an entity name, generate a flask_restful `Resource` class. In
    `create_api_endpoints()`, these generated classes are registered with the API e.g.
    `api.add_resource(get_number_count_files_endpoint("Dataset"),
    "/Datasets<string:pid>/files/count")`

    :param entity_name: Name of the entity
    :type entity_name: :class:`str`
    :return: Generated endpoint class
    """

    class CountFilesEndpoint(Resource):
        @search_api_error_handling
        def get(self, pid):
            # Only WHERE included on count endpoints
            filters = get_filters_from_query_string("search_api", entity_name)
            log.debug("Filters: %s", filters)
            return get_files_count(entity_name, filters, pid)

        get.__doc__ = f"""
            ---
            summary: Count {entity_name}s for the given Dataset
            description: Return the count of {entity_name} objects for the given Dataset
                object that would be retrieved given the filters provided
            tags:
                - Dataset
            parameters:
                - in: path
                  required: true
                  name: pid
                  description: The pid of the entity to retrieve
                  schema:
                    oneOf:
                      - type: string
                - WHERE_FILTER
            responses:
                200:
                    description: Success - The count of {entity_name} objects for the
                        given Dataset object
                    content:
                        application/json:
                            schema:
                                type: integer
                400:
                    description: Bad request - Something was wrong with the request
                404:
                    description: No such record - Unable to find a record in ICAT
            """

    CountFilesEndpoint.__name__ = entity_name
    return CountFilesEndpoint
