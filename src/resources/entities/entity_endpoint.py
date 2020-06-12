from flask import request
from flask_restful import Resource

from common.database_helpers import get_rows_by_filter, create_rows_from_json, patch_entities, get_row_by_id, \
    delete_row_by_id, update_row_from_id, get_filtered_row_count, get_first_filtered_row
from common.helpers import get_session_id_from_auth_header, get_filters_from_query_string
from common.backends import backend


def get_endpoint(name, table):
    """
    Given an entity name generate a flask_restful Resource class.
    In main.py these generated classes are registered with the api e.g
    api.add_resource(get_endpoint("Datafiles", DATAFILE), "/datafiles")
    :param name: The name of the entity
    :param table: The table the endpoint will use in queries
    :return: The generated endpoint class
    """
    class Endpoint(Resource):
        def get(self):
            return backend.get_with_filters(get_session_id_from_auth_header(), table, get_filters_from_query_string()), 200

        get.__doc__ = f"""
            ---
            summary: Get {name}
            description: Retrieves a list of {table.__name__} objects
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
                    description: Success - returns {table.__name__} that satisfy the filters
                    content:
                        application/json:
                            schema:
                                type: array
                                items:
                                  $ref: '#/components/schemas/{table.__name__.strip("_")}'
                400:
                    description: Bad request - Something was wrong with the request
                401:
                    description: Unauthorized - No session ID was found in the HTTP Authorization header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in the database
            """

        def post(self):
            return backend.create(get_session_id_from_auth_header(), table, request.json), 200

        post.__doc__ = f"""
            ---
            summary: Create new {name}
            description: Creates new {table.__name__} object(s) with details provided in the request body
            tags:
                - {name}
            requestBody:
              description: The values to use to create the new object(s) with
              required: true
              content:
                application/json:
                  schema:
                    oneOf:
                      - $ref: '#/components/schemas/{table.__name__.strip("_")}'
                      - type: array
                        items:
                          $ref: '#/components/schemas/{table.__name__.strip("_")}'
            responses:
                200:
                    description: Success - returns the created object
                    content:
                      application/json:
                        schema:
                          oneOf:
                            - $ref: '#/components/schemas/{table.__name__.strip("_")}'
                            - type: array
                              items:
                                $ref: '#/components/schemas/{table.__name__.strip("_")}'
                400:
                    description: Bad request - Something was wrong with the request
                401:
                    description: Unauthorized - No session ID was found in the HTTP Authorization header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in the database
            """

        def patch(self):
            return list(map(lambda x: x.to_dict(), backend.update(get_session_id_from_auth_header(), table, request.json))), 200

        patch.__doc__ = f"""
            ---
            summary: Update {name}
            description: Updates {table.__name__} object(s) with details provided in the request body
            tags:
                - {name}
            requestBody:
              description: The values to use to update the object(s) with
              required: true
              content:
                application/json:
                  schema:
                    oneOf:
                      - $ref: '#/components/schemas/{table.__name__.strip("_")}'
                      - type: array
                        items:
                          $ref: '#/components/schemas/{table.__name__.strip("_")}'
            responses:
                200:
                    description: Success - returns the updated object(s)
                    content:
                      application/json:
                        schema:
                          oneOf:
                            - $ref: '#/components/schemas/{table.__name__.strip("_")}'
                            - type: array
                              items:
                                $ref: '#/components/schemas/{table.__name__.strip("_")}'
                400:
                    description: Bad request - Something was wrong with the request
                401:
                    description: Unauthorized - No session ID was found in the HTTP Authorization header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in the database
            """

    Endpoint.__name__ = name
    return Endpoint


