from datetime import datetime, timedelta
from functools import wraps
import logging

from cachetools import cached
from dateutil.tz import tzlocal
from icat.exception import (
    ICATInternalError,
    ICATNoObjectError,
    ICATObjectExistsError,
    ICATParameterError,
    ICATSessionError,
    ICATValidationError,
)

from datagateway_api.src.common.config import Config
from datagateway_api.src.common.date_handler import DateHandler
from datagateway_api.src.common.exceptions import (
    AuthenticationError,
    BadRequestError,
    MissingRecordError,
    PythonICATError,
)
from datagateway_api.src.common.filter_order_handler import FilterOrderHandler
from datagateway_api.src.datagateway_api.icat.filters import (
    PythonICATLimitFilter,
    PythonICATWhereFilter,
)
from datagateway_api.src.datagateway_api.icat.icat_client_pool import ICATClient
from datagateway_api.src.datagateway_api.icat.lru_cache import ExtendedLRUCache
from datagateway_api.src.datagateway_api.icat.query import ICATQuery
from datagateway_api.src.datagateway_api.icat.reader_query_handler import (
    ReaderQueryHandler,
)

log = logging.getLogger()


def requires_session_id(method):
    """
    Decorator for Python ICAT backend methods that looks out for session errors when
    using the API. The API call runs and an ICATSessionError may be raised due to an
    expired session, invalid session ID etc.

    The session ID from the request is set here, so there is no requirement for a user
    to use the login endpoint, they can go straight into using the API so long as they
    have a valid session ID (be it created from this API, or from an alternative such as
    scigateway-auth).

    This assumes the session ID is the second argument of the function where this
    decorator is applied, which is reasonable to assume considering the current method
    signatures of all the endpoints.

    :param method: The method for the backend operation
    :raises AuthenticationError: If a valid session_id is not provided with the request
    """

    @wraps(method)
    def wrapper_requires_session(*args, **kwargs):
        try:
            client_pool = kwargs.get("client_pool")

            client = get_cached_client(args[1], client_pool)
            client.sessionId = args[1]
            # Client object put into kwargs so it can be accessed by backend functions
            kwargs["client"] = client

            # Find out if session has expired
            session_time = client.getRemainingMinutes()
            log.info("Session time: %d", session_time)
            if session_time < 0:
                raise AuthenticationError("Forbidden")
            else:
                return method(*args, **kwargs)
        except ICATSessionError as e:
            raise AuthenticationError(e)

    return wrapper_requires_session


@cached(cache=ExtendedLRUCache())
def get_cached_client(session_id, client_pool):
    """
    Get a client from cache using session ID as the cache parameter (client_pool will
    always be given the same object, so won't impact on argument hashing)

    An available client is fetched from the object pool, given a session ID, and kept
    around in this cache until it becomes 'least recently used'. At this point, the
    session ID is flushed and the client is returned to the pool. More details about
    client handling can be found in the README

    :param session_id: The user's session ID
    :type session_id: :class:`str`
    :param client_pool: Client object pool used to fetch an unused client
    :type client_pool: :class:`ObjectPool`
    """

    # Get a client from the pool
    client, stats = client_pool._get_resource()

    # `session_id` of None suggests this function is being called from an endpoint that
    # doesn't use the `requires_session_id` decorator (e.g. POST /sessions)
    log.info("Caching, session ID: %s", session_id)
    if session_id:
        client.sessionId = session_id

    return client


