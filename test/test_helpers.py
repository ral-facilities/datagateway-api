from unittest import TestCase

from sqlalchemy.exc import IntegrityError

from common.database_helpers import delete_row_by_id
from common.exceptions import MissingRecordError, BadFilterError, BadRequestError
from common.helpers import is_valid_json, queries_records
from common.models.db_models import SESSION
from src.main import app, insert_row_into_table


class TestIs_valid_json(TestCase):
    def test_array(self):
        self.assertTrue(is_valid_json("[]"))

    def test_null(self):
        self.assertTrue("null")

    def test_valid_json(self):
        self.assertTrue(is_valid_json('{"test":1}'))

    def test_single_quoted_json(self):
        self.assertFalse(is_valid_json("{'test':1}"))

    def test_none(self):
        self.assertFalse(is_valid_json(None))

    def test_int(self):
        self.assertFalse(is_valid_json(1))

    def test_dict(self):
        self.assertFalse(is_valid_json({"test": 1}))

    def test_list(self):
        self.assertFalse(is_valid_json([]))


class TestRequires_session_id(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.good_credentials_header = {"Authorization": "Bearer Test"}
        self.bad_credentials_header = {"Authorization": "Test"}
        session = SESSION()
        session.ID = "Test"
        insert_row_into_table(SESSION, session)

    def tearDown(self):
        delete_row_by_id(SESSION, "Test")

    def test_missing_credentials(self):
        self.assertEqual(401, self.app.get("/datafiles").status_code)

    def test_bad_credentials(self):
        self.assertEqual(403, self.app.get("/datafiles", headers=self.bad_credentials_header).status_code)

    def test_good_credentials(self):
        self.assertEqual(200, self.app.get("/datafiles?limit=0", headers=self.good_credentials_header).status_code)


class TestQueries_records(TestCase):
    def test_missing_record_error(self):
        @queries_records
        def raise_missing_record():
            raise MissingRecordError()

        self.assertEqual(("No such record in table", 404), raise_missing_record())

    def test_bad_filter_error(self):
        @queries_records
        def raise_bad_filter_error():
            raise BadFilterError()

        self.assertEqual(("Invalid filter requested", 400), raise_bad_filter_error())

    def test_value_error(self):
        @queries_records
        def raise_value_error():
            raise ValueError()

        self.assertEqual(("Bad request", 400), raise_value_error())

    def test_type_error(self):
        @queries_records
        def raise_type_error():
            raise TypeError()

        self.assertEqual(("Bad request", 400), raise_type_error())

    def test_integrity_error(self):
        @queries_records
        def raise_integrity_error():
            raise IntegrityError()

        self.assertEqual(("Bad request", 400), raise_integrity_error())

    def test_bad_request_error(self):
        @queries_records
        def raise_bad_request_error():
            raise BadRequestError()

        self.assertEqual(("Bad request", 400), raise_bad_request_error())
