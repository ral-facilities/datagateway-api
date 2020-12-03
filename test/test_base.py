from unittest import TestCase

from flask import Flask

from datagateway_api.src.main import create_api_endpoints, create_app_infrastructure


class FlaskAppTest(TestCase):
    """
    The FlaskAppTest Base class sets up a test client to be used to mock requests
    """

    def setUp(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["TESTING"] = True
        app.config["TEST_BACKEND"] = "db"

        api, spec = create_app_infrastructure(app)
        create_api_endpoints(app, api, spec)
        self.app = app.test_client()
