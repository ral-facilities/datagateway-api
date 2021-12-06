from flask_restful import Resource

from datagateway_api.src.search_api.helpers import (
    get_count,
    get_files,
    get_files_count,
    get_search,
    get_with_id,
)


def get_search_endpoint(name):
    """
    TODO - Add docstring
    """

    class Endpoint(Resource):
        def get(self):
            return get_search(name), 200

        # TODO - Add `get.__doc__`

    Endpoint.__name__ = name
    return Endpoint


def get_single_endpoint(name):
    """
    TODO - Add docstring
    """

    class EndpointWithID(Resource):
        def get(self, pid):
            return get_with_id(name, pid), 200

        # TODO - Add `get.__doc__`

    EndpointWithID.__name__ = name
    return EndpointWithID


def get_number_count_endpoint(name):
    """
    TODO - Add docstring
    """

    class CountEndpoint(Resource):
        def get(self):
            return get_count(name), 200

        # TODO - Add `get.__doc__`

    CountEndpoint.__name__ = name
    return CountEndpoint


def get_files_endpoint(name):
    """
    TODO - Add docstring
    """

    class FilesEndpoint(Resource):
        def get(self, pid):
            return get_files(name), 200

        # TODO - Add `get.__doc__`

    FilesEndpoint.__name__ = name
    return FilesEndpoint


def get_number_count_files_endpoint(name):
    """
    TODO - Add docstring
    """

    class CountFilesEndpoint(Resource):
        def get(self, pid):
            return get_files_count(name, pid)

        # TODO - Add `get.__doc__`

    CountFilesEndpoint.__name__ = name
    return CountFilesEndpoint
