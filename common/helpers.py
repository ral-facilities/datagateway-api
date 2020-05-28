import json
import logging
from functools import wraps

from flask import request
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError

from common.database_helpers import QueryFilterFactory
from common.exceptions import ApiError, AuthenticationError, BadFilterError, BadRequestError, MissingCredentialsError, MissingRecordError, MultipleIncludeError
from common.models.db_models import SESSION
from common.session_manager import session_manager

log = logging.getLogger()


def requires_session_id(method):
    """
    Decorator for database backend methods that makes sure a valid session_id is provided
    It expects that session_id is the second argument supplied to the function
    :param method: The method for the backend operation
    :raises AuthenticationError, if a valid session_id is not provided with the request
    """

    @wraps(method)
    def wrapper_requires_session(*args, **kwargs):
        log.info(" Authenticating consumer")
        session = session_manager.get_icat_db_session()
        query = session.query(SESSION).filter(
            SESSION.ID == args[1]).first()
        if query is not None:
            log.info(" Closing DB session")
            session.close()
            session.close()
            log.info(" Consumer authenticated")
            return method(*args, **kwargs)
        else:
            log.info(" Could not authenticate consumer, closing DB session")
            session.close()
            raise AuthenticationError("Forbidden")

    return wrapper_requires_session


def queries_records(method):
    """
    Decorator for endpoint resources that search for a record in a table
    :param method: The method for the endpoint
    :return: Will return a 404, "No such record" if a MissingRecordError is caught
    """

    @wraps(method)
    def wrapper_gets_records(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except ApiError as e:
            log.exception(e)
            raise e
        except ValueError as e:
            log.exception(e)
            raise BadRequestError()
        except TypeError as e:
            log.exception(e)
            raise BadRequestError()
        except IntegrityError as e:
            log.exception(e)
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
    auth_header = args["Authorization"].split(
        " ") if args["Authorization"] is not None else ""
    if auth_header == "":
        raise MissingCredentialsError(
            f"No credentials provided in auth header")
    if len(auth_header) != 2 or auth_header[0] != "Bearer":
        raise AuthenticationError(
            f" Could not authenticate consumer with auth header {auth_header}")
    return auth_header[1]


def is_valid_json(string):
    """
    Determines if a string is valid JSON
    :param string: The string to be tested
    :return: boolean representing if the string is valid JSON
    """
    try:
        json_object = json.loads(string)
    except ValueError:
        return False
    except TypeError:
        return False
    return True


def get_filters_from_query_string():
    """
    Gets a list of filters from the query_strings arg,value pairs, and returns a list of QueryFilter Objects
    :return: The list of filters
    """
    log.info(" Getting filters from query string")
    try:
        filters = []
        for arg in request.args:
            for value in request.args.getlist(arg):
                filters.append(QueryFilterFactory.get_query_filter(
                    {arg: json.loads(value)}))
        return filters
    except:
        raise BadFilterError()
