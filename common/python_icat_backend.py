from common.backend import Backend
from common.helpers import requires_session_id, queries_records
#from common.python_icat_helpers import


class PythonICATBackend(Backend):
    """
    Class that contains functions to access and modify data in an ICAT database directly
    """

    def login(self, credentials, mnemonic):
        pass

    @requires_session_id
    def get_session_details(self, session_id):
        pass

    @requires_session_id
    def refresh(self, session_id):
        pass

    @requires_session_id
    @queries_records
    def logout(self, session_id):
        pass

    @requires_session_id
    @queries_records
    def get_with_filters(self, session_id, table, filters):
        pass

    @requires_session_id
    @queries_records
    def create(self, session_id, table, data):
        pass

    @requires_session_id
    @queries_records
    def update(self, session_id, table, data):
        pass

    @requires_session_id
    @queries_records
    def get_one_with_filters(self, session_id, table, filters):
        pass

    @requires_session_id
    @queries_records
    def count_with_filters(self, session_id, table, filters):
        pass

    @requires_session_id
    @queries_records
    def get_with_id(self, session_id, table, id):
        pass

    @requires_session_id
    @queries_records
    def delete_with_id(self, session_id, table, id):
        pass

    @requires_session_id
    @queries_records
    def update_with_id(self, session_id, table, id, data):
        pass

    @requires_session_id
    @queries_records
    def get_instrument_facilitycycles_with_filters(self, session_id, instrument_id, filters):
        pass

    @requires_session_id
    @queries_records
    def count_instrument_facilitycycles_with_filters(self, session_id, instrument_id, filters):
        pass
        #return get_facility_cycles_for_instrument_count(instrument_id, filters)

    @requires_session_id
    @queries_records
    def get_instrument_facilitycycle_investigations_with_filters(self, session_id, instrument_id, facilitycycle_id, filters):
        pass
        #return get_investigations_for_instrument_in_facility_cycle(instrument_id, facilitycycle_id, filters)

    @requires_session_id
    @queries_records
    def count_instrument_facilitycycles_investigations_with_filters(self, session_id, instrument_id, facilitycycle_id, filters):
        pass
        #return get_investigations_for_instrument_in_facility_cycle_count(instrument_id, facilitycycle_id, filters)

