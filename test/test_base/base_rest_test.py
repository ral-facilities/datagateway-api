from unittest import TestCase

from common.database_helpers import insert_row_into_table, delete_row_by_id
from common.exceptions import MissingRecordError
from common.helpers import is_valid_json
from common.models.db_models import SESSION


class RestTestCase(TestCase):
    """
    Parent class of endpoint test cases
    """

    def setUp(self):
        """
        Inserts a session for testing into the user_sessions table
        """
        insert_row_into_table(SESSION(ID="TestSession"))

    def tearDown(self):
        """
        Removes the inserted session from the user_sessions table
        """
        try:
            delete_row_by_id(SESSION, "TestSession")
        except MissingRecordError:
            pass

    def expect_status_code(self, expected_status_code, response):
        """
        Asserts whethere the returned status code is equal to the expected
        :param expected_status_code: int: The status code that is expected
        :param response: The response to be checked
        """
        self.assertEqual(expected_status_code, response.status_code, "Incorrect status code, received: " +
                         str(response.status_code) + ". Expected " + str(expected_status_code))

    def expect_json_response(self, response):
        """
        Asserts whether the returned item is valid JSON
        :param response: The response to be checked
        """
        self.assertTrue(is_valid_json(response.text), "Response was not valid JSON")
