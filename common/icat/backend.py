import logging

import icat.client
from icat.exception import ICATSessionError

from common.backend import Backend
from common.helpers import queries_records
from common.icat.helpers import (
    requires_session_id,
    get_session_details_helper,
    logout_icat_client,
    refresh_client_session,
    get_entity_by_id,
    update_entity_by_id,
    delete_entity_by_id,
    get_entity_with_filters,
    get_count_with_filters,
    get_first_result_with_filters,
    update_entities,
    create_entities,
    get_facility_cycles_for_instrument,
    get_facility_cycles_for_instrument_count,
    get_investigations_for_instrument_in_facility_cycle,
    get_investigations_for_instrument_in_facility_cycle_count,
)

from common.config import config
from common.exceptions import AuthenticationError
from common.models.db_models import SESSION

log = logging.getLogger()


class PythonICATBackend(Backend):
    """
    Class that contains functions to access and modify data in an ICAT database directly
    """

    def __init__(self):
        # Client object is created here as well as in login() to avoid uncaught
        # exceptions where the object is None. This could happen where a user tries to
        # use an endpoint before logging in. Also helps to give a bit of certainty to
        # what's stored here
        self.client = icat.client.Client(
            config.get_icat_url(), checkCert=config.get_icat_check_cert()
        )

    def login(self, credentials):
        log.info("Logging in to get session ID")
        # Client object is re-created here so session IDs aren't overwritten in the
        # database
        self.client = icat.client.Client(
            config.get_icat_url(), checkCert=config.get_icat_check_cert()
        )

        # Syntax for Python ICAT
        login_details = {
            "username": credentials["username"],
            "password": credentials["password"],
        }
        try:
            session_id = self.client.login(credentials["mechanism"], login_details)
            return session_id
        except ICATSessionError:
            raise AuthenticationError("User credentials are incorrect")

    @requires_session_id
    def get_session_details(self, session_id):
        log.info("Getting session details for session: %s", session_id)
        self.client.sessionId = session_id
        return get_session_details_helper(self.client)

    @requires_session_id
    def refresh(self, session_id):
        log.info("Refreshing session: %s", session_id)
        self.client.sessionId = session_id
        return refresh_client_session(self.client)

    @requires_session_id
    @queries_records
    def logout(self, session_id):
        log.info("Logging out of the Python ICAT client")
        self.client.sessionId = session_id
        return logout_icat_client(self.client)

    @requires_session_id
    @queries_records
    def get_with_filters(self, session_id, table, filters):
        self.client.sessionId = session_id
        return get_entity_with_filters(self.client, table.__name__, filters)

    @requires_session_id
    @queries_records
    def create(self, session_id, table, data):
        self.client.sessionId = session_id
        return create_entities(self.client, table.__name__, data)

    @requires_session_id
    @queries_records
    def update(self, session_id, table, data):
        self.client.sessionId = session_id
        return update_entities(self.client, table.__name__, data)

    @requires_session_id
    @queries_records
    def get_one_with_filters(self, session_id, table, filters):
        self.client.sessionId = session_id
        return get_first_result_with_filters(self.client, table.__name__, filters)

    @requires_session_id
    @queries_records
    def count_with_filters(self, session_id, table, filters):
        self.client.sessionId = session_id
        return get_count_with_filters(self.client, table.__name__, filters)

    @requires_session_id
    @queries_records
    def get_with_id(self, session_id, table, id_):
        return get_entity_by_id(self.client, table.__name__, id_, True)

    @requires_session_id
    @queries_records
    def delete_with_id(self, session_id, table, id_):
        return delete_entity_by_id(self.client, table.__name__, id_)

    @requires_session_id
    @queries_records
    def update_with_id(self, session_id, table, id_, data):
        return update_entity_by_id(self.client, table.__name__, id_, data)

    @requires_session_id
    @queries_records
    def get_facility_cycles_for_instrument_with_filters(
        self, session_id, instrument_id, filters
    ):
        self.client.sessionId = session_id
        return get_facility_cycles_for_instrument(self.client, instrument_id, filters)

    @requires_session_id
    @queries_records
    def get_facility_cycles_for_instrument_count_with_filters(
        self, session_id, instrument_id, filters
    ):
        self.client.sessionId = session_id
        return get_facility_cycles_for_instrument_count(
            self.client, instrument_id, filters
        )

    @requires_session_id
    @queries_records
    def get_investigations_for_instrument_in_facility_cycle_with_filters(
        self, session_id, instrument_id, facilitycycle_id, filters
    ):
        self.client.sessionId = session_id
        return get_investigations_for_instrument_in_facility_cycle(
            self.client, instrument_id, facilitycycle_id, filters
        )

    @requires_session_id
    @queries_records
    def get_investigations_for_instrument_in_facility_cycle_count_with_filters(
        self, session_id, instrument_id, facilitycycle_id, filters
    ):
        self.client.sessionId = session_id
        return get_investigations_for_instrument_in_facility_cycle_count(
            self.client, instrument_id, facilitycycle_id, filters
        )
