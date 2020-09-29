from common.database.backend import DatabaseBackend
from common.icat.backend import PythonICATBackend
from common.backend import Backend
from common.config import config
import sys


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
