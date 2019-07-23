from flask import request
from flask_restful import Resource

from common.database_helpers import EntityManager
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string
from common.models.db_models import DATAFILE


class Datafiles(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        return EntityManager.get_rows_by_filter(DATAFILE, get_filters_from_query_string()), 200

    @requires_session_id
    @queries_records
    def post(self):
        EntityManager.create_row_from_json(DATAFILE, request.json)
        return "", 200

    @requires_session_id
    @queries_records
    def patch(self):
        return list(map(lambda x: x.to_dict(), EntityManager.patch_entities(DATAFILE, request.json))), 200


class DatafilesWithID(Resource):

    @requires_session_id
    @queries_records
    def get(self, id):
        return EntityManager.get_row_by_id(DATAFILE, id).to_dict(), 200

    @requires_session_id
    @queries_records
    def delete(self, id):
        EntityManager.delete_row_by_id(DATAFILE, id)
        return "", 204

    @requires_session_id
    @queries_records
    def patch(self, id):
        EntityManager.update_row_from_id(DATAFILE, id, request.json)
        return EntityManager.get_row_by_id(DATAFILE, id).to_dict(), 200


class DatafilesCount(Resource):

    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return EntityManager.get_filtered_row_count(DATAFILE, filters), 200


class DatafilesFindOne(Resource):

    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return EntityManager.get_first_filtered_row(DATAFILE, filters), 200
