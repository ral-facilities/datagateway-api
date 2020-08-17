from functools import wraps
import logging
from datetime import datetime, timedelta

from icat.query import Query
from icat.exception import ICATSessionError, ICATValidationError
from common.exceptions import (
    AuthenticationError,
    BadRequestError,
    MissingRecordError,
    PythonICATError,
)
from common.filters import FilterOrderHandler
from common.constants import Constants


log = logging.getLogger()


def requires_session_id(method):
    """
    Decorator for Python ICAT backend methods that looks out for session errors when
    using the API. The API call runs and an ICATSessionError may be raised due to an
    expired session, invalid session ID etc.
 
    :param method: The method for the backend operation
    :raises AuthenticationError: If a valid session_id is not provided with the request
    """

    @wraps(method)
    def wrapper_requires_session(*args, **kwargs):
        try:

            client = args[0].client
            # Find out if session has expired
            session_time = client.getRemainingMinutes()
            log.info("Session time: %d", session_time)
            if session_time < 0:
                raise AuthenticationError("Forbidden")
            else:
                return method(*args, **kwargs)
        except ICATSessionError:
            raise AuthenticationError("Forbidden")

    return wrapper_requires_session


def get_session_details_helper(client):
    """
    Retrieve details regarding the current session within `client`

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :return: Details of the user's session, ready to be converted into a JSON response
        body
    """
    # Remove rounding
    session_time_remaining = client.getRemainingMinutes()
    session_expiry_time = datetime.now() + timedelta(minutes=session_time_remaining)

    username = client.getUserName()

    return {
        "ID": client.sessionId,
        "EXPIREDATETIME": str(session_expiry_time),
        "USERNAME": username,
    }


def logout_icat_client(client):
    """
    Logout a user of the currently authenticated user within `client`

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    """

    client.logout()


def refresh_client_session(client):
    """
    Refresh the session of the currently authenticated user within `client`

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    """
    client.refresh()


def construct_icat_query(
    client, entity_name, conditions=None, aggregate=None, includes=None
):
    """
    Create a Query object within Python ICAT 

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param entity_name: Name of the entity to get data from
    :type entity_name: :class:`suds.sax.text.Text`
    :param conditions: Constraints used when an entity is queried
    :type conditions: :class:`dict`
    :param aggregate: Name of the aggregate function to apply. Operations such as
        counting the number of records. See `icat.query.setAggregate` for valid values.
    :type aggregate: :class:`str`
    :param includes: List of related entity names to add to the query so related
        entities (and their data) can be returned with the query result
    :type includes: :class:`str` or iterable of :class:`str`
    :return: Query object from Python ICAT
    :raises PythonICATError: If a ValueError is raised when creating a Query(), 500 will
        be returned as a response
    """

    try:
        query = Query(
            client,
            entity_name,
            conditions=conditions,
            aggregate=aggregate,
            includes=includes,
        )
    except ValueError:
        raise PythonICATError(
            "An issue has occurred while creating a Python ICAT Query object,"
            " suggesting an invalid argument"
        )

    return query


def execute_icat_query(client, query, return_json_formattable=False):
    """
    Execute a previously created ICAT Query object and return in the format specified
    by the return_json_formattable flag

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param query: ICAT Query object to execute within Python ICAT
    :type query: :class:`icat.query.Query`
    :param return_json_formattable: Flag to determine whether the data from the query
        should be returned as a list of data ready to be converted straight to JSON 
        (i.e. if the data will be used as a response for an API call) or whether to
        leave the data in a Python ICAT format (i.e. if it's going to be manipulated at
        some point)
    :type return_json_formattable_data: :class:`bool`
    :return: Data (of type list) from the executed query
    """

    try:
        query_result = client.search(query)
    except ICATValidationError as e:
        raise PythonICATError(e)

    if return_json_formattable:
        data = []
        for result in query_result:
            dict_result = result.as_dict()
            for key, value in dict_result.items():
                # Convert datetime objects to strings so they can be JSON serialisable
                if isinstance(value, datetime):
                    # Remove timezone data which isn't utilised in ICAT
                    dict_result[key] = value.replace(tzinfo=None).strftime(
                        Constants.ACCEPTED_DATE_FORMAT
                    )

            data.append(dict_result)
        return data
    else:
        return query_result


