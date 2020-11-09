from flask import request
from flask_restful import Resource

from datagateway_api.common.backends import create_backend
from datagateway_api.common.config import config
from datagateway_api.common.helpers import (
    get_filters_from_query_string,
    get_session_id_from_auth_header,
)

backend = create_backend(config.get_backend_type())


def get_endpoint(name, entity_type):
    """
    Given an entity name generate a flask_restful Resource class.
    In main.py these generated classes are registered with the api e.g
    api.add_resource(get_endpoint("Datafiles", DATAFILE), "/datafiles")

    :param name: The name of the entity
    :param entity_type: The entity the endpoint will use in queries
    :return: The generated endpoint class
    """

    entity_schema_name = entity_type.strip("_").upper()

    class Endpoint(Resource):
        def get(self):
            return (
                backend.get_with_filters(
                    get_session_id_from_auth_header(),
                    entity_type,
                    get_filters_from_query_string(),
                ),
                200,
            )

        get.__doc__ = f"""
            ---
            summary: Get {name}
            description: Retrieves a list of {entity_type} objects
            tags:
                - {name}
            parameters:
                - WHERE_FILTER
                - ORDER_FILTER
                - LIMIT_FILTER
                - SKIP_FILTER
                - DISTINCT_FILTER
                - INCLUDE_FILTER
            responses:
                200:
                    description: Success - returns {entity_type} that satisfy the
                        filters
                    content:
                        application/json:
                            schema:
                                type: array
                                items:
                                  $ref:
                                    '#/components/schemas/{entity_schema_name}'
                400:
                    description: Bad request - Something was wrong with the request
                401:
                    description: Unauthorized - No session ID found in HTTP Auth. header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in ICAT
            """

        def post(self):
            return (
                backend.create(
                    get_session_id_from_auth_header(), entity_type, request.json,
                ),
                200,
            )

        post.__doc__ = f"""
            ---
            summary: Create new {name}
            description: Creates new {entity_type} object(s) with details provided in
                the request body
            tags:
                - {name}
            requestBody:
              description: The values to use to create the new object(s) with
              required: true
              content:
                application/json:
                  schema:
                    type: array
                    items:
                      $ref: '#/components/schemas/{entity_schema_name}'
            responses:
                200:
                    description: Success - returns the created object
                    content:
                      application/json:
                        schema:
                          type: array
                          items:
                            $ref: '#/components/schemas/{entity_schema_name}'
                400:
                    description: Bad request - Something was wrong with the request
                401:
                    description: Unauthorized - No session ID found in HTTP Auth. header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in ICAT
            """

        def patch(self):
            return (
                backend.update(
                    get_session_id_from_auth_header(), entity_type, request.json,
                ),
                200,
            )

        patch.__doc__ = f"""
            ---
            summary: Update {name}
            description: Updates {entity_type} object(s) with details provided in the
                request body
            tags:
                - {name}
            requestBody:
              description: The values to use to update the object(s) with
              required: true
              content:
                application/json:
                  schema:
                    type: array
                    items:
                      $ref: '#/components/schemas/{entity_schema_name}'
            responses:
                200:
                    description: Success - returns the updated object(s)
                    content:
                      application/json:
                        schema:
                          type: array
                          items:
                            $ref: '#/components/schemas/{entity_schema_name}'
                400:
                    description: Bad request - Something was wrong with the request
                401:
                    description: Unauthorized - No session ID found in HTTP Auth. header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in ICAT
            """

    Endpoint.__name__ = name
    return Endpoint


