from flask import request
from flask_restful import Resource

from common.database_helpers import EntityManager, patch_entities
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string
from common.models.db_models import INVESTIGATIONPARAMETER


class InvestigationParameters(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        return EntityManager.get_rows_by_filter(INVESTIGATIONPARAMETER, get_filters_from_query_string()), 200

    @requires_session_id
    @queries_records
    def post(self):
        EntityManager.create_row_from_json(INVESTIGATIONPARAMETER, request.json)
        return EntityManager.get_row_by_id(INVESTIGATIONPARAMETER, request.json["id"].to_dict()), 200

    @requires_session_id
    @queries_records
    def patch(self):
        return list(map(lambda x: x.to_dict(), patch_entities(INVESTIGATIONPARAMETER, request.json))), 200


class InvestigationParametersWithID(Resource):
    @requires_session_id
    @queries_records
    def get(self, id):
        return EntityManager.get_row_by_id(INVESTIGATIONPARAMETER, id).to_dict(), 200

    @requires_session_id
    @queries_records
    def delete(self, id):
        EntityManager.delete_row_by_id(INVESTIGATIONPARAMETER, id)
        return "", 204

    @requires_session_id
    @queries_records
    def patch(self, id):
        EntityManager.update_row_from_id(INVESTIGATIONPARAMETER, id, str(request.json))
        return EntityManager.get_row_by_id(INVESTIGATIONPARAMETER, id).to_dict(), 200


class InvestigationParametersCount(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return EntityManager.get_filtered_row_count(INVESTIGATIONPARAMETER, filters), 200


class InvestigationParametersFindOne(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return EntityManager.get_first_filtered_row(INVESTIGATIONPARAMETER, filters), 200
