import requests

from common.database_helpers import delete_row_by_id, EntityManager
from common.exceptions import MissingRecordError
from common.models.db_models import DATAFILE
from test.test_base.base_rest_test import RestTestCase
from test.test_base.constants import GOOD_CREDENTIALS_HEADER, BAD_CREDENTIALS_HEADER

url_with_file_existing = "http://localhost:5000/datafiles/-50"
url_without_file_existing = "http://localhost:5000/datafiles/0"
good_data = {"NAME":"test"}
bad_data = '{"NAMEFf" : "test"}'


class TestDatafiles(RestTestCase):

    def setUp(self):
        super().setUp()
        EntityManager.insert_row_into_table(DATAFILE, DATAFILE(ID=-50, MOD_ID="modID", CREATE_ID="create_id",
                                                        NAME="test_name", MOD_TIME="2019-05-05 11:11:11",
                                                        CREATE_TIME="2019-04-06 12:12:12",DATASET_ID=1))


    def tearDown(self):
        super().tearDown()
        try:  # This catches the exception when we attempt to delete the file, that was deleted in the test
            delete_row_by_id(DATAFILE, -50)
        except MissingRecordError:
            pass

    def test_get_with_id_with_credentials_and_file_exist(self):
        response = requests.get(url_with_file_existing, headers=GOOD_CREDENTIALS_HEADER)
        self.expect_status_code(200, response)
        self.expect_json_response(response)
        # Add test to check the correct datafile is being returned

    def test_get_with_id_with_bad_credentials_and_file_exists(self):
        response = requests.get(url_with_file_existing, headers=BAD_CREDENTIALS_HEADER)
        self.expect_status_code(403, response)

    def test_get_with_id_with_no_credentials_and_file_exists(self):
        response = requests.get(url_with_file_existing)
        self.expect_status_code(403, response)

    def test_get_with_id_with_credentials_and_file_doesnt_exist(self):
        response = requests.get(url_without_file_existing, headers=GOOD_CREDENTIALS_HEADER)
        self.expect_status_code(404, response)

    def test_get_with_id_with_bad_credentials_and_file_doesnt_exist(self):
        response = requests.get(url_without_file_existing, headers=BAD_CREDENTIALS_HEADER)
        self.expect_status_code(403, response)

    def test_get_with_id_with_no_credentials_and_file_doesnt_exist(self):
        response = requests.get(url_without_file_existing, headers=BAD_CREDENTIALS_HEADER)
        self.expect_status_code(403, response)

    def test_delete_with_credentials_and_file_exists(self):
        response = requests.delete(url_with_file_existing, headers=GOOD_CREDENTIALS_HEADER)
        self.expect_status_code(204, response)

    def test_delete_with_bad_credentials_and_file_exists(self):
        response = requests.delete(url_with_file_existing, headers=BAD_CREDENTIALS_HEADER)
        self.expect_status_code(403, response)

    def test_delete_with_no_credentials_and_file_exists(self):
        response = requests.delete(url_with_file_existing)
        self.expect_status_code(403, response)

    def test_delete_with_credentials_and_file_doesnt_exists(self):
        response = requests.delete(url_without_file_existing, headers=GOOD_CREDENTIALS_HEADER)
        self.expect_status_code(404, response)

    def test_delete_with_bad_credentials_and_file_doesnt_exists(self):
        response = requests.delete(url_without_file_existing, headers=BAD_CREDENTIALS_HEADER)
        self.expect_status_code(403, response)

    def test_delete_with_no_credentials_and_file_doesnt_exists(self):
        response = requests.delete(url_without_file_existing)
        self.expect_status_code(403, response)

    def test_patch_with_credentials_and_file_exists_with_valid_data(self):
        response = requests.patch(url_with_file_existing, headers=GOOD_CREDENTIALS_HEADER, json=good_data)
        self.expect_status_code(200, response)
        self.expect_json_response(response)

    def test_patch_with_credentials_and_file_exists_with_invalid_data(self):
        response = requests.patch(url_with_file_existing, headers=GOOD_CREDENTIALS_HEADER, json=bad_data)
        self.expect_status_code(400, response)

    def test_patch_with_credentials_and_file_exists_with_no_data(self):
        response = requests.patch(url_with_file_existing, headers=GOOD_CREDENTIALS_HEADER)
        self.expect_status_code(400, response)

    def test_patch_with_credentials_and_file_doesnt_exist_with_valid_data(self):
        response = requests.patch(url_without_file_existing, headers=GOOD_CREDENTIALS_HEADER, json=good_data)
        self.expect_status_code(404, response)

    def test_patch_with_credentials_and_file_doesnt_exist_with_invalid_data(self):
        response = requests.patch(url_without_file_existing, headers=GOOD_CREDENTIALS_HEADER, json=bad_data)
        self.expect_status_code(404, response)

    def test_patch_with_credentaisl_and_file_doesnt_exist_with_no_data(self):
        response = requests.patch(url_without_file_existing, headers=GOOD_CREDENTIALS_HEADER)
        self.expect_status_code(404, response)

    def test_patch_with_bad_credentials_and_file_exists_with_valid_data(self):
        response = requests.patch(url_with_file_existing, headers=BAD_CREDENTIALS_HEADER, json=good_data )
        self.expect_status_code(403, response)

    def test_patch_with_no_credentials_and_file_exists_without_valid_data(self):
        response = requests.patch(url_with_file_existing, json=bad_data)
        self.expect_status_code(403, response)