import logging

from flask import Flask

from datagateway_api.src.api_start_utils import (
    create_api_endpoints,
    create_app_infrastructure,
    create_openapi_endpoints,
)
from datagateway_api.src.common.config import Config
from datagateway_api.src.common.logger_setup import setup_logger

setup_logger() 
log = logging.getLogger()
log.info("Logging now setup")

app = Flask(__name__)
api, specs = create_app_infrastructure(app)
create_api_endpoints(app, api, specs)
create_openapi_endpoints(app, specs)

if __name__ == "__main__":
    app.run(
        host=Config.config.host,
        port=Config.config.port,
        debug=Config.config.debug_mode,
        use_reloader=Config.config.flask_reloader,
    )
