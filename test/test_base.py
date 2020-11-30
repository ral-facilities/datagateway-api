from unittest import TestCase

from datagateway_api.src.main import app


class FlaskAppTest(TestCase):
    """
    The FlaskAppTest Base class sets up a test client to be used to mock requests
    """

    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
