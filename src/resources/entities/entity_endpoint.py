from flask import request
from flask_restful import Resource

from common.database_helpers import get_rows_by_filter, create_rows_from_json, patch_entities, get_row_by_id, \
    delete_row_by_id, update_row_from_id, get_filtered_row_count, get_first_filtered_row
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string


def get_endpoint(name, table):
    class Endpoint(Resource):
        @requires_session_id
        @queries_records
        def get(self):
            return get_rows_by_filter(table, get_filters_from_query_string()), 200

        @requires_session_id
        @queries_records
        def post(self):
            return create_rows_from_json(table, request.json), 200

        @requires_session_id
        @queries_records
        def patch(self):
            return list(map(lambda x: x.to_dict(), patch_entities(table, request.json))), 200

    Endpoint.__name__ = name
    return Endpoint


def get_id_endpoint(name, table):
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
    class CountEndpoint(Resource):

        @requires_session_id
        @queries_records
        def get(self):
            filters = get_filters_from_query_string()
            return get_filtered_row_count(table, filters), 200

    CountEndpoint.__name__ = f"{name}Count"
    return CountEndpoint


def get_find_one_endpoint(name, table):
    class FindOneEndpoint(Resource):

        @requires_session_id
        @queries_records
        def get(self):
            filters = get_filters_from_query_string()
            return get_first_filtered_row(table, filters), 200

    FindOneEndpoint.__name__ = f"{name}FindOne"
    return FindOneEndpoint
