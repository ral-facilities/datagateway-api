import logging

import icat.client
from icat.exception import ICATSessionError

from common.backend import Backend
from common.helpers import queries_records, requires_session_id
from common.config import config
from common.exceptions import AuthenticationError
from common.models.db_models import SESSION

log = logging.getLogger()

class PythonICATBackend(Backend):
    """
    Class that contains functions to access and modify data in an ICAT database directly
    """
    
    def __init__(self):
        icat_server_url = config.get_icat_url()
        self.client = icat.client.Client(icat_server_url, checkCert=config.get_icat_check_cert())

    def login(self, credentials):
        # Syntax for Python ICAT
        login_details = {'username': credentials['username'], 'password': credentials['password']}

        try:
            session_id = self.client.login(credentials["mechanism"], login_details)
            return session_id
        except ICATSessionError:
            raise AuthenticationError("User credentials are incorrect")

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
