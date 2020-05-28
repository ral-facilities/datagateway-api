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

        def post(self):
            return backend.create(get_session_id_from_auth_header(), table, request.json), 200

        def patch(self):
            return list(map(lambda x: x.to_dict(), backend.update(get_session_id_from_auth_header(), table, request.json))), 200

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
            return backend.get_with_id(get_session_id_from_auth_header(), table, id).to_dict(), 200

        def delete(self, id):
            backend.delete_with_id(
                get_session_id_from_auth_header(), table, id)
            return "", 204

        def patch(self, id):
            session_id = get_session_id_from_auth_header()
            backend.update_with_id(session_id, table, id, request.json)
            return backend.get_with_id(session_id, table, id).to_dict(), 200

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

    FindOneEndpoint.__name__ = f"{name}FindOne"
    return FindOneEndpoint
