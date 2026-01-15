import logging

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

from datagateway_api.src.api_start_utils import (
    create_api_endpoints,
    create_app_infrastructure,
    create_openapi_endpoints,
)
from datagateway_api.src.common.config import Config
from datagateway_api.src.common.logger_setup import setup_logger
from datagateway_api.src.datagateway_api.build_models import build_datagateway_api_model
from datagateway_api.src.datagateway_api.icat.icat_client_pool import create_client_pool
from datagateway_api.src.datagateway_api.icat.python_icat import PythonICAT


setup_logger()
log = logging.getLogger()
log.info("Logging now setup")

app = Flask(__name__)

python_icat = PythonICAT()
# Create client pool
icat_client_pool = create_client_pool()
dg_models = build_datagateway_api_model(client_pool=icat_client_pool)
api, specs = create_app_infrastructure(app, dg_models.values())
create_api_endpoints(app, api, specs, python_icat, icat_client_pool)
create_openapi_endpoints(app, specs)
app.config["APPLICATION_ROOT"] = Config.config.url_prefix

if __name__ == "__main__":
    app.wsgi_app = DispatcherMiddleware(
        Response("Not Found", status=404),
        {Config.config.url_prefix: app.wsgi_app},
    )
    app.run(
        host=Config.config.host,
        port=Config.config.port,
        debug=Config.config.debug_mode,
        use_reloader=Config.config.flask_reloader,
    )
