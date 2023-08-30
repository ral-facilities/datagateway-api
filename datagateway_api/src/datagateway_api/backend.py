from abc import ABC, abstractmethod


class Backend(ABC):
    """
    Abstact base class for implementations of a backend to inherit from
    """

    @abstractmethod
    def ping(self):
        """
        Endpoint requiring no authentication to check the API is alive and does a basic
        check to ensure the connection method to ICAT is working
        :returns: String to tell user the API is OK
        """
        pass

    @abstractmethod
    def login(self, credentials):
        """
        Attempt to log a user in using the provided credentials
        :param credentials: The user's credentials (including mechanism). Credentials
            should take the following format in JSON:
            { username: "value", password: "value", mechanism: "value"}
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
