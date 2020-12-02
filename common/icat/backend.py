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
    create_client,
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
        pass

    def login(self, credentials):
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
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_session_details_helper(client)

    @requires_session_id
    def refresh(self, session_id, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return refresh_client_session(client)

    @requires_session_id
    @queries_records
    def logout(self, session_id, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return logout_icat_client(client)

    @requires_session_id
    @queries_records
    def get_with_filters(self, session_id, table, filters, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_entity_with_filters(client, table.__name__, filters)

    @requires_session_id
    @queries_records
    def create(self, session_id, table, data, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return create_entities(client, table.__name__, data)

    @requires_session_id
    @queries_records
    def update(self, session_id, table, data, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return create_entities(client, table.__name__, data)

    @requires_session_id
    @queries_records
    def get_one_with_filters(self, session_id, table, filters, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_first_result_with_filters(client, table.__name__, filters)

    @requires_session_id
    @queries_records
    def count_with_filters(self, session_id, table, filters, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_count_with_filters(client, table.__name__, filters)

    @requires_session_id
    @queries_records
    def get_with_id(self, session_id, table, id_, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_entity_by_id(client, table.__name__, id_, True)

    @requires_session_id
    @queries_records
    def delete_with_id(self, session_id, table, id_, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return delete_entity_by_id(client, table.__name__, id_)

    @requires_session_id
    @queries_records
    def update_with_id(self, session_id, table, id_, data, **kwargs):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return update_entity_by_id(client, table.__name__, id_, data)

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
    def get_investigations_for_instrument_in_facility_cycle_with_filters(
        self, session_id, instrument_id, facilitycycle_id, filters, **kwargs,
    ):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_investigations_for_instrument_in_facility_cycle(
            client, instrument_id, facilitycycle_id, filters
        )

    @requires_session_id
    @queries_records
    def get_investigations_for_instrument_in_facility_cycle_count_with_filters(
        self, session_id, instrument_id, facilitycycle_id, filters, **kwargs,
    ):
        client = kwargs["client"] if kwargs["client"] else create_client()
        return get_investigations_for_instrument_in_facility_cycle_count(
            client, instrument_id, facilitycycle_id, filters
        )
