import logging

from flask import Flask

from datagateway_api.src.api_start_utils import (
    create_api_endpoints,
    create_app_infrastructure,
    create_openapi_endpoint,
    openapi_config,
)
from datagateway_api.src.common.config import config
from datagateway_api.src.common.logger_setup import setup_logger

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
        host=config.host,
        port=config.port,
        debug=config.debug_mode,
        use_reloader=config.flask_reloader,
    )
