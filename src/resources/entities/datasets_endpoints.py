from flask import request
from flask_restful import Resource

from common.database_helpers import EntityManager
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string
from common.models.db_models import DATASET


class Datasets(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        return EntityManager.get_rows_by_filter(DATASET, get_filters_from_query_string()), 200

    @requires_session_id
    @queries_records
    def post(self):
        EntityManager.create_row_from_json(DATASET, request.json)
        return EntityManager.get_row_by_id(DATASET, request.json["id"].to_dict()), 200

    @requires_session_id
    @queries_records
    def patch(self):
        return list(map(lambda x: x.to_dict(), EntityManager.patch_entities(DATASET, request.json))), 200


class DatasetsWithID(Resource):
    @requires_session_id
    @queries_records
    def get(self, id):
        return EntityManager.get_row_by_id(DATASET, id).to_dict(), 200

    @requires_session_id
    @queries_records
    def delete(self, id):
        EntityManager.delete_row_by_id(DATASET, id)
        return "", 204

    @requires_session_id
    @queries_records
    def patch(self, id):
        EntityManager.update_row_from_id(DATASET, id, str(request.json))
        return EntityManager.get_row_by_id(DATASET, id).to_dict(), 200


class DatasetsCount(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return EntityManager.get_filtered_row_count(DATASET, filters), 200


class DatasetsFindOne(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return EntityManager.get_first_filtered_row(DATASET, filters), 200
