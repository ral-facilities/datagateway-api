from flask import request
from flask_restful import Resource

from common.database_helpers import get_rows_by_filter, create_rows_from_json, patch_entities, get_row_by_id, \
    delete_row_by_id, update_row_from_id, get_filtered_row_count, get_first_filtered_row
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string


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
        @requires_session_id
        @queries_records
        def get(self):
            return get_rows_by_filter(table, get_filters_from_query_string()), 200

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
                    description: Success - a user's session details
                    content:
                        application/json:
                            schema:
                                type: array
                                items:
                                  $ref: '#/components/schemas/{table.__name__.strip("_")}'
                400:
                    description: Bad request - something was wrong with the request
                401:
                    description: Unauthorized - No session ID was found in the HTTP Authorization header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in the database
            """

        @requires_session_id
        @queries_records
        def post(self):
            return create_rows_from_json(table, request.json), 200

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
                    description: Bad request - something was wrong with the request
                401:
                    description: Unauthorized - No session ID was found in the HTTP Authorization header
                403:
                    description: Forbidden - The session ID provided is invalid
                404:
                    description: No such record - Unable to find a record in the database
            """

        @requires_session_id
        @queries_records
        def patch(self):
            return list(map(lambda x: x.to_dict(), patch_entities(table, request.json))), 200

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
                    description: Success - returns the updated objects
                    content:
                      application/json:
                        schema:
                          oneOf:
                            - $ref: '#/components/schemas/{table.__name__.strip("_")}'
                            - type: array
                              items:
                                $ref: '#/components/schemas/{table.__name__.strip("_")}'
                400:
                    description: Bad request - something was wrong with the request
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

        @requires_session_id
        @queries_records
        def get(self, id):
            return get_row_by_id(table, id).to_dict(), 200

        @requires_session_id
        @queries_records
        def delete(self, id):
            delete_row_by_id(table, id)
            return "", 204

        @requires_session_id
        @queries_records
        def patch(self, id):
            update_row_from_id(table, id, request.json)
            return get_row_by_id(table, id).to_dict(), 200

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

        @requires_session_id
        @queries_records
        def get(self):
            filters = get_filters_from_query_string()
            return get_filtered_row_count(table, filters), 200

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

        @requires_session_id
        @queries_records
        def get(self):
            filters = get_filters_from_query_string()
            return get_first_filtered_row(table, filters), 200

    FindOneEndpoint.__name__ = f"{name}FindOne"
    return FindOneEndpoint
