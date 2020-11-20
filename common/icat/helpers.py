from functools import wraps
import logging
from datetime import datetime, timedelta


from icat.entities import getTypeMap
from icat.exception import (
    ICATSessionError,
    ICATValidationError,
    ICATInternalError,
    ICATObjectExistsError,
    ICATNoObjectError,
    ICATParameterError,
)
from icat.sslcontext import create_ssl_context
from common.exceptions import (
    AuthenticationError,
    BadRequestError,
    MissingRecordError,
    PythonICATError,
)
from common.filter_order_handler import FilterOrderHandler
from common.date_handler import DateHandler
from common.constants import Constants
from common.icat.filters import PythonICATLimitFilter, PythonICATWhereFilter
from common.icat.query import ICATQuery

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


def get_python_icat_entity_name(client, database_table_name, camel_case_output=False):
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
    :param camel_case_output: Flag to signify if the entity name should be returned in
        camel case format. Enabling this flag gets the entity names from a different
        place in Python ICAT.
    :type camel_case_output: :class:`bool`
    :return: Entity name (of type string) in the correct casing ready to be passed into
        Python ICAT
    :raises BadRequestError: If the entity cannot be found
    """

    if camel_case_output:
        entity_names = getTypeMap(client).keys()
    else:
        entity_names = client.getEntityNames()

    lowercase_table_name = database_table_name.lower()
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


def update_attributes(old_entity, new_entity):
    """
    Updates the attribute(s) of a given object which is a record of an entity from
    Python ICAT

    :param old_entity: An existing entity record from Python ICAT
    :type object: :class:`icat.entities.ENTITY` (implementation of
        :class:`icat.entity.Entity`)
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
                new_entity[key] = DateHandler.str_to_datetime_object(new_entity[key])
        except AttributeError:
            raise BadRequestError(
                f"Bad request made, cannot find attribute '{key}' within the"
                f" {old_entity.BeanName} entity"
            )

        try:
            setattr(old_entity, key, new_entity[key])
        except AttributeError:
            raise BadRequestError(
                f"Bad request made, cannot modify attribute '{key}' within the"
                f" {old_entity.BeanName} entity"
            )

    return old_entity


def push_data_updates_to_icat(entity):
    try:
        entity.update()
    except (ICATValidationError, ICATInternalError) as e:
        raise PythonICATError(e)