def get_session_details_helper(client):
    """
    Retrieve details regarding the current session within `client`

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :return: Details of the user's session, ready to be converted into a JSON response
        body
    """
    session_time_remaining = client.getRemainingMinutes()
    session_expiry_time = (
        datetime.now(tzlocal()) + timedelta(minutes=session_time_remaining)
    ).replace(microsecond=0)
    username = client.getUserName()

    return {
        "id": client.sessionId,
        "expireDateTime": DateHandler.datetime_object_to_str(session_expiry_time),
        "username": username,
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
    log.debug("Updating entity attributes: %s", list(new_entity.keys()))
    for key in new_entity:
        try:
            original_data_attribute = getattr(old_entity, key)
            if isinstance(original_data_attribute, datetime):
                new_entity[key] = DateHandler.str_to_datetime_object(new_entity[key])
        except AttributeError:
            raise BadRequestError(
                f"Bad request made, cannot find attribute '{key}' within the"
                f" {old_entity.BeanName} entity",
            )

        try:
            setattr(old_entity, key, new_entity[key])
        except AttributeError:
            raise BadRequestError(
                f"Bad request made, cannot modify attribute '{key}' within the"
                f" {old_entity.BeanName} entity",
            )

    return old_entity


def push_data_updates_to_icat(entity):
    try:
        entity.update()
    except ICATInternalError as e:
        raise PythonICATError(e)
    except ICATValidationError as e:
        raise BadRequestError(e)


def get_entity_by_id(
    client,
    entity_type,
    id_,
    return_json_formattable_data,
    return_related_entities=False,
):
    """
    Gets a record of a given ID from the specified entity

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param entity_type: The type of entity requested to manipulate data with
    :type entity_type: :class:`str`
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
    log.info("Getting %s of the ID %s", entity_type, id_)
    log.debug("Return related entities set to: %s", return_related_entities)

    # Set query condition for the selected ID
    id_condition = PythonICATWhereFilter.create_condition("id", "=", id_)

    includes_value = "1" if return_related_entities else None
    id_query = ICATQuery(
        client, entity_type, conditions=id_condition, includes=includes_value,
    )
    entity_by_id_data = id_query.execute_query(client, return_json_formattable_data)

    if not entity_by_id_data:
        # Cannot find any data matching the given ID
        raise MissingRecordError("No result found")
    else:
        return entity_by_id_data[0]


def delete_entity_by_id(client, entity_type, id_):
    """
    Deletes a record of a given ID of the specified entity

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param entity_type: The type of entity requested to manipulate data with
    :type entity_type: :class:`str`
    :param id_: ID number of the entity to delete
    :type id_: :class:`int`
    """
    log.info("Deleting %s of ID %s", entity_type, id_)
    entity_id_data = get_entity_by_id(client, entity_type, id_, False)
    client.delete(entity_id_data)


def update_entity_by_id(client, entity_type, id_, new_data):
    """
    Gets a record of a given ID of the specified entity

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param entity_type: The type of entity requested to manipulate data with
    :type entity_type: :class:`str`
    :param id_: ID number of the entity to retrieve
    :type id_: :class:`int`
    :param new_data: JSON from request body providing new data to update the record with
        the specified ID
    :return: The updated record of the specified ID from the given entity
    """
    log.info("Updating %s of ID %s", entity_type, id_)

    entity_id_data = get_entity_by_id(
        client, entity_type, id_, False, return_related_entities=True,
    )
    # There will only ever be one record associated with a single ID - if a record with
    # the specified ID cannot be found, it'll be picked up by the MissingRecordError in
    # get_entity_by_id()
    updated_icat_entity = update_attributes(entity_id_data, new_data)
    push_data_updates_to_icat(updated_icat_entity)

    # The record is re-obtained from Python ICAT (rather than using entity_id_data) to
    # show to the user whether the change has actually been applied
    return get_entity_by_id(client, entity_type, id_, True)


def get_entity_with_filters(client, entity_type, filters, client_pool=None):
    """
    Gets all the records of a given entity, based on the filters provided in the request

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param entity_type: The type of entity requested to manipulate data with
    :type entity_type: :class:`str`
    :param filters: The list of filters to be applied to the request
    :type filters: List of specific implementations :class:`QueryFilter`
    :return: The list of records of the given entity, using the filters to restrict the
        result of the query
    """
    log.info("Getting entity using request's filters")
    return get_data_with_filters(client, entity_type, filters, client_pool=client_pool)


def get_count_with_filters(client, entity_type, filters, client_pool=None):
    """
    Get the number of results of a given entity, based on the filters provided in the
    request. This acts very much like `get_entity_with_filters()` but returns the number
    of results, as opposed to a JSON object of data.

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param entity_type: The type of entity requested to manipulate data with
    :type entity_type: :class:`str`
    :param filters: The list of filters to be applied to the request
    :type filters: List of specific implementations :class:`QueryFilter`
    :return: The number of records of the given entity (of type integer), using the
        filters to restrict the result of the query
    """
    log.info(
        "Getting the number of results of %s, also using the request's filters",
        entity_type,
    )

    data = get_data_with_filters(
        client, entity_type, filters, aggregate="COUNT", client_pool=client_pool,
    )
    # Only ever 1 element in a count query result
    return data[0]


def get_data_with_filters(
    client, entity_type, filters, aggregate=None, client_pool=None,
):
    reader_query = ReaderQueryHandler(entity_type, filters)
    if reader_query.is_query_eligible_for_reader_performance():
        log.info("Query is eligible to be passed as reader acount")
        if reader_query.is_user_authorised_to_see_entity_id(client):
            reader_client = ReaderQueryHandler.reader_client
            log.info("Query to be executed as reader account")
            try:
                results = execute_entity_query(
                    reader_client, entity_type, filters, aggregate=aggregate,
                )
            except ICATSessionError:
                # re-login as reader and try the query again
                reader_client = reader_query.create_reader_client()
                results = execute_entity_query(
                    reader_client, entity_type, filters, aggregate=aggregate,
                )
            return results
        else:
            raise AuthenticationError(
                "Not authorised to access the"
                f" {ReaderQueryHandler.entity_filter_check[entity_type]}"
                " you have filtered on",
            )
    else:
        log.info("Query to be executed as user from request: %s", client.getUserName())
        return execute_entity_query(client, entity_type, filters, aggregate=aggregate)


def execute_entity_query(client, entity_type, filters, aggregate=None):
    query = ICATQuery(client, entity_type, aggregate=aggregate)

    filter_handler = FilterOrderHandler()
    filter_handler.manage_icat_filters(filters, query.query)

    log.debug(
        "Query on entity '%s' (aggregate: %s), executed as user: %s",
        entity_type,
        aggregate,
        client.getUserName(),
    )
    return query.execute_query(client, True)


def get_first_result_with_filters(client, entity_type, filters):
    """
    Using filters in the request, get results of the given entity, but only show the
    first one to the user

    Since only one result will be outputted, inserting a `PythonICATLimitFilter` in the
    query will make Python ICAT's data fetching more snappy and prevent a 500 being
    caused by trying to fetch over the number of records limited by ICAT (currently
    10000).

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param entity_type: The type of entity requested to manipulate data with
    :type entity_type: :class:`str`
    :param filters: The list of filters to be applied to the request
    :type filters: List of specific implementations :class:`QueryFilter`
    :return: The first record of the given entity, using the filters to restrict the
        result of the query
    """
    log.info(
        "Getting only first result of %s, making use of filters in request",
        entity_type,
    )

    limit_filter = PythonICATLimitFilter(1)
    filters.append(limit_filter)

    entity_data = get_entity_with_filters(client, entity_type, filters)

    if not entity_data:
        raise MissingRecordError("No results found")
    else:
        return entity_data[0]


def update_entities(client, entity_type, data_to_update):
    """
    Update one or more results for the given entity using the JSON provided in
    `data_to_update`

    If an exception occurs while sending data to icatdb, an attempt will be made to
    restore a backup of the data made before making the update.

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param entity_type: The type of entity requested to manipulate data with
    :type entity_type: :class:`str`
    :param data_to_update: The data that to be updated in ICAT
    :type data_to_update: :class:`list` or :class:`dict`
    :return: The updated record(s) of the given entity
    """
    log.info("Updating certain results in %s", entity_type)

    updated_data = []

    if not isinstance(data_to_update, list):
        data_to_update = [data_to_update]

    icat_data_backup = []
    updated_icat_data = []

    for entity_request in data_to_update:
        try:
            entity_data = get_entity_by_id(
                client,
                entity_type,
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
                " 'id') of the entity you wish to update",
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
            get_entity_by_id(client, entity_type, updated_icat_entity.id, True),
        )

    return updated_data


def create_entities(client, entity_type, data):
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
    :param entity_type: The type of entity requested to manipulate data with
    :type entity_type: :class:`str`
    :param data: The data that needs to be created in ICAT
    :type data_to_update: :class:`list` or :class:`dict`
    :return: The created record(s) of the given entity
    """
    log.info("Creating ICAT data for %s", entity_type)

    created_data = []
    created_icat_data = []

    if not isinstance(data, list):
        data = [data]

    for result in data:
        new_entity = client.new(entity_type.lower())

        for attribute_name, value in result.items():
            log.debug("Preparing data for %s", attribute_name)
            try:
                entity_info = new_entity.getAttrInfo(client, attribute_name)
                if entity_info.relType.lower() == "attribute":
                    # Short circuiting ensures is_str_date() will only be executed if
                    # value is a string
                    if isinstance(value, str) and DateHandler.is_str_a_date(value):
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
        except ICATInternalError as e:
            for entity_json in created_data:
                # Delete any data that has been pushed to ICAT before the exception
                delete_entity_by_id(client, entity_type, entity_json["id"])

            raise PythonICATError(e)
        except (ICATObjectExistsError, ICATParameterError, ICATValidationError) as e:
            for entity_json in created_data:
                delete_entity_by_id(client, entity_type, entity_json["id"])

            raise BadRequestError(e)

        created_data.append(get_entity_by_id(client, entity_type, entity.id, True))

    return created_data
