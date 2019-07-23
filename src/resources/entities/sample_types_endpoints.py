from flask import request
from flask_restful import Resource

from common.database_helpers import EntityManager
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string
from common.models.db_models import SAMPLETYPE


class SampleTypes(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        return EntityManager.get_rows_by_filter(SAMPLETYPE, get_filters_from_query_string()), 200

    @requires_session_id
    @queries_records
    def post(self):
        EntityManager.create_row_from_json(SAMPLETYPE, request.json)
        return EntityManager.get_row_by_id(SAMPLETYPE, request.json["id"].to_dict()), 200

    @requires_session_id
    @queries_records
    def patch(self):
        return list(map(lambda x: x.to_dict(), EntityManager.patch_entities(SAMPLETYPE, request.json))), 200


class SampleTypesWithID(Resource):
    @requires_session_id
    @queries_records
    def get(self, id):
        return EntityManager.get_row_by_id(SAMPLETYPE, id).to_dict(), 200

    @requires_session_id
    @queries_records
    def delete(self, id):
        EntityManager.delete_row_by_id(SAMPLETYPE, id)
        return "", 204

    @requires_session_id
    @queries_records
    def patch(self, id):
        EntityManager.update_row_from_id(SAMPLETYPE, id, str(request.json))
        return EntityManager.get_row_by_id(SAMPLETYPE, id).to_dict(), 200


class SampleTypesCount(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return EntityManager.get_filtered_row_count(SAMPLETYPE, filters), 200


class SampleTypesFindOne(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return EntityManager.get_first_filtered_row(SAMPLETYPE, filters), 200
