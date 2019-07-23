from flask import request
from flask_restful import Resource

from common.database_helpers import delete_row_by_id, update_row_from_id, get_rows_by_filter, \
    get_filtered_row_count, get_first_filtered_row, EntityManager, patch_entities
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string
from common.models.db_models import PUBLICSTEP


class PublicSteps(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        return get_rows_by_filter(PUBLICSTEP, get_filters_from_query_string()), 200

    @requires_session_id
    @queries_records
    def post(self):
        EntityManager.create_row_from_json(PUBLICSTEP, request.json)
        return EntityManager.get_row_by_id(PUBLICSTEP, request.json["id"].to_dict()), 200

    @requires_session_id
    @queries_records
    def patch(self):
        return list(map(lambda x: x.to_dict(), patch_entities(PUBLICSTEP, request.json))), 200


class PublicStepsWithID(Resource):
    @requires_session_id
    @queries_records
    def get(self, id):
        return EntityManager.get_row_by_id(PUBLICSTEP, id).to_dict(), 200

    @requires_session_id
    @queries_records
    def delete(self, id):
        delete_row_by_id(PUBLICSTEP, id)
        return "", 204

    @requires_session_id
    @queries_records
    def patch(self, id):
        update_row_from_id(PUBLICSTEP, id, str(request.json))
        return EntityManager.get_row_by_id(PUBLICSTEP, id).to_dict(), 200


class PublicStepsCount(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_filtered_row_count(PUBLICSTEP, filters), 200


class PublicStepsFindOne(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_first_filtered_row(PUBLICSTEP, filters), 200
