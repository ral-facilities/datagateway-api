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


def construct_icat_query(client, entity_name, conditions=None, aggregate=None):
    """
    Create a Query object within Python ICAT 

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param entity_name: Name of the entity to get data from
    :type entity_name: TODO
    :param conditions: TODO
    :type conditions: TODO
    :param aggregate: Name of the aggregate function to apply. Operations such as counting the
        number of records. See `icat.query.setAggregate for valid values.
    :type aggregate: :class:`str`
    :return: Query object from Python ICAT
    """
    return Query(client, entity_name, conditions=conditions, aggregate=aggregate)


def execute_icat_query(client, query):
    """
    Execute a previously created ICAT Query object

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param query: ICAT Query object to execute within Python ICAT
    :type query: :class:`icat.query.Query`
    :return: Data (of type list) from the executed query in a format that can be converted
        straight to JSON
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


def get_python_icat_entity_name(client, database_table_name):
    """
    From the database table name, this function returns the correctly cased entity name relating
    to the table name

    Due to the case sensitivity of Python ICAT, the table name must be compared with each of the
    valid entity names within Python ICAT to get the correctly cased entity name. This is done by
    putting everything to lowercase and comparing from there

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param database_table_name: Table name (from icatdb) to be interacted with
    :type database_table_name: :class:`str`
    :return: Entity name (of type string) in the correct casing ready to be passed into Python ICAT
    """

    lowercase_table_name = database_table_name.lower()
    entity_names = client.getEntityNames()
    python_icat_entity_name = None
    for entity_name in entity_names:
        lowercase_name = entity_name.lower()

        if lowercase_name == lowercase_table_name:
            python_icat_entity_name = entity_name

    # Raise a 400 if a valid entity cannot be found
    if python_icat_entity_name is None:
        raise BadRequestError(f"Bad request made, cannot find {database_table_name} entity within Python ICAT")

    return python_icat_entity_name


def get_entity_by_id(client, table_name, id):
    """
    Gets a record of a given ID of the specified entity

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param table_name: Table name to extract which entity to use
    :type table_name: TODO
    :param id: ID number of the entity to retrieve
    :type id: :class:`int`
    :return: The record of the specified ID from the given entity
    """

    # Set query condition for the selected ID
    # TODO - Could this be moved out of this function for more generic conditions that'll be implemented later on?
    id_condition = {}
    operator = '='
    id_condition[attribute_name] = f"{operator} '{id}'"

    selected_entity_name = get_python_icat_entity_name(client, table_name)

    id_query = construct_icat_query(client, selected_entity_name, id_condition)
    entity_by_id_data = execute_icat_query(client, id_query)

    return entity_by_id_data


def update_entity_by_id(client, table_name, id, new_data):
    """
    Updates certain attributes Gets a record of a given ID of the specified entity

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param table_name: Table name to extract which entity to use
    :type table_name: TODO
    :param id: ID number of the entity to retrieve
    :type id: :class:`int`
    :param new_data: JSON from request body providing new data to update the record with the
        specified ID
    """

    pass

    return entity_by_id_data
