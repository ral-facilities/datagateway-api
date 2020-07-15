from functools import wraps
import logging
from datetime import datetime, timedelta
from icat.query import Query

from icat.exception import ICATSessionError
from common.exceptions import AuthenticationError, BadRequestError

log = logging.getLogger()

def requires_session_id(method):
    """
    Decorator for Python ICAT backend methods that looks out for session errors when using the API.
    The API call runs and an ICATSessionError may be raised due to an expired session, invalid 
    session ID etc. This does not explictly check whether a session ID is valid or not, 
    :param method: The method for the backend operation
    :raises AuthenticationError, if a valid session_id is not provided with the request
    """

    @wraps(method)
    def wrapper_requires_session(*args, **kwargs):
        try:

            client = args[0].client
            # Find out if session has expired
            session_time = client.getRemainingMinutes()
            log.info("Session time: {}".format(session_time))
            if session_time < 0:
                raise AuthenticationError("Forbidden")
            else:
                return method(*args, **kwargs)
        except ICATSessionError:
            raise AuthenticationError("Forbidden")

    return wrapper_requires_session


def queries_records(method):
    """
    Docstring
    """

    @wraps(method)
    def wrapper_gets_records(*args, **kwargs):
        pass

    return wrapper_gets_records


def get_session_details_helper(client):
    # Remove rounding 
    session_time_remaining = client.getRemainingMinutes()
    session_expiry_time = datetime.now() + timedelta(minutes=session_time_remaining)

    username = client.getUserName()

    return {"ID": client.sessionId, "EXPIREDATETIME": str(session_expiry_time), "USERNAME": username}


def logout_icat_client(client):
    client.logout()


def refresh_client_session(client):
    client.refresh()


def construct_icat_query(client, entity_name, conditions=None):
    """
    Create a Query object within Python ICAT 

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param entity_name: Name of the entity to get data from
    :type entity_name: TODO
    :param conditions: TODO
    :type conditions: TODO
    :return: Query object from Python ICAT
    """
    return Query(client, entity_name, conditions=conditions)


def execute_icat_query(client, query):
    """
    Execute a previously created ICAT Query object

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param query: ICAT Query object to execute within Python ICAT
    :type query: :class:`icat.query.Query`
    :return: Data (of type list) from the executed query in a format that can be converted straight to JSON
    """
    query_result = client.search(query)

    data = []
    for result in query_result:
        dict_result = result.as_dict()
        for key, value in dict_result.items():
            # Convert datetime objects to strings so they can be JSON serialisable
            if isinstance(dict_result[key], datetime):
                dict_result[key] = str(dict_result[key])

        data.append(dict_result)

    return data


def get_entity_by_id(client, table, id):
    """
    Gets a record of a given ID of the specified entity

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param table: Table to extract which entity to use
    :type table: TODO
    :param id: ID number of the entity to retrieve
    :type id: :class:`int`
    :return: The record of the specified ID from the given entity
    """

    # Set query condition for the selected ID
    # TODO - Could this be moved out of this function for more generic conditions that'll be implemented later on?
    id_condition = {'id': f'= {id}'}

    # Due to the case sensitivity of Python ICAT, the table name must be compared with each of the
    # valid entity names within Python ICAT to get the correctly cased entity name. This is done by
    # putting everything to lowercase and comparing from there
    lowercase_table_name = table.__name__.lower()
    entity_names = client.getEntityNames()
    selected_entity = None
    for entity_name in entity_names:
        lowercase_name = entity_name.lower()

        if lowercase_name == lowercase_table_name:
            selected_entity = entity_name

    # Raise a 400 if a valid entity cannot be found
    if selected_entity is None:
        raise BadRequestError(f"Bad request made, cannot find {table.__name__} entity within Python ICAT")

    id_query = construct_icat_query(client, selected_entity, id_condition)
    entity_by_id_data = execute_icat_query(client, id_query)

    return entity_by_id_data
