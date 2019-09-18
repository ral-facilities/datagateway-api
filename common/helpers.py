import json
import logging
from functools import wraps

from flask import request
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError

from common.database_helpers import QueryFilterFactory
from common.exceptions import MissingRecordError, BadFilterError, AuthenticationError, BadRequestError, \
    MissingCredentialsError, MultipleIncludeError
from common.models.db_models import SESSION
from common.session_manager import session_manager

log = logging.getLogger()


def requires_session_id(method):
    """
    Decorator for endpoint resources that makes sure a valid session_id is provided in requests to that endpoint
    :param method: The method for the endpoint
    :returns a 403, "Forbidden" if a valid session_id is not provided with the request
    """
    log.info("")

    @wraps(method)
    def wrapper_requires_session(*args, **kwargs):
        log.info(" Authenticating consumer")
        try:
            session = session_manager.get_icat_db_session()
            query = session.query(SESSION).filter(
                SESSION.ID == get_session_id_from_auth_header()).first()
            if query is not None:
                log.info(" Closing DB session")
                session.close()
                session.close()
                log.info(" Consumer authenticated")
                return method(*args, **kwargs)
            else:
                log.info(" Could not authenticate consumer, closing DB session")
                session.close()
                return "Forbidden", 403
        except MissingCredentialsError:
            return "Unauthorized", 401
        except AuthenticationError:
            return "Forbidden", 403


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
        except MissingRecordError as e:
            log.exception(e)
            return "No such record in table", 404
        except MultipleIncludeError as e:
            log.exception(e)
            return "Bad request, only one include filter may be given per request", 400
        except BadFilterError as e:
            log.exception(e)
            return "Invalid filter requested", 400
        except ValueError as e:
            log.exception(e)
            return "Bad request", 400
        except TypeError as e:
            log.exception(e)
            return "Bad request", 400
        except IntegrityError as e:
            log.exception(e)
            return "Bad request", 400
        except BadRequestError as e:
            log.exception(e)
            return "Bad request", 400
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
    auth_header = args["Authorization"].split(" ") if args["Authorization"] is not None else ""
    if auth_header == "":
        raise MissingCredentialsError(f"No credentials provided in auth header")
    if len(auth_header) != 2 or auth_header[0] != "Bearer":
        raise AuthenticationError(f" Could not authenticate consumer with auth header {auth_header}")
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
    return True


def get_filters_from_query_string():
    """
    Gets a list of filters from the query_strings arg,value pairs, and returns a list of QueryFilter Objects
    :return: The list of filters
    """
    log.info(" Getting filters from query string")
    filters = []
    for arg in request.args:
        for value in request.args.getlist(arg):
            filters.append(QueryFilterFactory.get_query_filter({arg: json.loads(value)}))
    return filters
