import sys

from datagateway_api.common.backend import Backend
from datagateway_api.common.database.backend import DatabaseBackend
from datagateway_api.common.icat.backend import PythonICATBackend


def create_backend(backend_type):
    """
    TODO - Add docstring
    """

    if backend_type == "db":
        backend = DatabaseBackend()
    elif backend_type == "python_icat":
        backend = PythonICATBackend()
    else:
        # Might turn to a warning so the abstract class can be tested?
        sys.exit(f"Invalid config value '{backend_type}' for config option backend")
        backend = Backend()

    return backend