def get_id_endpoint(name, table):
    """
    Given an entity name generate a flask_restful Resource class.
    In main.py these generated classes are registered with the api e.g
    api.add_resource(get_endpoint("Datafiles", DATAFILE), "/datafiles/<int:id>")
    :param name: The name of the entity
    :param table: The table the endpoint will use in queries
    :return: The generated id endpoint class
    """
    class EndpointWithID(Resource):

        def get(self, id):
            return backend.get_with_id(get_session_id_from_auth_header(), table, id), 200

        get.__doc__ = f"""
            ---
            summary: Find the {table.__name__} matching the given ID
            description: Retrieves a list of {table.__name__} objects
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
                    description: Success - the matching {table.__name__}
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/{table.__name__.strip("_")}'
                400:
                    description: Bad request - Something was wrong with the request
                401:
                    description: Unauthorized - No session ID was found in the HTTP Authorization header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in the database
            """

        def delete(self, id):
            backend.delete_with_id(
                get_session_id_from_auth_header(), table, id)
            return "", 204

        delete.__doc__ = f"""
            ---
            summary: Delete {name} by id
            description: Updates {table.__name__} with the specified ID with details provided in the request body
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
                    description: Unauthorized - No session ID was found in the HTTP Authorization header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in the database
            """

        def patch(self, id):
            session_id = get_session_id_from_auth_header()
            backend.update_with_id(session_id, table, id, request.json)
            return backend.get_with_id(session_id, table, id).to_dict(), 200

        patch.__doc__ = f"""
            ---
            summary: Update {name} by id
            description: Updates {table.__name__} with the specified ID with details provided in the request body
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
                    $ref: '#/components/schemas/{table.__name__.strip("_")}'
            responses:
                200:
                    description: Success - returns the updated object
                    content:
                      application/json:
                        schema:
                          $ref: '#/components/schemas/{table.__name__.strip("_")}'
                400:
                    description: Bad request - Something was wrong with the request
                401:
                    description: Unauthorized - No session ID was found in the HTTP Authorization header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in the database
            """

    EndpointWithID.__name__ = f"{name}WithID"
    return EndpointWithID


def get_count_endpoint(name, table):
    """
    Given an entity name generate a flask_restful Resource class.
    In main.py these generated classes are registered with the api e.g
    api.add_resource(get_endpoint("Datafiles", DATAFILE), "/datafiles/count")
    :param name: The name of the entity
    :param table: The table the endpoint will use in queries
    :return: The generated count endpoint class
    """
    class CountEndpoint(Resource):

        def get(self):
            filters = get_filters_from_query_string()
            return backend.count_with_filters(get_session_id_from_auth_header(), table, filters), 200

        get.__doc__ = f"""
            ---
            summary: Count {name}
            description: Return the count of the {table.__name__} objects that would be retrieved given the filters provided
            tags:
                - {name}
            parameters:
                - WHERE_FILTER
                - DISTINCT_FILTER
                - INCLUDE_FILTER
            responses:
                200:
                    description: Success - The count of the {table.__name__} objects
                    content:
                        application/json:
                            schema:
                                type: integer
                400:
                    description: Bad request - Something was wrong with the request
                401:
                    description: Unauthorized - No session ID was found in the HTTP Authorization header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in the database
            """

    CountEndpoint.__name__ = f"{name}Count"
    return CountEndpoint


def get_find_one_endpoint(name, table):
    """
    Given an entity name generate a flask_restful Resource class.
    In main.py these generated classes are registered with the api e.g
    api.add_resource(get_endpoint("Datafiles", DATAFILE), "/datafiles/findone")
    :param name: The name of the entity
    :param table: The table the endpoint will use in queries
    :return: The generated findOne endpoint class
    """
    class FindOneEndpoint(Resource):

        def get(self):
            filters = get_filters_from_query_string()
            return backend.get_one_with_filters(get_session_id_from_auth_header(), table, filters), 200

        get.__doc__ = f"""
            ---
            summary: Get single {table.__name__}
            description: Retrieves the first {table.__name__} objects that satisfies the filters.
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
                    description: Success - a {table.__name__} object that satisfies the filters
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/{table.__name__.strip("_")}'
                400:
                    description: Bad request - Something was wrong with the request
                401:
                    description: Unauthorized - No session ID was found in the HTTP Authorization header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in the database
            """

    FindOneEndpoint.__name__ = f"{name}FindOne"
    return FindOneEndpoint