def get_id_endpoint(name, entity_type):
    """
    Given an entity name generate a flask_restful Resource class.
    In main.py these generated classes are registered with the api e.g
    api.add_resource(get_endpoint("Datafiles", DATAFILE), "/datafiles/<int:id_>")

    :param name: The name of the entity
    :param entity_type: The entity the endpoint will use in queries
    :return: The generated id endpoint class
    """

    entity_schema_name = entity_type.strip("_").upper()

    class EndpointWithID(Resource):
        def get(self, id_):
            return (
                backend.get_with_id(
                    get_session_id_from_auth_header(), entity_type, id_,
                ),
                200,
            )

        get.__doc__ = f"""
            ---
            summary: Find the {entity_type} matching the given ID
            description: Retrieves a list of {entity_type} objects
            tags:
                - {name}
            parameters:
                - in: path
                  required: true
                  name: id
                  description: The id of the entity to retrieve
                  schema:
                    type: integer
            responses:
                200:
                    description: Success - the matching {entity_type}
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/{entity_schema_name}'
                400:
                    description: Bad request - Something was wrong with the request
                401:
                    description: Unauthorized - No session ID found in HTTP Auth. header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in ICAT
            """

        def delete(self, id_):
            backend.delete_with_id(get_session_id_from_auth_header(), entity_type, id_)
            return "", 204

        delete.__doc__ = f"""
            ---
            summary: Delete {name} by id
            description: Updates {entity_type} with the specified ID with details
                provided in the request body
            tags:
                - {name}
            parameters:
                - in: path
                  required: true
                  name: id
                  description: The id of the entity to delete
                  schema:
                    type: integer
            responses:
                204:
                    description: No Content - Object was successfully deleted
                400:
                    description: Bad request - Something was wrong with the request
                401:
                    description: Unauthorized - No session ID found in HTTP Auth. header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in ICAT
            """

        def patch(self, id_):
            session_id = get_session_id_from_auth_header()
            backend.update_with_id(session_id, entity_type, id_, request.json)
            return backend.get_with_id(session_id, entity_type, id_), 200

        patch.__doc__ = f"""
            ---
            summary: Update {name} by id
            description: Updates {entity_type} with the specified ID with details
                provided in the request body
            tags:
                - {name}
            parameters:
                - in: path
                  required: true
                  name: id
                  description: The id of the entity to update
                  schema:
                    type: integer
            requestBody:
              description: The values to use to update the object(s) with
              required: true
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/{entity_schema_name}'
            responses:
                200:
                    description: Success - returns the updated object
                    content:
                      application/json:
                        schema:
                          $ref: '#/components/schemas/{entity_schema_name}'
                400:
                    description: Bad request - Something was wrong with the request
                401:
                    description: Unauthorized - No session ID found in HTTP Auth. header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in ICAT
            """

    EndpointWithID.__name__ = f"{name}WithID"
    return EndpointWithID


def get_count_endpoint(name, entity_type):
    """
    Given an entity name generate a flask_restful Resource class.
    In main.py these generated classes are registered with the api e.g
    api.add_resource(get_endpoint("Datafiles", DATAFILE), "/datafiles/count")

    :param name: The name of the entity
    :param entity_type: The entity the endpoint will use in queries
    :return: The generated count endpoint class
    """

    class CountEndpoint(Resource):
        def get(self):
            filters = get_filters_from_query_string()
            return (
                backend.count_with_filters(
                    get_session_id_from_auth_header(), entity_type, filters,
                ),
                200,
            )

        get.__doc__ = f"""
            ---
            summary: Count {name}
            description: Return the count of the {entity_type} objects that would be
                retrieved given the filters provided
            tags:
                - {name}
            parameters:
                - WHERE_FILTER
                - DISTINCT_FILTER
                - INCLUDE_FILTER
            responses:
                200:
                    description: Success - The count of the {entity_type} objects
                    content:
                        application/json:
                            schema:
                                type: integer
                400:
                    description: Bad request - Something was wrong with the request
                401:
                    description: Unauthorized - No session ID found in HTTP Auth. header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in ICAT
            """

    CountEndpoint.__name__ = f"{name}Count"
    return CountEndpoint


def get_find_one_endpoint(name, entity_type):
    """
    Given an entity name generate a flask_restful Resource class.
    In main.py these generated classes are registered with the api e.g
    api.add_resource(get_endpoint("Datafiles", DATAFILE), "/datafiles/findone")

    :param name: The name of the entity
    :param entity_type: The entity the endpoint will use in queries
    :return: The generated findOne endpoint class
    """

    entity_schema_name = entity_type.strip("_").upper()

    class FindOneEndpoint(Resource):
        def get(self):
            filters = get_filters_from_query_string()
            return (
                backend.get_one_with_filters(
                    get_session_id_from_auth_header(), entity_type, filters,
                ),
                200,
            )

        get.__doc__ = f"""
            ---
            summary: Get single {entity_type}
            description: Retrieves the first {entity_type} objects that satisfies the
                filters.
            tags:
                - {name}
            parameters:
                - WHERE_FILTER
                - ORDER_FILTER
                - LIMIT_FILTER
                - SKIP_FILTER
                - DISTINCT_FILTER
                - INCLUDE_FILTER
            responses:
                200:
                    description: Success - a {entity_type} object that satisfies the
                        filters
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/{entity_schema_name}'
                400:
                    description: Bad request - Something was wrong with the request
                401:
                    description: Unauthorized - No session ID found in HTTP Auth. header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in ICAT
            """

    FindOneEndpoint.__name__ = f"{name}FindOne"
    return FindOneEndpoint
