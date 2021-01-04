import logging

from icat.exception import ICATSessionError

from datagateway_api.common.backend import Backend
from datagateway_api.common.exceptions import AuthenticationError
from datagateway_api.common.helpers import queries_records
from datagateway_api.common.icat.helpers import (
    create_client,
    create_entities,
    delete_entity_by_id,
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

    def __init__(self):
        pass

    def login(self, credentials):
        log.info("Logging in to get session ID")
        client = create_client()

        # Syntax for Python ICAT
        login_details = {
            "username": credentials["username"],
            "password": credentials["password"],
        }
        try:
            session_id = client.login(credentials["mechanism"], login_details)
            return session_id
        except ICATSessionError:
            raise AuthenticationError("User credentials are incorrect")

    @requires_session_id
    def get_session_details(self, session_id, **kwargs):
        log.info("Getting session details for session: %s", session_id)
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_session_details_helper(client)

    @requires_session_id
    def refresh(self, session_id, **kwargs):
        log.info("Refreshing session: %s", session_id)
        client = kwargs["client"] if kwargs["client"] else create_client()
        return refresh_client_session(client)

    @requires_session_id
    @queries_records
    def logout(self, session_id, **kwargs):
        log.info("Logging out of the Python ICAT client")
        client = kwargs["client"] if kwargs["client"] else create_client()
        return logout_icat_client(client)

    @requires_session_id
    @queries_records
    def get_with_filters(self, session_id, entity_type, filters, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_entity_with_filters(client, entity_type, filters)

    @requires_session_id
    @queries_records
    def create(self, session_id, entity_type, data, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return create_entities(client, entity_type, data)

    @requires_session_id
    @queries_records
    def update(self, session_id, entity_type, data, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return update_entities(client, entity_type, data)

    @requires_session_id
    @queries_records
    def get_one_with_filters(self, session_id, entity_type, filters, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_first_result_with_filters(client, entity_type, filters)

    @requires_session_id
    @queries_records
    def count_with_filters(self, session_id, entity_type, filters, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_count_with_filters(client, entity_type, filters)

    @requires_session_id
    @queries_records
    def get_with_id(self, session_id, entity_type, id_, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_entity_by_id(client, entity_type, id_, True)

    @requires_session_id
    @queries_records
    def delete_with_id(self, session_id, entity_type, id_, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return delete_entity_by_id(client, entity_type, id_)

    @requires_session_id
    @queries_records
    def update_with_id(self, session_id, entity_type, id_, data, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return update_entity_by_id(client, entity_type, id_, data)

    @requires_session_id
    @queries_records
    def get_facility_cycles_for_instrument_with_filters(
        self, session_id, instrument_id, filters, **kwargs,
    ):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_facility_cycles_for_instrument(client, instrument_id, filters)

    @requires_session_id
    @queries_records
    def get_facility_cycles_for_instrument_count_with_filters(
        self, session_id, instrument_id, filters, **kwargs,
    ):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_facility_cycles_for_instrument_count(client, instrument_id, filters)

    @requires_session_id
    @queries_records
    def get_investigations_for_instrument_facility_cycle_with_filters(
        self, session_id, instrument_id, facilitycycle_id, filters, **kwargs,
    ):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_investigations_for_instrument_in_facility_cycle(
            client, instrument_id, facilitycycle_id, filters,
        )

    @requires_session_id
    @queries_records
    def get_investigation_count_instrument_facility_cycle_with_filters(
        self, session_id, instrument_id, facilitycycle_id, filters, **kwargs,
    ):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_investigations_for_instrument_in_facility_cycle_count(
            client, instrument_id, facilitycycle_id, filters,
        )
