from flask_restful import Resource

from common.database_helpers import get_investigations_for_user, get_investigations_for_user_count
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string


class UsersInvestigations(Resource):
    @requires_session_id
    @queries_records
    def get(self, id):
        return get_investigations_for_user(id, get_filters_from_query_string()), 200


class UsersInvestigationsCount(Resource):
    @requires_session_id
    @queries_records
    def get(self, id):
        return get_investigations_for_user_count(id, get_filters_from_query_string()), 200


class InstrumentsFacilityCycles(Resource):
    pass


class InstrumentsFacilityCyclesCount(Resource):
    pass


class InstrumentsFacilityCyclesInvestigations(Resource):
    pass


class InstrumentsFacilityCyclesInvestigationsCount(Resource):
    pass

