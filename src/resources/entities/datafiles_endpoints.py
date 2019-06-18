from flask import request
from flask_restful import Resource

from common.database_helpers import get_row_by_id, delete_row_by_id, update_row_from_id, get_rows_by_filter, \
    get_filtered_row_count, get_first_filtered_row, create_row_from_json
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string
from common.models.db_models import DATAFILE


class Datafiles(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        return get_rows_by_filter(DATAFILE, get_filters_from_query_string()), 200

    @requires_session_id
    @queries_records
    def post(self):
        create_row_from_json(DATAFILE, request.json)
        return "", 200

    @requires_session_id
    @queries_records
    def patch(self):
        pass


class DatafilesWithID(Resource):

    @requires_session_id
    @queries_records
    def get(self, id):
        return get_row_by_id(DATAFILE, id).to_dict(), 200

    @requires_session_id
    @queries_records
    def delete(self, id):
        delete_row_by_id(DATAFILE, id)
        return "", 204

    @requires_session_id
    @queries_records
    def patch(self, id):
        update_row_from_id(DATAFILE, id, request.json)
        return get_row_by_id(DATAFILE, id).to_dict(), 200


class DatafilesCount(Resource):

    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_filtered_row_count(DATAFILE, filters), 200


class DatafilesFindOne(Resource):

    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_first_filtered_row(DATAFILE, filters), 200
