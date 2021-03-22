import logging
import sys

logging.basicConfig(stream=sys.stderr)

from datagateway_api.src.main import app as application
