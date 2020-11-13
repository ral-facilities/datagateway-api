from datetime import datetime, timedelta
from functools import wraps
import logging


import icat.client
from icat.entities import getTypeMap
from icat.exception import (
    ICATInternalError,
    ICATNoObjectError,
    ICATObjectExistsError,
    ICATParameterError,
    ICATSessionError,
    ICATValidationError,
)

from datagateway_api.common.config import config
from datagateway_api.common.date_handler import DateHandler
from datagateway_api.common.exceptions import (
    AuthenticationError,
    BadRequestError,
    MissingRecordError,
    PythonICATError,
)
from datagateway_api.common.filter_order_handler import FilterOrderHandler
from datagateway_api.common.icat.filters import (
    PythonICATLimitFilter,
    PythonICATWhereFilter,
)
from datagateway_api.common.icat.query import ICATQuery


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
            client = create_client()
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
        except ICATSessionError:
            raise AuthenticationError("Forbidden")

    return wrapper_requires_session


def create_client():
    client = icat.client.Client(
        config.get_icat_url(), checkCert=config.get_icat_check_cert(),
    )
    return client


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
    log.info("Logging out of the Python ICAT client")
    client.logout()


def refresh_client_session(client):
    """
    Refresh the session of the currently authenticated user within `client`

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    """
    client.refresh()


def get_icat_entity_name_as_camel_case(client, entity_name):
    """
    From the entity name, this function returns a camelCase version of its input

    Due to the case sensitivity of Python ICAT, a camelCase version of the entity name
    is required for creating ICAT entities in ICAT (e.g. `client.new("parameterType")`).

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param entity_name: Entity name to fetch a camelCase version of
    :type entity_name: :class:`str`
    :return: Entity name (of type string) in the correct casing ready to be passed into
        Python ICAT
    :raises BadRequestError: If the entity cannot be found
    """

    entity_names = getTypeMap(client).keys()
    lowercase_entity_name = entity_name.lower()
    python_icat_entity_name = None

    for entity_name in entity_names:
        lowercase_name = entity_name.lower()
        if lowercase_name == lowercase_entity_name:
            python_icat_entity_name = entity_name

    # Raise a 400 if a valid entity cannot be found
    if python_icat_entity_name is None:
        raise BadRequestError(
            f"Bad request made, cannot find {entity_name} entity within Python ICAT",
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
                f" {old_entity.BeanName} entity",
            )

        try:
            setattr(old_entity, key, new_entity[key])
        except AttributeError:
            raise BadRequestError(
                f"Bad request made, cannot modify attribute '{key}' within the"
                f" {old_entity.BeanName} entity",
            )

    try:
        old_entity.update()
    except (ICATValidationError, ICATInternalError) as e:
        raise PythonICATError(e)


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
    update_attributes(entity_id_data, new_data)

    # The record is re-obtained from Python ICAT (rather than using entity_id_data) to
    # show to the user whether the change has actually been applied
    return get_entity_by_id(client, entity_type, id_, True)


def get_entity_with_filters(client, entity_type, filters):
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

    query = ICATQuery(client, entity_type)

    filter_handler = FilterOrderHandler()
    filter_handler.manage_icat_filters(filters, query.query)

    data = query.execute_query(client, True)

    if not data:
        raise MissingRecordError("No results found")
    else:
        return data


def get_count_with_filters(client, entity_type, filters):
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

    query = ICATQuery(client, entity_type, aggregate="COUNT")

    filter_handler = FilterOrderHandler()
    filter_handler.manage_icat_filters(filters, query.query)

    data = query.execute_query(client, True)

    if not data:
        raise MissingRecordError("No results found")
    else:
        # Only ever 1 element in a count query result
        return data[0]


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

    for entity in data_to_update:
        try:
            updated_result = update_entity_by_id(
                client, entity_type, entity["id"], entity,
            )
            updated_data.append(updated_result)
        except KeyError:
            raise BadRequestError(
                "The new data in the request body must contain the ID (using the key:"
                " 'id') of the entity you wish to update",
            )

    return updated_data


