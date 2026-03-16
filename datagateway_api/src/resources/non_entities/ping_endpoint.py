from flask_restful import Resource


def ping_endpoint(python_icat, **kwargs):
    """
    Generate a flask_restful Resource class using python ICAT. In main.py
    these generated classes are registered with the api e.g.
    `api.add_resource(get_endpoint("Datafiles", DATAFILE), "/datafiles")`

    :param python_icat: The python ICAT instance used for processing requests
    :type python_icat: :class:`PythonICAT`
    :return: The generated ping endpoint class
    """

    class Ping(Resource):
        def get(self):
            """
            Pings the connection method to ensure the API is responsive
            :return: String: A standard OK message, 200
            ---
            summary: Ping API connection method
            description: Pings the API's connection method to check responsiveness
            tags:
              - Ping
            responses:
              200:
                description: Success - the API is responsive on the python ICAT server
                content:
                  application/json:
                    schema:
                      type: string
                      description: OK message
                      example: DataGateway API OK
              500:
                description: Pinging the API's connection method has gone wrong
            """
            return python_icat.ping(**kwargs), 200

    return Ping
