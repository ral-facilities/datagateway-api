from common.backend import Backend
from common.database_helpers import get_facility_cycles_for_instrument, get_facility_cycles_for_instrument_count, \
    get_investigations_for_instrument_in_facility_cycle, get_investigations_for_instrument_in_facility_cycle_count, \
    get_rows_by_filter, create_rows_from_json, patch_entities, get_row_by_id, insert_row_into_table, \
    delete_row_by_id, update_row_from_id, get_filtered_row_count, get_first_filtered_row
from common.helpers import requires_session_id, queries_records
from common.models.db_models import SESSION
import uuid
from common.exceptions import AuthenticationError
import datetime


class DatabaseBackend(Backend):
    """
    Class that contains functions to access and modify data in an ICAT database directly
    """

    def login(self, credentials):
        if credentials["username"] == "user" and credentials["password"] == "password":
            session_id = str(uuid.uuid1())
            insert_row_into_table(SESSION, SESSION(ID=session_id, USERNAME="simple/root",
                                                   EXPIREDATETIME=datetime.datetime.now() + datetime.timedelta(days=1)))
            return session_id
        else:
            raise AuthenticationError("Username and password are incorrect")

    @requires_session_id
    def get_session_details(self, session_id):
        return get_row_by_id(SESSION, session_id)

    @requires_session_id
    def refresh(self, session_id):
        return session_id

    @requires_session_id
    @queries_records
    def logout(self, session_id):
        return delete_row_by_id(SESSION, session_id)

    @requires_session_id
    @queries_records
    def get_with_filters(self, session_id, table, filters):
        return get_rows_by_filter(table, filters)

    @requires_session_id
    @queries_records
    def create(self, session_id, table, data):
        return create_rows_from_json(table, data)

    @requires_session_id
    @queries_records
    def update(self, session_id, table, data):
        return patch_entities(table, data)

    @requires_session_id
    @queries_records
    def get_one_with_filters(self, session_id, table, filters):
        return get_first_filtered_row(table, filters)

    @requires_session_id
    @queries_records
    def count_with_filters(self, session_id, table, filters):
        return get_filtered_row_count(table, filters)

    @requires_session_id
    @queries_records
    def get_with_id(self, session_id, table, id):
        return get_row_by_id(table, id).to_dict()

    @requires_session_id
    @queries_records
    def delete_with_id(self, session_id, table, id):
        return delete_row_by_id(table, id)

    @requires_session_id
    @queries_records
    def update_with_id(self, session_id, table, id, data):
        return update_row_from_id(table, id, data)

    @requires_session_id
    @queries_records
    def get_instrument_facilitycycles_with_filters(self, session_id, instrument_id, filters):
        return get_facility_cycles_for_instrument(instrument_id, filters)

    @requires_session_id
    @queries_records
    def count_instrument_facilitycycles_with_filters(self, session_id, instrument_id, filters):
        return get_facility_cycles_for_instrument_count(instrument_id, filters)

    @requires_session_id
    @queries_records
    def get_instrument_facilitycycle_investigations_with_filters(self, session_id, instrument_id, facilitycycle_id, filters):
        return get_investigations_for_instrument_in_facility_cycle(instrument_id, facilitycycle_id, filters)

    @requires_session_id
    @queries_records
    def count_instrument_facilitycycles_investigations_with_filters(self, session_id, instrument_id, facilitycycle_id, filters):
        return get_investigations_for_instrument_in_facility_cycle_count(instrument_id, facilitycycle_id, filters)
