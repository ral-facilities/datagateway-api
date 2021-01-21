import logging

from flask import request
from flask_restful import Resource

from datagateway_api.common.exceptions import AuthenticationError
from datagateway_api.common.helpers import get_session_id_from_auth_header


log = logging.getLogger()


def session_endpoints(backend):
    """
    Generate a flask_restful Resource class using the configured backend. In main.py
    these generated classes are registered with the api e.g.
    `api.add_resource(get_endpoint("Datafiles", DATAFILE), "/datafiles")`

    :param backend: The backend instance used for processing requests
    :type backend: :class:`DatabaseBackend` or :class:`PythonICATBackend`
    :return: The generated session endpoint class
    """

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
                description: Bad request - User credentials not provided in request body
              403:
                 description: Forbidden - User credentials were invalid
            """
            if not (
                request.data
                and "username" in request.json
                and "password" in request.json
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
                description: Unauthorized - No session ID found in HTTP Auth. header
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
                description: Unauthorized - No session ID found in HTTP Auth. header
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
                description: Unauthorized - No session ID found in HTTP Auth. header
              403:
                description: Forbidden - The session ID provided is invalid
            """
            return backend.refresh(get_session_id_from_auth_header()), 200

    return Sessions
