from datagateway_api.common.date_handler import DateHandler
from datetime import datetime
from functools import wraps
import json
import logging

from flask import request
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError

from datagateway_api.common.database import models
from datagateway_api.common.exceptions import (
    ApiError,
    AuthenticationError,
    BadRequestError,
    FilterError,
    MissingCredentialsError,
)
from datagateway_api.common.query_filter_factory import QueryFilterFactory
from datagateway_api.src.resources.entities.entity_endpoint_dict import endpoints

log = logging.getLogger()


def queries_records(method):
    """
    Decorator for endpoint resources that search for a record in a table
    :param method: The method for the endpoint
    :return: Will return a 404, "No such record" if a MissingRecordError is caught
    :return: Will return a 400, "Error message" if other expected errors are caught
    """

    @wraps(method)
    def wrapper_gets_records(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except ApiError as e:
            log.exception(msg=e.args)
            raise e
        except ValueError as e:
            log.exception(msg=e.args)
            raise BadRequestError()
        except TypeError as e:
            log.exception(e.args)
            raise BadRequestError()
        except IntegrityError as e:
            log.exception(e.args)
            raise BadRequestError()

    return wrapper_gets_records


def get_session_id_from_auth_header():
    """
    Gets the sessionID from the Authorization header of a request
    :return: String: SessionID
    """
    log.info(" Getting session Id from auth header")
    parser = reqparse.RequestParser()
    parser.add_argument("Authorization", location="headers")
    args = parser.parse_args()
    auth_header = (
        args["Authorization"].split(" ") if args["Authorization"] is not None else ""
    )
    if auth_header == "":
        raise MissingCredentialsError("No credentials provided in auth header")
    if len(auth_header) != 2 or auth_header[0] != "Bearer":
        raise AuthenticationError(
            f" Could not authenticate consumer with auth header {auth_header}",
        )
    return auth_header[1]


def is_valid_json(string):
    """
    Determines if a string is valid JSON
    :param string: The string to be tested
    :return: boolean representing if the string is valid JSON
    """
    try:
        json.loads(string)
    except ValueError:
        return False
    except TypeError:
        return False
    return True


def get_filters_from_query_string():
    """
    Gets a list of filters from the query_strings arg,value pairs, and returns a list of
    QueryFilter Objects

    :return: The list of filters
    """
    log.info(" Getting filters from query string")
    try:
        filters = []
        for arg in request.args:
            for value in request.args.getlist(arg):
                filters.append(
                    QueryFilterFactory.get_query_filter({arg: json.loads(value)}),
                )
        return filters
    except Exception as e:
        raise FilterError(e)


def get_entity_object_from_name(entity_name):
    """
    From an entity name, this function gets a Python version of that entity for the
    database backend

    :param entity_name: Name of the entity to fetch a version from this model
    :type entity_name: :class:`str`
    :return: Object of the entity requested (e.g.
        :class:`datagateway_api.common.database.models.INVESTIGATIONINSTRUMENT`)
    :raises: KeyError: If an entity model cannot be found as a class in this model
    """
    try:
        # If a plural is given, fetch the singular field name
        if entity_name[-1] == "s":
            entity_name = entity_name[0].upper() + entity_name[1:]
            entity_name = endpoints[entity_name]

        return getattr(models, entity_name.upper())
    except KeyError:
        raise ApiError(
            f"Entity class cannot be found, missing class for {entity_name}",
        )


def map_distinct_attributes_to_results(distinct_attributes, query_result):
    """
    Maps the attribute names from a distinct filter onto the results given by the result
    of a query

    When selecting multiple (but not all) attributes in a database query, the results
    are returned in a list and not mapped to an entity object. This means the 'normal'
    functions used to process data ready for output (`entity_to_dict()` for the ICAT
    backend) cannot be used, as the structure of the query result is different.

    :param distinct_attributes: List of distinct attributes from the distinct
        filter of the incoming request
    :type distinct_attributes: :class:`list`
    :param query_result: Results fetched from a database query (backend independent due
        to the data structure of this parameter)
    :type query_result: :class:`tuple` or :class:`list` when a single attribute is
        given from ICAT backend, or :class:`sqlalchemy.engine.row.Row` when used on the
        DB backend
    :return: Dictionary of attribute names paired with the results, ready to be
        returned to the user
    """
    result_dict = {}
    for attr_name, data in zip(distinct_attributes, query_result):
        # Splitting attribute names in case it's from a related entity
        split_attr_name = attr_name.split(".")

        if isinstance(data, datetime):
            data = DateHandler.datetime_object_to_str(data)

        # Attribute name is from the 'origin' entity (i.e. not a related entity)
        if len(split_attr_name) == 1:
            result_dict[attr_name] = data
        # Attribute name is a related entity, dictionary needs to be nested
        else:
            result_dict.update(map_nested_attrs({}, split_attr_name, data))

    return result_dict


def map_nested_attrs(nested_dict, split_attr_name, query_data):
    """
    A function that can be called recursively to map attributes from related
    entities to the associated data

    :param nested_dict: Dictionary to insert data into
    :type nested_dict: :class:`dict`
    :param split_attr_name: List of parts to an attribute name, that have been split
        by "."
    :type split_attr_name: :class:`list`
    :param query_data: Data to be added to the dictionary
    :type query_data: :class:`str` or :class:`str`
    :return: Dictionary to be added to the result dictionary
    """
    # Popping LHS of related attribute name to see if it's an attribute name or part
    # of a path to a related entity
    attr_name_pop = split_attr_name.pop(0)

    # Related attribute name, ready to insert data into dictionary
    if len(split_attr_name) == 0:
        # at role, so put data in
        nested_dict[attr_name_pop] = query_data
    # Part of the path for related entity, need to recurse to get to attribute name
    else:
        nested_dict[attr_name_pop] = {}
        map_nested_attrs(nested_dict[attr_name_pop], split_attr_name, query_data)

    return nested_dict
