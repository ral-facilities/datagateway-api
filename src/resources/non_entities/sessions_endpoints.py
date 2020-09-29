import uuid
import logging

from flask import request
from flask_restful import Resource, reqparse

from common.database.helpers import (
    insert_row_into_table,
    delete_row_by_id,
    get_row_by_id,
)
from common.helpers import get_session_id_from_auth_header
from common.models.db_models import SESSION
from common.backends import create_backend
from common.exceptions import AuthenticationError
from common.config import config

log = logging.getLogger()

backend = create_backend(config.get_backend_type())

class Sessions(Resource):
    def post(self):
        """
        Generates a sessionID if the user has correct credentials
        :return: String - SessionID

        ---
        summary: Login
        description: Generates a sessionID if the user has correct credentials
        tags:
         - Sessions
        security: []
        requestBody:
          description: User credentials to login with
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  username:
                    type: string
                  password:
                    type: string
                  mechanism:
                    type: string
        responses:
          201:
            description: Success - returns a session ID
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    sessionID:
                      type: string
                      description: Session ID
                      example: xxxxxx-yyyyyyy-zzzzzz
          400:
            description: Bad request. User credentials were not provided in request body.
          403: 
             description: Forbidden. User credentials were invalid
        """
        if not (
            request.data and "username" in request.json and "password" in request.json
        ):
            return "Bad request", 400
        # If no mechanism is present in request body, default to simple
        if not ("mechanism" in request.json):
            request.json["mechanism"] = "simple"
        try:
            return {"sessionID": backend.login(request.json)}, 201
        except AuthenticationError:
            return "Forbidden", 403

    def delete(self):
        """
        Deletes a users sessionID when they logout
        :return: Blank response, 200
        ---
        summary: Delete session
        description: Deletes a users sessionID when they logout
        tags:
         - Sessions
        responses:
          200:
            description: Success - User's session was successfully deleted
          400:
            description: Bad request - something was wrong with the request
          401:
            description: Unauthorized - No session ID was found in the HTTP Authorization header
          403:
            description: Forbidden - The session ID provided is invalid
          404:
            description: Not Found - Unable to find session ID
        """
        backend.logout(get_session_id_from_auth_header())
        return "", 200

    def get(self):
        """
        Gives details of a users session
        :return: String: Details of the session, 200
        ---
        summary: Get session details
        description: Gives details of a user's session
        tags:
         - Sessions
        responses:
          200:
            description: Success - a user's session details
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    ID:
                      type: string
                      description: The session ID
                      example: xxxxxx-yyyyyyy-zzzzzz
                    EXPIREDATETIME:
                      type: string
                      format: datetime
                      description: When this session expires
                      example: "2017-07-21T17:32:28Z"
                    USERNAME:
                      type: string
                      description: Username associated with this session
          401:
            description: Unauthorized - No session ID was found in the HTTP Authorization header
          403:
            description: Forbidden - The session ID provided is invalid
        """
        return backend.get_session_details(get_session_id_from_auth_header()), 200

    def put(self):
        """
        Refreshes a users session
        :return: String: The session ID that has been refreshed, 200
        ---
        summary: Refresh session
        description: Refreshes a users session
        tags:
         - Sessions
        responses:
          200:
            description: Success - the user's session ID that has been refreshed
            content:
              application/json:
                schema:
                  type: string
                  description: Session ID
                  example: xxxxxx-yyyyyyy-zzzzzz
          401:
            description: Unauthorized - No session ID was found in the HTTP Authorization header
          403:
            description: Forbidden - The session ID provided is invalid
        """
        return backend.refresh(get_session_id_from_auth_header()), 200
