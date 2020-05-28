import uuid

from flask import request
from flask_restful import Resource, reqparse

from common.database_helpers import insert_row_into_table, delete_row_by_id, get_row_by_id
from common.helpers import get_session_id_from_auth_header
from common.models.db_models import SESSION
from common.backends import backend
from common.exceptions import AuthenticationError


class Sessions(Resource):

    def post(self):
        """
        Generates a sessionID if the user has correct credentials
        :return: String - SessionID
        """
        if not (request.data and "username" in request.json and "password" in request.json):
            return "Bad request", 400
        try:
            return {"sessionID": backend.login(request.json)}, 201
        except AuthenticationError:
            return "Forbidden", 403

    def delete(self):
        """
        Deletes a users sessionID when they logout
        :return: Blank response, 200
        """
        backend.logout(get_session_id_from_auth_header())
        return "", 200

    def get(self):
        """
        Gives details of a users session
        :return: String: Details of the session, 200
        """
        return backend.get_session_details(get_session_id_from_auth_header()).to_dict(), 200

    def put(self):
        """
        Refreshes a users session
        :return: String: The session ID that has been refreshed, 200
        """
        return backend.refresh(get_session_id_from_auth_header()), 200
