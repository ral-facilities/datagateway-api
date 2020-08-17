from abc import ABC, abstractmethod


class Backend(ABC):
    """
    Abstact base class for implementations of a backend to inherit from
    """

    @abstractmethod
    def login(self, credentials):
        """
        Attempt to log a user in using the provided credentials
        :param credentials: The user's credentials (including mechanism)
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
        Given a list of filters supplied in json format, returns entities that match the
        filters for the given entity type

        :param session_id: The session id of the requesting user
        :param entity_type: The type of entity
        :param filters: The list of filters to be applied
        :return: A list of the matching entities in json format
        """
        pass

    @abstractmethod
    def create(self, session_id, entity_type, data):
        """
        Create one or more entities, from the given list containing json. Each entity
        must not contain its ID

        :param session_id: The session id of the requesting user
        :param entity_type: The type of entity
        :param data: The entities to be created
        :return: The created entities.
        """
        pass

    @abstractmethod
    def update(self, session_id, entity_type, data):
        """
        Update one or more entities, from the given list containing json. Each entity
        must contain its ID

        :param session_id: The session id of the requesting user
        :param entity_type: The type of entity
        :param data: the list of updated values or a dictionary
        :return: The list of updated entities.
        """
        pass

    @abstractmethod
    def get_one_with_filters(self, session_id, entity_type, filters):
        """
        Returns the first entity that matches a given filter, for a given entity type

        :param session_id: The session id of the requesting user
        :param entity_type: The type of entity
        :param filters: the filter to be applied to the query
        :return: the first entity matching the filter
        """
        pass

    @abstractmethod
    def count_with_filters(self, session_id, entity_type, filters):
        """
        Returns the count of the entities that match a given filter for a given entity
        type

        :param session_id: The session id of the requesting user
        :param entity_type: The type of entity
        :param filters: the filters to be applied to the query
        :return: int: the count of the entities
        """
        pass

    @abstractmethod
    def get_with_id(self, session_id, entity_type, id_):
        """
        Gets the entity matching the given ID for the given entity type

        :param session_id: The session id of the requesting user
        :param entity_type: The type of entity
        :param id_: the id of the record to find
        :return: the entity retrieved
        """
        pass

    @abstractmethod
    def delete_with_id(self, session_id, entity_type, id_):
        """
        Deletes the row matching the given ID for the given entity type

        :param session_id: The session id of the requesting user
        :param table: the table to be searched
        :param id_: the id of the record to delete
        """
        pass

    @abstractmethod
    def update_with_id(self, session_id, entity_type, id_, data):
        """
        Updates the row matching the given ID for the given entity type

        :param session_id: The session id of the requesting user
        :param entity_type: The type of entity
        :param id_: the id of the record to update
        :param data: The dictionary that the entity should be updated with
        :return: The updated entity.
        """
        pass

    @abstractmethod
    def get_instrument_facilitycycles_with_filters(
        self, session_id, instrument_id, filters
    ):
        """
        Given an instrument_id get facility cycles where the instrument has
        investigations that occur within that cycle

        :param session_id: The session id of the requesting user
        :param filters: The filters to be applied to the query
        :param instrument_id: The id of the instrument
        :return: A list of facility cycle entities
        """
        pass

    @abstractmethod
    def count_instrument_facilitycycles_with_filters(
        self, session_id, instrument_id, filters
    ):
        """
        Given an instrument_id get the facility cycles count where the instrument has
        investigations that occur within that cycle

        :param session_id: The session id of the requesting user
        :param filters: The filters to be applied to the query
        :param instrument_id: The id of the instrument
        :return: The count of the facility cycles
        """
        pass

    @abstractmethod
    def get_instrument_facilitycycle_investigations_with_filters(
        self, session_id, instrument_id, facilitycycle_id, filters
    ):
        """
        Given an instrument id and facility cycle id, get investigations that use the
        given instrument in the given cycle

        :param session_id: The session id of the requesting user
        :param filters: The filters to be applied to the query
        :param instrument_id: The id of the instrument
        :param facility_cycle_id:  the ID of the facility cycle
        :return: The investigations
        """
        pass

    @abstractmethod
    def count_instrument_facilitycycles_investigations_with_filters(
        self, session_id, instrument_id, facilitycycle_id, filters
    ):
        """
        Given an instrument id and facility cycle id, get the count of the
        investigations that use the given instrument in the given cycle
        
        :param session_id: The session id of the requesting user
        :param filters: The filters to be applied to the query
        :param instrument_id: The id of the instrument
        :param facility_cycle_id:  the ID of the facility cycle
        :return: The investigations count
        """
        pass
