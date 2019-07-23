from flask import request
from flask_restful import Resource

from common.database_helpers import EntityManager
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string
from common.models.db_models import STUDY


class Studies(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        return EntityManager.get_rows_by_filter(STUDY, get_filters_from_query_string()), 200

    @requires_session_id
    @queries_records
    def post(self):
        EntityManager.create_row_from_json(STUDY, request.json)
        return EntityManager.get_row_by_id(STUDY, request.json["id"].to_dict()), 200

    @requires_session_id
    @queries_records
    def patch(self):
        return list(map(lambda x: x.to_dict(), EntityManager.patch_entities(STUDY, request.json))), 200


class StudiesWithID(Resource):
    @requires_session_id
    @queries_records
    def get(self, id):
        return EntityManager.get_row_by_id(STUDY, id).to_dict(), 200

    @requires_session_id
    @queries_records
    def delete(self, id):
        EntityManager.delete_row_by_id(STUDY, id)
        return "", 204

    @requires_session_id
    @queries_records
    def patch(self, id):
        EntityManager.update_row_from_id(STUDY, id, str(request.json))
        return EntityManager.get_row_by_id(STUDY, id).to_dict(), 200


class StudiesCount(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return EntityManager.get_filtered_row_count(STUDY, filters), 200


class StudiesFindOne(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return EntityManager.get_first_filtered_row(STUDY, filters), 200
