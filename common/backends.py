from common.database.backend import DatabaseBackend
from common.icat.backend import PythonICATBackend
from common.backend import Backend
from common.config import config
import sys

backend_type = config.get_backend_type()

if backend_type == "db":
    backend = DatabaseBackend()
elif backend_type == "python_icat":
    backend = PythonICATBackend()
else:
    sys.exit(
        f"Invalid config value '{backend_type}' for config option backend")
    backend = Backend()
