import re

import requests

from test.test_base.constants import GOOD_CREDENTIALS_HEADER, BAD_CREDENTIALS_HEADER
from test.test_base.base_rest_test import RestTestCase

uuid_pattern = re.compile("\\b[0-9a-f]{8}\\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\\b[0-9a-f]{12}\\b")
sessions_url = "http://localhost:5000/sessions"


def is_session_id_uuid(response):
    if uuid_pattern.match(eval(response.text)["sessionID"]):
        return True
    return False


class TestSessions(RestTestCase):

    def test_post_generate_session_id_with_good_credentials(self):
        response = requests.post(sessions_url, headers={"Authorization": "user:password"})
        self.assertTrue(is_session_id_uuid(response), "sessionID returned is not a uuid")
        self.expect_status_code(201, response)
        self.expect_json_response(response)

    def test_post_generate_session_id_with_bad_credentials(self):
        response = requests.post(sessions_url, headers=BAD_CREDENTIALS_HEADER)
        self.expect_status_code(403, response)

    def test_post_generate_session_id_with_no_credentials(self):
        response = requests.post(sessions_url)
        self.expect_status_code(401, response)

    def test_delete_remove_session_id_with_real_session_id(self):
        response = requests.delete(sessions_url, headers=GOOD_CREDENTIALS_HEADER)
        self.expect_status_code(200, response)

    def test_delete_remove_session_id_with_incorrect_session_id(self):
        response = requests.delete(sessions_url, headers=BAD_CREDENTIALS_HEADER)
        self.expect_status_code(403, response)

    def test_delete_remove_session_id_with_no_session_id(self):
        response = requests.delete(sessions_url)
        self.expect_status_code(403, response)

    def test_get_session_details_with_real_session_id(self):
        response = requests.get(sessions_url, headers=GOOD_CREDENTIALS_HEADER)
        self.expect_status_code(200, response)
        self.expect_json_response(response)

    def test_get_session_details_with_incorrect_session_id(self):
        response = requests.get(sessions_url, headers=BAD_CREDENTIALS_HEADER)
        self.expect_status_code(403, response)

    def test_get_session_details_with_no_session_id(self):
        response = requests.get(sessions_url)
        self.expect_status_code(403, response)

    def test_put_refresh_session_with_real_session_id(self):  # put is not currently not implemented properly
        response = requests.put(sessions_url, headers=GOOD_CREDENTIALS_HEADER)
        self.expect_status_code(200, response)

    def test_put_refresh_session_with_incorrect_session_id(self):  # put is not currently implemented properly
        response = requests.put(sessions_url, headers=BAD_CREDENTIALS_HEADER)
        self.expect_status_code(403, response)

    def test_put_refresh_session_with_no_session_id(self):  # put is not currently implemented properly
        response = requests.put(sessions_url)
        self.expect_status_code(403, response)