def get_entity_by_id(
    client, table_name, id_, return_json_formattable_data, return_related_entities=False
):
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
    :param return_related_entities: Flag to determine whether related entities should
        automatically be returned or not. Returning related entities used as a bug fix
        for an `IcatException` where ICAT attempts to set a field to null because said
        field hasn't been included in the updated data
    :type return_related_entities: :class:`bool`
    :return: The record of the specified ID from the given entity
    :raises: MissingRecordError: If Python ICAT cannot find a record of the specified ID
    """

    selected_entity_name = get_python_icat_entity_name(client, table_name)
    # Set query condition for the selected ID
    id_condition = PythonICATWhereFilter.create_condition("id", "=", id_)

    includes_value = "1" if return_related_entities == True else None
    id_query = ICATQuery(
        client, selected_entity_name, conditions=id_condition, includes=includes_value
    )
    entity_by_id_data = id_query.execute_query(client, return_json_formattable_data)

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

    entity_id_data = get_entity_by_id(
        client, table_name, id_, False, return_related_entities=True
    )
    # There will only ever be one record associated with a single ID - if a record with
    # the specified ID cannot be found, it'll be picked up by the MissingRecordError in
    # get_entity_by_id()
    updated_icat_entity = update_attributes(entity_id_data, new_data)
    push_data_updates_to_icat(updated_icat_entity)

    # The record is re-obtained from Python ICAT (rather than using entity_id_data) to
    # show to the user whether the change has actually been applied
    return get_entity_by_id(client, table_name, id_, True)


def get_entity_with_filters(client, table_name, filters):
    """
    Gets all the records of a given entity, based on the filters provided in the request

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param table_name: Table name to extract which entity to use
    :type table_name: :class:`str`
    :param filters: The list of filters to be applied to the request
    :type filters: List of specific implementations :class:`QueryFilter`
    :return: The list of records of the given entity, using the filters to restrict the
        result of the query
    """
    log.info("Getting entity using request's filters")

    selected_entity_name = get_python_icat_entity_name(client, table_name)
    query = ICATQuery(client, selected_entity_name)

    filter_handler = FilterOrderHandler()
    filter_handler.manage_icat_filters(filters, query.query)

    data = query.execute_query(client, True)

    if not data:
        raise MissingRecordError("No results found")
    else:
        return data


def get_count_with_filters(client, table_name, filters):
    """
    Get the number of results of a given entity, based on the filters provided in the
    request. This acts very much like `get_entity_with_filters()` but returns the number
    of results, as opposed to a JSON object of data.

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param table_name: Table name to extract which entity to use
    :type table_name: :class:`str`
    :param filters: The list of filters to be applied to the request
    :type filters: List of specific implementations :class:`QueryFilter`
    :return: The number of records of the given entity (of type integer), using the
        filters to restrict the result of the query
    """
    log.info(
        "Getting the number of results of %s, also using the request's filters",
        table_name,
    )

    selected_entity_name = get_python_icat_entity_name(client, table_name)
    query = ICATQuery(client, selected_entity_name, aggregate="COUNT")

    filter_handler = FilterOrderHandler()
    filter_handler.manage_icat_filters(filters, query.query)

    data = query.execute_query(client, True)

    if not data:
        raise MissingRecordError("No results found")
    else:
        # Only ever 1 element in a count query result
        return data[0]


def get_first_result_with_filters(client, table_name, filters):
    """
    Using filters in the request, get results of the given entity, but only show the
    first one to the user

    Since only one result will be outputted, inserting a `PythonICATLimitFilter` in the
    query will make Python ICAT's data fetching more snappy and prevent a 500 being
    caused by trying to fetch over the number of records limited by ICAT (currently
    10000).

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param table_name: Table name to extract which entity to use
    :type table_name: :class:`str`
    :param filters: The list of filters to be applied to the request
    :type filters: List of specific implementations :class:`QueryFilter`
    :return: The first record of the given entity, using the filters to restrict the
        result of the query
    """
    log.info(
        "Getting only first result of %s, making use of filters in request", table_name
    )

    limit_filter = PythonICATLimitFilter(1)
    filters.append(limit_filter)

    entity_data = get_entity_with_filters(client, table_name, filters)

    if not entity_data:
        raise MissingRecordError("No results found")
    else:
        return entity_data[0]


def update_entities(client, table_name, data_to_update):
    """
    Update one or more results for the given entity using the JSON provided in 
    `data_to_update`

    If an exception occurs while sending data to icatdb, an attempt will be made to
    restore a backup of the data made before making the update.

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param table_name: Table name to extract which entity to use
    :type table_name: :class:`str`
    :param data_to_update: The data that to be updated in ICAT
    :type data_to_update: :class:`list` or :class:`dict`
    :return: The updated record(s) of the given entity
    """
    log.info("Updating certain results in %s", table_name)

    updated_data = []

    if not isinstance(data_to_update, list):
        data_to_update = [data_to_update]

    icat_data_backup = []
    updated_icat_data = []

    for entity_request in data_to_update:
        try:
            entity_data = get_entity_by_id(
                client,
                table_name,
                entity_request["id"],
                False,
                return_related_entities=True,
            )
            icat_data_backup.append(entity_data.copy())

            updated_entity_data = update_attributes(entity_data, entity_request)
            updated_icat_data.append(updated_entity_data)
        except KeyError:
            raise BadRequestError(
                "The new data in the request body must contain the ID (using the key:"
                " 'id') of the entity you wish to update"
            )

    # This separates the local data updates from pushing these updates to icatdb
    for updated_icat_entity in updated_icat_data:
        try:
            updated_icat_entity.update()
        except (ICATValidationError, ICATInternalError) as e:
            # Use `icat_data_backup` to restore data trying to updated to the state
            # before this request
            for icat_entity_backup in icat_data_backup:
                try:
                    icat_entity_backup.update()
                except (ICATValidationError, ICATInternalError) as e:
                    # If an error occurs while trying to restore backup data, just throw
                    # a 500 immediately
                    raise PythonICATError(e)

            raise PythonICATError(e)

        updated_data.append(
            get_entity_by_id(client, table_name, updated_icat_entity.id, True)
        )

    return updated_data


def create_entities(client, table_name, data):
    """
    Add one or more results for the given entity using the JSON provided in `data`

    `created_icat_data` is data of `icat.entity.Entity` type that is collated to be
    pushed to ICAT at the end of the function - this avoids confusion over which data
    has/hasn't been created if the request returns an error. When pushing the data to
    ICAT, there is still risk an exception might be caught, so any entities already
    pushed to ICAT will be deleted. Python ICAT doesn't support a database rollback (or
    the concept of transactions) so this is a good alternative.

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param table_name: Table name to extract which entity to use
    :type table_name: :class:`str`
    :param data: The data that needs to be created in ICAT
    :type data_to_update: :class:`list` or :class:`dict`
    :return: The created record(s) of the given entity
    """
    log.info("Creating ICAT data for %s", table_name)

    created_data = []
    created_icat_data = []

    if not isinstance(data, list):
        data = [data]

    for result in data:
        new_entity = client.new(
            get_python_icat_entity_name(client, table_name, camel_case_output=True)
        )

        for attribute_name, value in result.items():
            try:
                entity_info = new_entity.getAttrInfo(client, attribute_name)
                if entity_info.relType.lower() == "attribute":
                    if isinstance(value, str):
                        if DateHandler.is_str_a_date(value):
                            value = DateHandler.str_to_datetime_object(value)

                    setattr(new_entity, attribute_name, value)
                else:
                    # This means the attribute has a relationship with another object
                    try:
                        related_object = client.get(entity_info.type, value)
                    except ICATNoObjectError as e:
                        raise BadRequestError(e)
                    if entity_info.relType.lower() == "many":
                        related_object = [related_object]
                    setattr(new_entity, attribute_name, related_object)

            except ValueError as e:
                raise BadRequestError(e)

        created_icat_data.append(new_entity)

    for entity in created_icat_data:
        try:
            entity.create()
        except (ICATValidationError, ICATInternalError) as e:
            for entity_json in created_data:
                # Delete any data that has been pushed to ICAT before the exception
                delete_entity_by_id(client, table_name, entity_json["id"])

            raise PythonICATError(e)
        except (ICATObjectExistsError, ICATParameterError) as e:
            for entity_json in created_data:
                delete_entity_by_id(client, table_name, entity_json["id"])

            raise BadRequestError(e)

        created_data.append(get_entity_by_id(client, table_name, entity.id, True))

    return created_data
