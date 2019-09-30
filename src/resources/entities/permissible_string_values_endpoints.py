from flask import request
from flask_restful import Resource

from common.database_helpers import get_row_by_id, delete_row_by_id, update_row_from_id, get_rows_by_filter, \
    get_filtered_row_count, get_first_filtered_row, patch_entities, create_rows_from_json
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string
from common.models.db_models import PERMISSIBLESTRINGVALUE
from src.swagger.swagger_generator import swagger_gen


@swagger_gen.resource_wrapper()
class PermissibleStringValues(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        return get_rows_by_filter(PERMISSIBLESTRINGVALUE, get_filters_from_query_string()), 200

    @requires_session_id
    @queries_records
    def post(self):
        return create_rows_from_json(request.json, PERMISSIBLESTRINGVALUE), 200

    @requires_session_id
    @queries_records
    def patch(self):
        return list(map(lambda x: x.to_dict(), patch_entities(PERMISSIBLESTRINGVALUE, request.json))), 200


class PermissibleStringValuesWithID(Resource):
    @requires_session_id
    @queries_records
    def get(self, id):
        return get_row_by_id(PERMISSIBLESTRINGVALUE, id).to_dict(), 200

    @requires_session_id
    @queries_records
    def delete(self, id):
        delete_row_by_id(PERMISSIBLESTRINGVALUE, id)
        return "", 204

    @requires_session_id
    @queries_records
    def patch(self, id):
        update_row_from_id(PERMISSIBLESTRINGVALUE, id, str(request.json))
        return get_row_by_id(PERMISSIBLESTRINGVALUE, id).to_dict(), 200


class PermissibleStringValuesCount(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_filtered_row_count(PERMISSIBLESTRINGVALUE, filters), 200


class PermissibleStringValuesFindOne(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_first_filtered_row(PERMISSIBLESTRINGVALUE, filters), 200
