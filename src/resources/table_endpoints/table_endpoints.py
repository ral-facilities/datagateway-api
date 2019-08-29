from flask_restful import Resource

from common.database_helpers import get_investigations_for_user, get_investigations_for_user_count, \
    get_facility_cycles_for_instrument, get_facility_cycles_for_instrument_count, \
    get_investigations_for_instrument_in_facility_cycle, get_investigations_for_instrument_in_facility_cycle_count
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
    @requires_session_id
    @queries_records
    def get(self, id):
        return list(
            map(lambda x: x.to_dict(), get_facility_cycles_for_instrument(id, get_filters_from_query_string()))), 200


class InstrumentsFacilityCyclesCount(Resource):
    @requires_session_id
    @queries_records
    def get(self, id):
        return get_facility_cycles_for_instrument_count(id), 200


class InstrumentsFacilityCyclesInvestigations(Resource):
    @requires_session_id
    @queries_records
    def get(self, instrument_id, cycle_id):
        return list(map(lambda x: x.to_dict(), get_investigations_for_instrument_in_facility_cycle(instrument_id, cycle_id))), 200


class InstrumentsFacilityCyclesInvestigationsCount(Resource):
    @requires_session_id
    @queries_records
    def get(self, instrument_id, cycle_id):
        return get_investigations_for_instrument_in_facility_cycle_count(instrument_id, cycle_id), 200