def get_python_icat_entity_name(client, database_table_name):
    """
    From the database table name, this function returns the correctly cased entity name
    relating to the table name

    Due to the case sensitivity of Python ICAT, the table name must be compared with
    each of the valid entity names within Python ICAT to get the correctly cased entity
    name. This is done by putting everything to lowercase and comparing from there

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param database_table_name: Table name (from icatdb) to be interacted with
    :type database_table_name: :class:`str`
    :return: Entity name (of type string) in the correct casing ready to be passed into
        Python ICAT
    :raises BadRequestError: If the entity cannot be found
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
        raise BadRequestError(
            f"Bad request made, cannot find {database_table_name} entity within Python"
            " ICAT"
        )

    return python_icat_entity_name


def create_condition(attribute_name, operator, value):
    """
    Construct and return a Python dictionary containing conditions to be used in a
    Query object

    :param attribute_name: Attribute name to search
    :type attribute_name: :class:`str`
    :param operator: Operator to use when filtering the data
    :type operator: :class:`str`
    :param value: What ICAT will use to filter the data
    :type value: :class:`str` or :class:`tuple` (when using an IN expression)
    :return: Condition (of type :class:`dict`) ready to be added to a Python ICAT Query
        object
    """

    conditions = {}
    # Removing quote marks when doing conditions with IN expressions
    jpql_value = f"{value}" if isinstance(value, tuple) else f"'{value}'"
    conditions[attribute_name] = f"{operator} {jpql_value}"

    return conditions


def str_to_datetime_object(icat_attribute, data):
    """
    Where data is stored as dates in ICAT (which this function determines), convert 
    strings (i.e. user data from PATCH/POST requests) into datetime objects so they can
    be stored in ICAT

    Python 3.7+ has support for `datetime.fromisoformat()` which would be a more elegant
    solution to this conversion operation since dates are converted into ISO format
    within this file, however, the production instance of this API is typically built on
    Python 3.6, and it doesn't seem of enough value to mandate 3.7 for a single line of
    code

    :param icat_attribute: Attribute that will be updated with new data
    :type icat_attribute: Any valid data type that can be stored in Python ICAT
    :param data: Single data value from the request body
    :type data: Data type of the data as per user's request body
    :return: Date converted into a :class:`datetime` object
    :raises BadRequestError: If the date is entered in the incorrect format, as per
        `Constants.ACCEPTED_DATE_FORMAT`
    """

    try:
        data = datetime.strptime(data, Constants.ACCEPTED_DATE_FORMAT)
    except ValueError:
        raise BadRequestError(
            "Bad request made, the date entered is not in the correct format. Use the"
            f" {Constants.ACCEPTED_DATE_FORMAT} format to submit dates to the API"
        )

    return data


def update_attributes(old_entity, new_entity):
    """
    Updates the attribute(s) of a given object which is a record of an entity from
    Python ICAT

    :param old_entity: An existing entity record from Python ICAT
    :type object: :class:`icat.entities.ENTITY`
    :param new_entity: Dictionary containing the new data to be modified
    :type new_entity: :class:`dict`
    :raises BadRequestError: If the attribute cannot be found, or if it cannot be edited
        - typically if Python ICAT doesn't allow an attribute to be edited (e.g. modId &
        modTime)
    """
    for key in new_entity:
        try:
            original_data_attribute = getattr(old_entity, key)
            if isinstance(original_data_attribute, datetime):
                new_entity[key] = str_to_datetime_object(
                    original_data_attribute, new_entity[key]
                )
        except AttributeError:
            raise BadRequestError(
                f"Bad request made, cannot find attribute '{key}' within the"
                f"{old_entity.BeanName} entity"
            )

        try:
            setattr(old_entity, key, new_entity[key])
        except AttributeError:
            raise BadRequestError(
                f"Bad request made, cannot modify attribute '{key}' within the"
                f" {old_entity.BeanName} entity"
            )

    try:
        old_entity.update()
    except ICATValidationError as e:
        raise PythonICATError(e)


def get_entity_by_id(client, table_name, id_, return_json_formattable_data):
    """
    Gets a record of a given ID from the specified entity

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param table_name: Table name to extract which entity to use
    :type table_name: :class:`str`
    :param id_: ID number of the entity to retrieve
    :type id_: :class:`int`
    :param return_json_formattable_data: Flag to determine whether the data should be 
        returned as a list of data ready to be converted straight to JSON (i.e. if the
        data will be used as a response for an API call) or whether to leave the data in
        a Python ICAT format
    :type return_json_formattable_data: :class:`bool`
    :return: The record of the specified ID from the given entity
    :raises: MissingRecordError: If Python ICAT cannot find a record of the specified ID
    """

    # Set query condition for the selected ID
    id_condition = create_condition("id", "=", id_)

    selected_entity_name = get_python_icat_entity_name(client, table_name)

    id_query = construct_icat_query(
        client, selected_entity_name, conditions=id_condition, includes="1"
    )
    entity_by_id_data = execute_icat_query(
        client, id_query, return_json_formattable_data
    )

    if not entity_by_id_data:
        # Cannot find any data matching the given ID
        raise MissingRecordError("No result found")
    else:
        return entity_by_id_data[0]


def delete_entity_by_id(client, table_name, id_):
    """
    Deletes a record of a given ID of the specified entity

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param table_name: Table name to extract which entity to delete
    :type table_name: :class:`str`
    :param id_: ID number of the entity to delete
    :type id_: :class:`int`
    """

    entity_id_data = get_entity_by_id(client, table_name, id_, False)
    client.delete(entity_id_data)


def update_entity_by_id(client, table_name, id_, new_data):
    """
    Gets a record of a given ID of the specified entity

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param table_name: Table name to extract which entity to use
    :type table_name: :class:`str`
    :param id_: ID number of the entity to retrieve
    :type id_: :class:`int`
    :param new_data: JSON from request body providing new data to update the record with
        the specified ID
    :return: The updated record of the specified ID from the given entity
    """

    entity_id_data = get_entity_by_id(client, table_name, id_, False)
    # There will only ever be one record associated with a single ID - if a record with
    # the specified ID cannot be found, it'll be picked up by the MissingRecordError in
    # get_entity_by_id()
    update_attributes(entity_id_data, new_data)

    # The record is re-obtained from Python ICAT (rather than using entity_id_data) to
    # show to the user whether the change has actually been applied
    return get_entity_by_id(client, table_name, id_, True)


def get_entity_with_filters(client, table_name, filters):
    selected_entity_name = get_python_icat_entity_name(client, table_name)
    query = construct_icat_query(client, selected_entity_name)
    filter_handler = FilterOrderHandler()
    filter_handler.add_filters(filters)
    filter_handler.apply_filters(query)

    data = execute_icat_query(client, query, True)

    if not data:
        raise MissingRecordError("No results found")
    else:
        return data
