from abc import ABC, abstractmethod
from common.database_helpers import get_investigations_for_user, get_investigations_for_user_count, \
    get_facility_cycles_for_instrument, get_facility_cycles_for_instrument_count, \
    get_investigations_for_instrument_in_facility_cycle, get_investigations_for_instrument_in_facility_cycle_count, \
    get_rows_by_filter, create_rows_from_json, patch_entities, get_row_by_id, insert_row_into_table, \
    delete_row_by_id, update_row_from_id, get_filtered_row_count, get_first_filtered_row
from common.helpers import requires_session_id, queries_records
from common.models.db_models import SESSION
from common.config import config
import uuid
import sys
from common.exceptions import AuthenticationError


class Backend(ABC):
    """
    Abstact base class for implementations of a backend to inherit from
    """

    @abstractmethod
    def login(self, credentials):
        """
        Attempt to log a user in using the provided credentials
        :param credentials: The user's credentials
        :returns: a session ID
        """
        pass

    @abstractmethod
    def get_session_details(self, session_id):
        """
        Returns the details of a user's session
        :param session_id: The user's session ID
        :returns: The user's session details
        """
        pass

    @abstractmethod
    def refresh(self, session_id):
        """
        Attempts to refresh a user's session
        :param session_id: The user's session ID
        :returns: the user's refreshed session ID
        """
        pass

    @abstractmethod
    def logout(self, session_id):
        """
        Logs a user out
        :param session_id: The user's session ID
        """
        pass

    @abstractmethod
    def get_with_filters(self, session_id, entity_type, filters):
        """
        Given a list of filters supplied in json format, returns entities that match the filters for the given entity type
        :param session_id: The session id of the requesting user
        :param entity_type: The type of entity
        :param filters: The list of filters to be applied
        :return: A list of the matching entities in json format
        """
        pass

    @abstractmethod
    def create(self, session_id, entity_type, data):
        """
        Create one or more entities, from the given list containing json. Each entity must not contain its ID
        :param session_id: The session id of the requesting user
        :param entity_type: The type of entity
        :param data: The entities to be created
        :return: The created entities.
        """
        pass

    @abstractmethod
    def update(self, session_id, entity_type, data):
        """
        Update one or more entities, from the given list containing json. Each entity must contain its ID
        :param session_id: The session id of the requesting user
        :param entity_type: The type of entity
        :param data: the list of updated values or a dictionary
        :return: The list of updated entities.
        """
        pass

    @abstractmethod
    def get_one_with_filters(self, session_id, entity_type, filters):
        """
        returns the first entity that matches a given filter, for a given entity type
        :param session_id: The session id of the requesting user
        :param entity_type: The type of entity
        :param filters: the filter to be applied to the query
        :return: the first entity matching the filter
        """
        pass

    @abstractmethod
    def count_with_filters(self, session_id, entity_type, filters):
        """
        returns the count of the entities that match a given filter for a given entity type
        :param session_id: The session id of the requesting user
        :param entity_type: The type of entity
        :param filters: the filters to be applied to the query
        :return: int: the count of the entities
        """
        pass

    @abstractmethod
    def get_with_id(self, session_id, entity_type, id):
        """
        Gets the entity matching the given ID for the given entity type
        :param session_id: The session id of the requesting user
        :param entity_type: The type of entity
        :param id: the id of the record to find
        :return: the entity retrieved
        """
        pass

    @abstractmethod
    def delete_with_id(self, session_id, entity_type, id):
        """
        Deletes the row matching the given ID for the given entity type
        :param session_id: The session id of the requesting user
        :param table: the table to be searched
        :param id: the id of the record to delete
        """
        pass

    @abstractmethod
    def update_with_id(self, session_id, entity_type, id, data):
        """
        Updates the row matching the given ID for the given entity type
        :param session_id: The session id of the requesting user
        :param entity_type: The type of entity
        :param data: The dictionary that the entity should be updated with
        :return: The updated entity.
        """
        pass

    @abstractmethod
    def get_users_investigations_with_filters(self, session_id, user_id, filters):
        """
        Given a user id and a list of filters, return a filtered list of all investigations that belong to that user
        :param session_id: The session id of the requesting user
        :param user_id: The id of the user
        :param filters: The list of filters
        :return: A list of dictionary representations of the investigation entities
        """
        pass

    @abstractmethod
    def count_users_investigations_with_filters(self, session_id, user_id, filters):
        """
        Given a user id and a list of filters, return the count of all investigations that belong to that user
        :param session_id: The session id of the requesting user
        :param user_id: The id of the user
        :param filters: The list of filters
        :return: The count
        """
        pass

    @abstractmethod
    def get_instrument_facilitycycles_with_filters(self, session_id, instrument_id, filters):
        """
        Given an instrument_id get facility cycles where the instrument has investigations that occur within that cycle
        :param session_id: The session id of the requesting user
        :param filters: The filters to be applied to the query
        :param instrument_id: The id of the instrument
        :return: A list of facility cycle entities
        """
        pass

    @abstractmethod
    def count_instrument_facilitycycles_with_filters(self, session_id, instrument_id, filters):
        """
        Given an instrument_id get the facility cycles count where the instrument has investigations that occur within
        that cycle
        :param session_id: The session id of the requesting user
        :param filters: The filters to be applied to the query
        :param instrument_id: The id of the instrument
        :return: The count of the facility cycles
        """
        pass

    @abstractmethod
    def get_instrument_facilitycycle_investigations_with_filters(self, session_id, instrument_id, facilitycycle_id, filters):
        """
        Given an instrument id and facility cycle id, get investigations that use the given instrument in the given cycle
        :param session_id: The session id of the requesting user
        :param filters: The filters to be applied to the query
        :param instrument_id: The id of the instrument
        :param facility_cycle_id:  the ID of the facility cycle
        :return: The investigations
        """
        pass

    @abstractmethod
    def count_instrument_facilitycycles_investigations_with_filters(self, session_id, instrument_id, facilitycycle_id, filters):
        """
        Given an instrument id and facility cycle id, get the count of the investigations that use the given instrument in
        the given cycle
        :param session_id: The session id of the requesting user
        :param filters: The filters to be applied to the query
        :param instrument_id: The id of the instrument
        :param facility_cycle_id:  the ID of the facility cycle
        :return: The investigations count
        """
        pass


class DatabaseBackend(Backend):
    """
    Class that contains functions to access and modify data in an ICAT database directly
    """

    def login(self, credentials):
        if credentials["username"] == "user" and credentials["password"] == "password":
            session_id = str(uuid.uuid1())
            insert_row_into_table(SESSION, SESSION(ID=session_id))
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
    def get_users_investigations_with_filters(self, session_id, user_id, filters):
        return get_investigations_for_user(user_id, filters)

    @requires_session_id
    @queries_records
    def count_users_investigations_with_filters(self, session_id, user_id, filters):
        return get_investigations_for_user_count(user_id, filters)

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


backend_type = config.get_backend_type()

if backend_type == "db":
    backend = DatabaseBackend()
else:
    sys.exit(
        f"Invalid config value '{backend_type}' for config option backend")
    backend = Backend()
