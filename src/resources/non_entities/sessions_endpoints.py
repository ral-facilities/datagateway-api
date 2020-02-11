import uuid

from flask import request
from flask_restful import Resource, reqparse

from common.database_helpers import insert_row_into_table, delete_row_by_id, get_row_by_id
from common.helpers import get_session_id_from_auth_header, requires_session_id, queries_records
from common.models.db_models import SESSION
import datetime


class Sessions(Resource):

    def post(self):
        """
        Generates a sessionID if the user has correct credentials
        :return: String - SessionID
        """
        if not (request.data and "username" in request.json and "password" in request.json):
            return "Bad request", 400
        if request.json["username"] == "user" and request.json["password"] == "password":
            session_id = str(uuid.uuid1())
            insert_row_into_table(SESSION, SESSION(ID=session_id, USERNAME="simple/root", EXPIREDATETIME=datetime.datetime.now() + datetime.timedelta(days=1)))
            return {"sessionID": session_id}, 201
        return "Forbidden", 403

    @requires_session_id
    @queries_records
    def delete(self):
        """
        Deletes a users sessionID when they logout
        :return: Blank response, 200
        """
        delete_row_by_id(SESSION, get_session_id_from_auth_header())
        return "", 200

    @requires_session_id
    def get(self):
        """
        Gives details of a users session
        :return: String: Details of the session, 200
        """
        return get_row_by_id(SESSION, get_session_id_from_auth_header()).to_dict(), 200

    @requires_session_id
    def put(self):
        """
        Refreshes a users session
        :return: String: The session ID that has been refreshed, 200
        """
        return get_session_id_from_auth_header(), 200
