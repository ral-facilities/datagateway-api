from flask import request
from flask_restful import Resource

from common.database_helpers import \
    get_filtered_row_count, get_first_filtered_row, EntityManager, patch_entities
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string
from common.models.db_models import INVESTIGATIONUSER


class InvestigationUsers(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        return EntityManager.get_rows_by_filter(INVESTIGATIONUSER, get_filters_from_query_string()), 200

    @requires_session_id
    @queries_records
    def post(self):
        EntityManager.create_row_from_json(INVESTIGATIONUSER, request.json)
        return EntityManager.get_row_by_id(INVESTIGATIONUSER, request.json["id"].to_dict()), 200

    @requires_session_id
    @queries_records
    def patch(self):
        return list(map(lambda x: x.to_dict(), patch_entities(INVESTIGATIONUSER, request.json))), 200


class InvestigationUsersWithID(Resource):
    @requires_session_id
    @queries_records
    def get(self, id):
        return EntityManager.get_row_by_id(INVESTIGATIONUSER, id).to_dict(), 200

    @requires_session_id
    @queries_records
    def delete(self, id):
        EntityManager.delete_row_by_id(INVESTIGATIONUSER, id)
        return "", 204

    @requires_session_id
    @queries_records
    def patch(self, id):
        EntityManager.update_row_from_id(INVESTIGATIONUSER, id, str(request.json))
        return EntityManager.get_row_by_id(INVESTIGATIONUSER, id).to_dict(), 200


class InvestigationUsersCount(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_filtered_row_count(INVESTIGATIONUSER, filters), 200


class InvestigationUsersFindOne(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_first_filtered_row(INVESTIGATIONUSER, filters), 200
