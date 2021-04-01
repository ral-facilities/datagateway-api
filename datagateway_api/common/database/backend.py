import datetime
import logging
import uuid

from datagateway_api.common.backend import Backend
from datagateway_api.common.database.helpers import (
    create_rows_from_json,
    delete_row_by_id,
    get_facility_cycles_for_instrument,
    get_facility_cycles_for_instrument_count,
    get_filtered_row_count,
    get_first_filtered_row,
    get_investigations_for_instrument_in_facility_cycle,
    get_investigations_for_instrument_in_facility_cycle_count,
    get_row_by_id,
    get_rows_by_filter,
    insert_row_into_table,
    patch_entities,
    requires_session_id,
    update_row_from_id,
)
from datagateway_api.common.database.models import SESSION
from datagateway_api.common.exceptions import AuthenticationError
from datagateway_api.common.helpers import get_entity_object_from_name, queries_records


log = logging.getLogger()


class DatabaseBackend(Backend):
    """
    Class that contains functions to access and modify data in an ICAT database directly
    """

    def login(self, credentials):
        if credentials["username"] == "user" and credentials["password"] == "password":
            session_id = str(uuid.uuid1())
            insert_row_into_table(
                SESSION,
                SESSION(
                    id=session_id,
                    username=f"{credentials['mechanism']}/root",
                    expireDateTime=datetime.datetime.now() + datetime.timedelta(days=1),
                ),
            )
            return session_id
        else:
            raise AuthenticationError("Username and password are incorrect")

    @requires_session_id
    def get_session_details(self, session_id):
        return get_row_by_id(SESSION, session_id).to_dict()

    @requires_session_id
    def refresh(self, session_id):
        return session_id

    @requires_session_id
    @queries_records
    def logout(self, session_id):
        return delete_row_by_id(SESSION, session_id)

    @requires_session_id
    @queries_records
    def get_with_filters(self, session_id, entity_type, filters):
        table = get_entity_object_from_name(entity_type)
        return get_rows_by_filter(table, filters)

    @requires_session_id
    @queries_records
    def create(self, session_id, entity_type, data):
        table = get_entity_object_from_name(entity_type)
        return create_rows_from_json(table, data)

    @requires_session_id
    @queries_records
    def update(self, session_id, entity_type, data):
        table = get_entity_object_from_name(entity_type)
        return patch_entities(table, data)

    @requires_session_id
    @queries_records
    def get_one_with_filters(self, session_id, entity_type, filters):
        table = get_entity_object_from_name(entity_type)
        return get_first_filtered_row(table, filters)

    @requires_session_id
    @queries_records
    def count_with_filters(self, session_id, entity_type, filters):
        table = get_entity_object_from_name(entity_type)
        return get_filtered_row_count(table, filters)

    @requires_session_id
    @queries_records
    def get_with_id(self, session_id, entity_type, id_):
        table = get_entity_object_from_name(entity_type)
        return get_row_by_id(table, id_).to_dict()

    @requires_session_id
    @queries_records
    def delete_with_id(self, session_id, entity_type, id_):
        table = get_entity_object_from_name(entity_type)
        return delete_row_by_id(table, id_)

    @requires_session_id
    @queries_records
    def update_with_id(self, session_id, entity_type, id_, data):
        table = get_entity_object_from_name(entity_type)
        return update_row_from_id(table, id_, data)

    @requires_session_id
    @queries_records
    def get_facility_cycles_for_instrument_with_filters(
        self, session_id, instrument_id, filters,
    ):
        return get_facility_cycles_for_instrument(instrument_id, filters)

    @requires_session_id
    @queries_records
    def get_facility_cycles_for_instrument_count_with_filters(
        self, session_id, instrument_id, filters,
    ):
        return get_facility_cycles_for_instrument_count(instrument_id, filters)

    @requires_session_id
    @queries_records
    def get_investigations_for_instrument_facility_cycle_with_filters(
        self, session_id, instrument_id, facilitycycle_id, filters,
    ):
        return get_investigations_for_instrument_in_facility_cycle(
            instrument_id, facilitycycle_id, filters,
        )

    @requires_session_id
    @queries_records
    def get_investigation_count_instrument_facility_cycle_with_filters(
        self, session_id, instrument_id, facilitycycle_id, filters,
    ):
        return get_investigations_for_instrument_in_facility_cycle_count(
            instrument_id, facilitycycle_id, filters,
        )
