from flask import request
from flask_restful import Resource

from common.database_helpers import get_rows_by_filter, \
    get_filtered_row_count, get_first_filtered_row, EntityManager, patch_entities
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string
from common.models.db_models import INSTRUMENTSCIENTIST


class InstrumentScientists(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        return get_rows_by_filter(INSTRUMENTSCIENTIST, get_filters_from_query_string()), 200

    @requires_session_id
    @queries_records
    def post(self):
        EntityManager.create_row_from_json(INSTRUMENTSCIENTIST, request.json)
        return EntityManager.get_row_by_id(INSTRUMENTSCIENTIST, request.json["id"].to_dict()), 200

    @requires_session_id
    @queries_records
    def patch(self):
        return list(map(lambda x: x.to_dict(), patch_entities(INSTRUMENTSCIENTIST, request.json))), 200

class InstrumentScientistsWithID(Resource):
    @requires_session_id
    @queries_records
    def get(self, id):
        return EntityManager.get_row_by_id(INSTRUMENTSCIENTIST, id).to_dict(), 200

    @requires_session_id
    @queries_records
    def delete(self, id):
        EntityManager.delete_row_by_id(INSTRUMENTSCIENTIST, id)
        return "", 204

    @requires_session_id
    @queries_records
    def patch(self, id):
        EntityManager.update_row_from_id(INSTRUMENTSCIENTIST, id, str(request.json))
        return EntityManager.get_row_by_id(INSTRUMENTSCIENTIST, id).to_dict(), 200


class InstrumentScientistsCount(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_filtered_row_count(INSTRUMENTSCIENTIST, filters), 200


class InstrumentScientistsFindOne(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_first_filtered_row(INSTRUMENTSCIENTIST, filters), 200
