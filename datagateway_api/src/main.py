import logging

from flask import Flask

from datagateway_api.common.config import config
from datagateway_api.common.logger_setup import setup_logger
from datagateway_api.src.api_start_utils import (
    create_api_endpoints,
    create_app_infrastructure,
    create_openapi_endpoint,
    openapi_config,
)

setup_logger()
log = logging.getLogger()
log.info("Logging now setup")

app = Flask(__name__)
api, spec = create_app_infrastructure(app)
create_api_endpoints(app, api, spec)
openapi_config(spec)
create_openapi_endpoint(app, spec)

if __name__ == "__main__":
    app.run(
        host=config.get_config_value("host"),
        port=config.get_config_value("port"),
        debug=config.get_config_value("debug_mode"),
        use_reloader=config.get_config_value("flask_reloader"),
    )
