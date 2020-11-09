from unittest import TestCase

from datagateway_api.src.main import app


# Move this into the test defintions and let it be inherited in test classes that need
# it
class FlaskAppTest(TestCase):
    """
    The FlaskAppTest Base class sets up a test client to be used to mock requests
    """

    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
