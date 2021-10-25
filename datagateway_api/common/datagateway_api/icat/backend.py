import logging

from icat.exception import ICATError, ICATSessionError

from datagateway_api.common.backend import Backend
from datagateway_api.common.constants import Constants
from datagateway_api.common.exceptions import AuthenticationError, PythonICATError
from datagateway_api.common.helpers import queries_records
from datagateway_api.common.icat.helpers import (
    create_entities,
    delete_entity_by_id,
    get_cached_client,
    get_count_with_filters,
    get_entity_by_id,
    get_entity_with_filters,
    get_facility_cycles_for_instrument,
    get_facility_cycles_for_instrument_count,
    get_first_result_with_filters,
    get_investigations_for_instrument_in_facility_cycle,
    get_investigations_for_instrument_in_facility_cycle_count,
    get_session_details_helper,
    logout_icat_client,
    refresh_client_session,
    requires_session_id,
    update_entities,
    update_entity_by_id,
)


log = logging.getLogger()


class PythonICATBackend(Backend):
    """
    Class that contains functions to access and modify data in an ICAT database directly
    """

    def ping(self, **kwargs):
        log.info("Pinging ICAT to ensure API is alive and well")

        client_pool = kwargs.get("client_pool")
        client = get_cached_client(None, client_pool)

        try:
            entity_names = client.getEntityNames()
            log.debug("Entity names on ping: %s", entity_names)
        except ICATError as e:
            raise PythonICATError(e)

        return Constants.PING_OK_RESPONSE

    def login(self, credentials, **kwargs):
        log.info("Logging in to get session ID")
        client_pool = kwargs.get("client_pool")

        # There is no session ID required for this endpoint, a client object will be
        # fetched from cache with a blank `sessionId` attribute
        client = get_cached_client(None, client_pool)

        # Syntax for Python ICAT
        login_details = {
            "username": credentials["username"],
            "password": credentials["password"],
        }
        try:
            session_id = client.login(credentials["mechanism"], login_details)
            # Flushing client's session ID so the session ID returned in this request
            # won't be logged out next time `client.login()` is used in this function.
            # `login()` calls `self.logout()` if `sessionId` is set
            client.sessionId = None

            return session_id
        except ICATSessionError:
            raise AuthenticationError("User credentials are incorrect")

    @requires_session_id
    def get_session_details(self, session_id, **kwargs):
        log.info("Getting session details for session: %s", session_id)
        return get_session_details_helper(kwargs.get("client"))

    @requires_session_id
    def refresh(self, session_id, **kwargs):
        log.info("Refreshing session: %s", session_id)
        return refresh_client_session(kwargs.get("client"))

    @requires_session_id
    @queries_records
    def logout(self, session_id, **kwargs):
        log.info("Logging out of the Python ICAT client")
        return logout_icat_client(kwargs.get("client"))

    @requires_session_id
    @queries_records
    def get_with_filters(self, session_id, entity_type, filters, **kwargs):
        return get_entity_with_filters(kwargs.get("client"), entity_type, filters)

    @requires_session_id
    @queries_records
    def create(self, session_id, entity_type, data, **kwargs):
        return create_entities(kwargs.get("client"), entity_type, data)

    @requires_session_id
    @queries_records
    def update(self, session_id, entity_type, data, **kwargs):
        return update_entities(kwargs.get("client"), entity_type, data)

    @requires_session_id
    @queries_records
    def get_one_with_filters(self, session_id, entity_type, filters, **kwargs):
        return get_first_result_with_filters(kwargs.get("client"), entity_type, filters)

    @requires_session_id
    @queries_records
    def count_with_filters(self, session_id, entity_type, filters, **kwargs):
        return get_count_with_filters(kwargs.get("client"), entity_type, filters)

    @requires_session_id
    @queries_records
    def get_with_id(self, session_id, entity_type, id_, **kwargs):
        return get_entity_by_id(kwargs.get("client"), entity_type, id_, True)

    @requires_session_id
    @queries_records
    def delete_with_id(self, session_id, entity_type, id_, **kwargs):
        return delete_entity_by_id(kwargs.get("client"), entity_type, id_)

    @requires_session_id
    @queries_records
    def update_with_id(self, session_id, entity_type, id_, data, **kwargs):
        return update_entity_by_id(kwargs.get("client"), entity_type, id_, data)

    @requires_session_id
    @queries_records
    def get_facility_cycles_for_instrument_with_filters(
        self, session_id, instrument_id, filters, **kwargs,
    ):
        return get_facility_cycles_for_instrument(
            kwargs.get("client"), instrument_id, filters,
        )

    @requires_session_id
    @queries_records
    def get_facility_cycles_for_instrument_count_with_filters(
        self, session_id, instrument_id, filters, **kwargs,
    ):
        return get_facility_cycles_for_instrument_count(
            kwargs.get("client"), instrument_id, filters,
        )

    @requires_session_id
    @queries_records
    def get_investigations_for_instrument_facility_cycle_with_filters(
        self, session_id, instrument_id, facilitycycle_id, filters, **kwargs,
    ):
        return get_investigations_for_instrument_in_facility_cycle(
            kwargs.get("client"), instrument_id, facilitycycle_id, filters,
        )

    @requires_session_id
    @queries_records
    def get_investigation_count_instrument_facility_cycle_with_filters(
        self, session_id, instrument_id, facilitycycle_id, filters, **kwargs,
    ):
        return get_investigations_for_instrument_in_facility_cycle_count(
            kwargs.get("client"), instrument_id, facilitycycle_id, filters,
        )
