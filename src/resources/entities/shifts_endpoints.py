from flask import request
from flask_restful import Resource

from common.database_helpers import delete_row_by_id, update_row_from_id, get_rows_by_filter, \
    get_filtered_row_count, get_first_filtered_row, EntityManager, patch_entities
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string
from common.models.db_models import SHIFT


class Shifts(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        return get_rows_by_filter(SHIFT, get_filters_from_query_string()), 200

    @requires_session_id
    @queries_records
    def post(self):
        EntityManager.create_row_from_json(SHIFT, request.json)
        return EntityManager.get_row_by_id(SHIFT, request.json["id"].to_dict()), 200

    @requires_session_id
    @queries_records
    def patch(self):
        return list(map(lambda x: x.to_dict(), patch_entities(SHIFT, request.json))), 200


class ShiftsWithID(Resource):
    @requires_session_id
    @queries_records
    def get(self, id):
        return EntityManager.get_row_by_id(SHIFT, id).to_dict(), 200

    @requires_session_id
    @queries_records
    def delete(self, id):
        delete_row_by_id(SHIFT, id)
        return "", 204

    @requires_session_id
    @queries_records
    def patch(self, id):
        update_row_from_id(SHIFT, id, str(request.json))
        return EntityManager.get_row_by_id(SHIFT, id).to_dict(), 200


class ShiftsCount(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_filtered_row_count(SHIFT, filters), 200


class ShiftsFindOne(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_first_filtered_row(SHIFT, filters), 200
