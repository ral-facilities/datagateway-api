from flask import request
from flask_restful import Resource

from common.database_helpers import get_row_by_id, delete_row_by_id, update_row_from_id, get_rows_by_filter, \
    get_filtered_row_count, get_first_filtered_row, EntityManager, patch_entities
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string
from common.models.db_models import DATAFILEFORMAT


class DatafileFormats(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        return get_rows_by_filter(DATAFILEFORMAT, get_filters_from_query_string()), 200

    @requires_session_id
    @queries_records
    def post(self):
        EntityManager.create_row_from_json(DATAFILEFORMAT, request.json)
        return get_row_by_id(DATAFILEFORMAT, request.json["id"].to_dict()), 200

    @requires_session_id
    @queries_records
    def patch(self):
        return list(map(lambda x: x.to_dict(), patch_entities(DATAFILEFORMAT, request.json))), 200


class DatafileFormatsWithID(Resource):
    @requires_session_id
    @queries_records
    def get(self, id):
        return get_row_by_id(DATAFILEFORMAT, id).to_dict(), 200

    @requires_session_id
    @queries_records
    def delete(self, id):
        delete_row_by_id(DATAFILEFORMAT, id)
        return "", 204

    @requires_session_id
    @queries_records
    def patch(self, id):
        update_row_from_id(DATAFILEFORMAT, id, str(request.json))
        return get_row_by_id(DATAFILEFORMAT, id).to_dict(), 200


class DatafileFormatsCount(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_filtered_row_count(DATAFILEFORMAT, filters), 200


class DatafileFormatsFindOne(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_first_filtered_row(DATAFILEFORMAT, filters), 200
