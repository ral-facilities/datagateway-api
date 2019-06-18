from flask import request
from flask_restful import Resource

from common.database_helpers import get_row_by_id, delete_row_by_id, update_row_from_id, get_rows_by_filter, \
    get_filtered_row_count, get_first_filtered_row, create_row_from_json
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string
from common.models.db_models import DATACOLLECTION


class DataCollections(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        return get_rows_by_filter(DATACOLLECTION, get_filters_from_query_string()), 200

    @requires_session_id
    @queries_records
    def post(self):
        create_row_from_json(DATACOLLECTION, request.json)
        return get_row_by_id(DATACOLLECTION, request.json["id"].to_dict()), 200

    @requires_session_id
    @queries_records
    def patch(self):
        pass


class DataCollectionsWithID(Resource):
    @requires_session_id
    @queries_records
    def get(self, id):
        return get_row_by_id(DATACOLLECTION, id).to_dict(), 200

    @requires_session_id
    @queries_records
    def delete(self, id):
        delete_row_by_id(DATACOLLECTION, id)
        return "", 204

    @requires_session_id
    @queries_records
    def patch(self, id):
        update_row_from_id(DATACOLLECTION, id, str(request.json))
        return get_row_by_id(DATACOLLECTION, id).to_dict(), 200


class DataCollectionsCount(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_filtered_row_count(DATACOLLECTION, filters), 200


class DataCollectionsFindOne(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_first_filtered_row(DATACOLLECTION, filters), 200