def create_entities(client, entity_type, data):
    """
    Add one or more results for the given entity using the JSON provided in `data`

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

    if not isinstance(data, list):
        data = [data]

    for result in data:
        new_entity = client.new(
            get_icat_entity_name_as_camel_case(
                client, entity_type, camel_case_output=True,
            ),
        )

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

        try:
            new_entity.create()
        except (ICATValidationError, ICATInternalError) as e:
            raise PythonICATError(e)
        except (ICATObjectExistsError, ICATParameterError) as e:
            raise BadRequestError(e)

        created_data.append(get_entity_by_id(client, entity_type, new_entity.id, True))

    return created_data


def get_facility_cycles_for_instrument(
    client, instrument_id, filters, count_query=False,
):
    """
    Given an Instrument ID, get the Facility Cycles where there are Instruments that
    have investigations occurring within that cycle

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param instrument_id: ID of the instrument from the request
    :type instrument_id: :class:`int`
    :param filters: The list of filters to be applied to the request
    :type filters: List of specific implementations :class:`QueryFilter`
    :param count_query: Flag to determine if the query in this function should be used
        as a count query. Used for `get_facility_cycles_for_instrument_count()`
    :type count_query: :class:`bool`
    :return: A list of Facility Cycles that match the query
    """
    log.info("Getting a list of facility cycles from the specified instrument for ISIS")

    query_aggregate = "COUNT:DISTINCT" if count_query else "DISTINCT"
    query = ICATQuery(client, "FacilityCycle", aggregate=query_aggregate)

    instrument_id_check = PythonICATWhereFilter(
        "facility.instruments.id", instrument_id, "eq",
    )
    investigation_instrument_id_check = PythonICATWhereFilter(
        "facility.investigations.investigationInstruments.instrument.id",
        instrument_id,
        "eq",
    )
    investigation_start_date_check = PythonICATWhereFilter(
        "facility.investigations.startDate", "o.startDate", "gte",
    )
    investigation_end_date_check = PythonICATWhereFilter(
        "facility.investigations.startDate", "o.endDate", "lte",
    )

    facility_cycle_filters = [
        instrument_id_check,
        investigation_instrument_id_check,
        investigation_start_date_check,
        investigation_end_date_check,
    ]
    filters.extend(facility_cycle_filters)
    filter_handler = FilterOrderHandler()
    filter_handler.manage_icat_filters(filters, query.query)

    data = query.execute_query(client, True)

    if not data:
        raise MissingRecordError("No results found")
    else:
        return data


def get_facility_cycles_for_instrument_count(client, instrument_id, filters):
    """
    Given an Instrument ID, get the number of Facility Cycles where there's Instruments
    that have investigations occurring within that cycle

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param instrument_id: ID of the instrument from the request
    :type instrument_id: :class:`int`
    :param filters: The list of filters to be applied to the request
    :type filters: List of specific implementations :class:`QueryFilter`
    :return: The number of Facility Cycles that match the query
    """
    log.info(
        "Getting the number of facility cycles from the specified instrument for ISIS",
    )
    return get_facility_cycles_for_instrument(
        client, instrument_id, filters, count_query=True,
    )[0]


def get_investigations_for_instrument_in_facility_cycle(
    client, instrument_id, facilitycycle_id, filters, count_query=False,
):
    """
    Given Instrument and Facility Cycle IDs, get investigations that use the given
    instrument in the given cycle

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param instrument_id: ID of the instrument from the request
    :type instrument_id: :class:`int`
    :param facilitycycle_id: ID of the facilityCycle from the request
    :type facilitycycle_id: :class:`int`
    :param filters: The list of filters to be applied to the request
    :type filters: List of specific implementations :class:`QueryFilter`
    :param count_query: Flag to determine if the query in this function should be used
        as a count query. Used for
        `get_investigations_for_instrument_in_facility_cycle_count()`
    :type count_query: :class:`bool`
    :return: A list of Investigations that match the query
    """
    log.info(
        "Getting a list of investigations from the specified instrument and facility"
        " cycle, for ISIS",
    )

    query_aggregate = "COUNT:DISTINCT" if count_query else "DISTINCT"
    query = ICATQuery(client, "Investigation", aggregate=query_aggregate)

    instrument_id_check = PythonICATWhereFilter(
        "facility.instruments.id", instrument_id, "eq",
    )
    investigation_instrument_id_check = PythonICATWhereFilter(
        "investigationInstruments.instrument.id", instrument_id, "eq",
    )
    facility_cycle_id_check = PythonICATWhereFilter(
        "facility.facilityCycles.id", facilitycycle_id, "eq",
    )
    facility_cycle_start_date_check = PythonICATWhereFilter(
        "facility.facilityCycles.startDate", "o.startDate", "lte",
    )
    facility_cycle_end_date_check = PythonICATWhereFilter(
        "facility.facilityCycles.endDate", "o.startDate", "gte",
    )

    required_filters = [
        instrument_id_check,
        investigation_instrument_id_check,
        facility_cycle_id_check,
        facility_cycle_start_date_check,
        facility_cycle_end_date_check,
    ]
    filters.extend(required_filters)
    filter_handler = FilterOrderHandler()
    filter_handler.manage_icat_filters(filters, query.query)

    data = query.execute_query(client, True)

    if not data:
        raise MissingRecordError("No results found")
    else:
        return data


def get_investigations_for_instrument_in_facility_cycle_count(
    client, instrument_id, facilitycycle_id, filters,
):
    """
    Given Instrument and Facility Cycle IDs, get the number of investigations that use
    the given instrument in the given cycle

    :param client: ICAT client containing an authenticated user
    :type client: :class:`icat.client.Client`
    :param instrument_id: ID of the instrument from the request
    :type instrument_id: :class:`int`
    :param facilitycycle_id: ID of the facilityCycle from the request
    :type facilitycycle_id: :class:`int`
    :param filters: The list of filters to be applied to the request
    :type filters: List of specific implementations :class:`QueryFilter`
    :return: The number of Investigations that match the query
    """
    log.info(
        "Getting the number of investigations from the specified instrument and"
        " facility cycle, for ISIS",
    )
    return get_investigations_for_instrument_in_facility_cycle(
        client, instrument_id, facilitycycle_id, filters, count_query=True,
    )[0]
