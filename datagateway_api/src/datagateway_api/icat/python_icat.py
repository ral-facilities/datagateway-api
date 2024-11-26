import logging

from icat.exception import ICATError, ICATSessionError

from datagateway_api.src.common.constants import Constants
from datagateway_api.src.common.exceptions import AuthenticationError, PythonICATError
from datagateway_api.src.common.helpers import queries_records
from datagateway_api.src.datagateway_api.icat.helpers import (
    create_entities,
    delete_entity_by_id,
    get_cached_client,
    get_count_with_filters,
    get_entity_by_id,
    get_entity_with_filters,
    get_first_result_with_filters,
    get_session_details_helper,
    logout_icat_client,
    refresh_client_session,
    requires_session_id,
    update_entities,
    update_entity_by_id,
)


log = logging.getLogger()


class PythonICAT:
    """
    Class that contains functions to access and modify data in an ICAT database directly
    """

    def ping(self, **kwargs):
        """
        Endpoint requiring no authentication to check the API is alive and does a basic
        check to ensure the connection method to ICAT is working.
        :returns: String to tell user the API is OK.
        """
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
        """
        Attempt to log a user in using the provided credentials.
        :param credentials: The user's credentials (including mechanism). Credentials
            should take the following format in JSON:
            { username: "value", password: "value", mechanism: "value"}
        :returns: a session ID.
        """
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
        """
        Returns the details of a user's session.
        :param session_id: The user's session ID.
        :returns: The user's session details.
        """
        log.info("Getting session details for session: %s", session_id)
        return get_session_details_helper(kwargs.get("client"))

    @requires_session_id
    def refresh(self, session_id, **kwargs):
        """
        Attempts to refresh a user's session.
        :param session_id: The user's session ID.
        :returns: the user's refreshed session ID.
        """
        log.info("Refreshing session: %s", session_id)
        return refresh_client_session(kwargs.get("client"))

    @requires_session_id
    @queries_records
    def logout(self, session_id, **kwargs):
        """
        Logs a user out.
        :param session_id: The user's session ID.
        """
        log.info("Logging out of the Python ICAT client")
        return logout_icat_client(kwargs.get("client"))

    @requires_session_id
    @queries_records
    def get_with_filters(self, session_id, entity_type, filters, **kwargs):
        """
        Given a list of filters supplied in JSON format, returns entities that match
        the filters for the given entity type.
        :param session_id: The session ID of the requesting user.
        :param entity_type: The type of entity.
        :param filters: The list of filters to be applied.
        :return: A list of the matching entities in JSON format.
        """
        return get_entity_with_filters(kwargs.get("client"), entity_type, filters)

    @requires_session_id
    @queries_records
    def create(self, session_id, entity_type, data, **kwargs):
        """
        Create one or more entities, from the given list containing JSON. Each entity
        must not contain its ID.
        :param session_id: The session ID of the requesting user.
        :param entity_type: The type of entity.
        :param data: The entities to be created.
        :return: The created entities.
        """
        return create_entities(kwargs.get("client"), entity_type, data)

    @requires_session_id
    @queries_records
    def update(self, session_id, entity_type, data, **kwargs):
        """
        Update one or more entities, from the given list containing JSON. Each entity
        must contain its ID.
        :param session_id: The session ID of the requesting user.
        :param entity_type: The type of entity.
        :param data: The list of updated values or a dictionary.
        :return: The list of updated entities.
        """
        return update_entities(kwargs.get("client"), entity_type, data)

    @requires_session_id
    @queries_records
    def get_one_with_filters(self, session_id, entity_type, filters, **kwargs):
        """
        Returns the first entity that matches a given filter, for a given entity type.
        :param session_id: The session ID of the requesting user.
        :param entity_type: The type of entity.
        :param filters: The filter to be applied to the query.
        :return: The first entity matching the filter.
        """
        return get_first_result_with_filters(kwargs.get("client"), entity_type, filters)

    @requires_session_id
    @queries_records
    def count_with_filters(self, session_id, entity_type, filters, **kwargs):
        """
        Returns the count of the entities that match a given filter for a given entity
        type.
        :param session_id: The session ID of the requesting user.
        :param entity_type: The type of entity.
        :param filters: The filters to be applied to the query.
        :return: int: The count of the entities.
        """
        return get_count_with_filters(kwargs.get("client"), entity_type, filters)

    @requires_session_id
    @queries_records
    def get_with_id(self, session_id, entity_type, id_, **kwargs):
        """
        Gets the entity matching the given ID for the given entity type.
        :param session_id: The session ID of the requesting user.
        :param entity_type: The type of entity.
        :param id_: The ID of the record to find.
        :return: The entity retrieved.
        """
        return get_entity_by_id(kwargs.get("client"), entity_type, id_, True)

    @requires_session_id
    @queries_records
    def delete_with_id(self, session_id, entity_type, id_, **kwargs):
        """
        Deletes the row matching the given ID for the given entity type.
        :param session_id: The session ID of the requesting user.
        :param entity_type: The type of entity.
        :param id_: The ID of the record to delete.
        """
        return delete_entity_by_id(kwargs.get("client"), entity_type, id_)

    @requires_session_id
    @queries_records
    def update_with_id(self, session_id, entity_type, id_, data, **kwargs):
        """
        Updates the row matching the given ID for the given entity type.
        :param session_id: The session ID of the requesting user.
        :param entity_type: The type of entity.
        :param id_: The ID of the record to update.
        :param data: The dictionary that the entity should be updated with.
        :return: The updated entity.
        """
        return update_entity_by_id(kwargs.get("client"), entity_type, id_, data)
