from flask_restful import Resource

from common.database_helpers import get_investigations_for_user, get_investigations_for_user_count, \
    get_facility_cycles_for_instrument, get_facility_cycles_for_instrument_count, \
    get_investigations_for_instrument_in_facility_cycle, get_investigations_for_instrument_in_facility_cycle_count
from common.helpers import get_session_id_from_auth_header, get_filters_from_query_string
from common.backends import backend


class UsersInvestigations(Resource):
    def get(self, id):
        return backend.get_investigations_for_user(get_session_id_from_auth_header(), id, get_filters_from_query_string()), 200


class UsersInvestigationsCount(Resource):
    def get(self, id):
        return backend.get_investigations_for_user_count(get_session_id_from_auth_header(), id, get_filters_from_query_string()), 200


class InstrumentsFacilityCycles(Resource):
    def get(self, id):
        return backend.get_facility_cycles_for_instrument(get_session_id_from_auth_header(), id, get_filters_from_query_string()), 200


class InstrumentsFacilityCyclesCount(Resource):
    def get(self, id):
        return backend.get_facility_cycles_for_instrument_count(get_session_id_from_auth_header(), id, get_filters_from_query_string()), 200


class InstrumentsFacilityCyclesInvestigations(Resource):
    def get(self, instrument_id, cycle_id):
        return backend.get_investigations_for_instrument_in_facility_cycle(get_session_id_from_auth_header(), instrument_id, cycle_id,
                                                                           get_filters_from_query_string()), 200


class InstrumentsFacilityCyclesInvestigationsCount(Resource):
    def get(self, instrument_id, cycle_id):
        return backend.get_investigations_for_instrument_in_facility_cycle_count(get_session_id_from_auth_header(), instrument_id, cycle_id,
                                                                                 get_filters_from_query_string()), 200
