from flask_restful import Resource


# TODO - Might need kwargs on get_endpoint(), get_id_endpoint(), get_count_endpoint(),
# get_files_endpoint(), get_count_files_endpoint() for client handling?
def get_endpoint(name):
    """
    TODO - Add docstring
    """

    class Endpoint(Resource):
        def get(self):
            """
            TODO - Need to return similar to
            return (
                backend.get_with_filters(
                    get_session_id_from_auth_header(),
                    entity_type,
                    get_filters_from_query_string(),
                    **kwargs,
                ),
                200,
            )
            """
            pass

        # TODO - Add `get.__doc__`

    Endpoint.__name__ = name
    return Endpoint


def get_id_endpoint(name):
    """
    TODO - Add docstring
    """

    class EndpointWithID(Resource):
        def get(self, pid):
            # TODO - Add return
            pass

        # TODO - Add `get.__doc__`

    EndpointWithID.__name__ = name
    return EndpointWithID


def get_count_endpoint(name):
    """
    TODO - Add docstring
    """

    class CountEndpoint(Resource):
        def get(self):
            # TODO - Add return
            pass

        # TODO - Add `get.__doc__`

    CountEndpoint.__name__ = name
    return CountEndpoint


def get_files_endpoint(name):
    """
    TODO - Add docstring
    """

    class FilesEndpoint(Resource):
        def get(self, pid):
            # TODO - Add return
            pass

        # TODO - Add `get.__doc__`

    FilesEndpoint.__name__ = name
    return FilesEndpoint


def get_count_files_endpoint(name):
    """
    TODO - Add docstring
    """

    class CountFilesEndpoint(Resource):
        def get(self, pid):
            # TODO - Add return
            pass

        # TODO - Add `get.__doc__`

    CountFilesEndpoint.__name__ = name
    return CountFilesEndpoint
