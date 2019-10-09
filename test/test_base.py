from unittest import TestCase

from src.main import app


class FlaskAppTest(TestCase):
    """
    The FlaskAppTest Base class sets up a test client to be used to mock requests
    """

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
