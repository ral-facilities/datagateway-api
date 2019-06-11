import json
from functools import wraps

from flask import request
from flask_restful import reqparse
from sqlalchemy.exc import IntegrityError

from common.database_helpers import get_icat_db_session
from common.exceptions import MissingRecordError, BadFilterError
from common.models.db_models import SESSION


def requires_session_id(method):
    """
    Decorator for endpoint resources that makes sure a valid session_id is provided in requests to that endpoint
    :param method: The method for the endpoint
    :returns a 403, "Forbidden" if a valid session_id is not provided with the request
    """

    @wraps(method)
    def wrapper_requires_session(*args, **kwargs):
        session = get_icat_db_session()
        query = session.query(SESSION).filter(
            SESSION.ID == get_session_id_from_auth_header()).first()
        if query is not None:
            return method(*args, **kwargs)
        else:
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
        except MissingRecordError:
            return "No such record in table", 404
        except BadFilterError:
            return "Invalid filter requested", 400
        except ValueError:
            return "Bad request", 400
        except TypeError:
            return "Bad request", 400
        except IntegrityError as e:
            return "Bad request", 400

    return wrapper_gets_records


def get_session_id_from_auth_header():
    """
    Gets the sessionID from the Authorization header of a request
    :return: String: SessionID
    """
    parser = reqparse.RequestParser()
    parser.add_argument("Authorization", location="headers")
    args = parser.parse_args()
    if args["Authorization"] is not None:
        return args["Authorization"]
    return ""


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
    filters = request.args.getlist("filter")
    return list(map(lambda x: json.loads(x), filters))
