import sys

from datagateway_api.common.database.backend import DatabaseBackend
from datagateway_api.common.icat.backend import PythonICATBackend


def create_backend(backend_type):
    """
    Create an instance of a backend dependent on the value parsed into the function. The
    value will typically be from the contents of `config.json`, however when creating a
    backend during automated tests the value will be from the Flask app's config (which
    will be set in the API's config at `common.config`

    The API will exit if a valid value isn't given.

    :param backend_type: The type of backend that should be created and used for the API
    :type backend_type: :class:`str`
    :return: Either an instance of `common.database.backend.DatabaseBackend` or
        `common.icat.backend.PythonICATBackend`
    """

    if backend_type == "db":
        backend = DatabaseBackend()
    elif backend_type == "python_icat":
        backend = PythonICATBackend()
    else:
        # Might turn to a warning so the abstract class can be tested?
        sys.exit(f"Invalid config value '{backend_type}' for config option backend")

    return backend
