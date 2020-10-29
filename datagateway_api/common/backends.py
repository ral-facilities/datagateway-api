from datagateway_api.common.database.backend import DatabaseBackend
from datagateway_api.common.icat.backend import PythonICATBackend
from datagateway_api.common.backend import Backend
from datagateway_api.common.config import config
import sys

backend_type = config.get_backend_type()

if backend_type == "db":
    backend = DatabaseBackend()
elif backend_type == "python_icat":
    backend = PythonICATBackend()
else:
    sys.exit(f"Invalid config value '{backend_type}' for config option backend")
    backend = Backend()
