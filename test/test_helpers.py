from unittest import TestCase

from sqlalchemy.exc import IntegrityError

from common.database.helpers import (
    delete_row_by_id,
    insert_row_into_table,
    LimitFilter,
    DistinctFieldFilter,
    IncludeFilter,
    SkipFilter,
    WhereFilter,
    OrderFilter,
)
from common.exceptions import (
    MissingRecordError,
    BadFilterError,
    BadRequestError,
    MissingCredentialsError,
    AuthenticationError,
)
from common.helpers import (
    is_valid_json,
    queries_records,
    get_session_id_from_auth_header,
    get_filters_from_query_string,
)
from common.models.db_models import SESSION
from test.test_base import FlaskAppTest


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


class TestRequires_session_id(FlaskAppTest):
    def setUp(self):
        super().setUp()
        self.good_credentials_header = {"Authorization": "Bearer Test"}
        self.invalid_credentials_header = {"Authorization": "Test"}
        self.bad_credentials_header = {"Authorization": "Bearer BadTest"}
        session = SESSION()
        session.ID = "Test"
        insert_row_into_table(SESSION, session)

    def tearDown(self):
        delete_row_by_id(SESSION, "Test")

    def test_missing_credentials(self):
        self.assertEqual(401, self.app.get("/datafiles").status_code)

    def test_invalid_credentials(self):
        self.assertEqual(
            403,
            self.app.get(
                "/datafiles", headers=self.invalid_credentials_header
            ).status_code,
        )

    def test_bad_credentials(self):
        self.assertEqual(
            403,
            self.app.get("/datafiles", headers=self.bad_credentials_header).status_code,
        )

    def test_good_credentials(self):
        self.assertEqual(
            200,
            self.app.get(
                "/datafiles?limit=0", headers=self.good_credentials_header
            ).status_code,
        )


class TestQueries_records(TestCase):
    def test_missing_record_error(self):
        @queries_records
        def raise_missing_record():
            raise MissingRecordError()

        with self.assertRaises(MissingRecordError) as ctx:
            raise_missing_record()
        self.assertEqual("No such record in table", str(ctx.exception))
        self.assertEqual(404, ctx.exception.status_code)

    def test_bad_filter_error(self):
        @queries_records
        def raise_bad_filter_error():
            raise BadFilterError()

        with self.assertRaises(BadFilterError) as ctx:
            raise_bad_filter_error()

        self.assertEqual("Invalid filter requested", str(ctx.exception))
        self.assertEqual(400, ctx.exception.status_code)

    def test_value_error(self):
        @queries_records
        def raise_value_error():
            raise ValueError()

        with self.assertRaises(BadRequestError) as ctx:
            raise_value_error()

        self.assertEqual("Bad request", str(ctx.exception))
        self.assertEqual(400, ctx.exception.status_code)

    def test_type_error(self):
        @queries_records
        def raise_type_error():
            raise TypeError()

        with self.assertRaises(BadRequestError) as ctx:
            raise_type_error()

        self.assertEqual("Bad request", str(ctx.exception))
        self.assertEqual(400, ctx.exception.status_code)

    def test_integrity_error(self):
        @queries_records
        def raise_integrity_error():
            raise IntegrityError()

        with self.assertRaises(BadRequestError) as ctx:
            raise_integrity_error()

        self.assertEqual("Bad request", str(ctx.exception))
        self.assertEqual(400, ctx.exception.status_code)

    def test_bad_request_error(self):
        @queries_records
        def raise_bad_request_error():
            raise BadRequestError()

        with self.assertRaises(BadRequestError) as ctx:
            raise_bad_request_error()

        self.assertEqual("Bad request", str(ctx.exception))
        self.assertEqual(400, ctx.exception.status_code)


class TestGet_session_id_from_auth_header(FlaskAppTest):
    def test_no_session_in_header(self):
        with self.app:
            self.app.get("/")
            self.assertRaises(MissingCredentialsError, get_session_id_from_auth_header)

    def test_with_bad_header(self):
        with self.app:
            self.app.get("/", headers={"Authorization": "test"})
            self.assertRaises(AuthenticationError, get_session_id_from_auth_header)

    def test_with_good_header(self):
        with self.app:
            self.app.get("/", headers={"Authorization": "Bearer test"})
            self.assertEqual("test", get_session_id_from_auth_header())


class TestGet_filters_from_query_string(FlaskAppTest):
    def test_no_filters(self):
        with self.app:
            self.app.get("/")
            self.assertEqual([], get_filters_from_query_string())

    def test_bad_filter(self):
        with self.app:
            self.app.get('/?test="test"')
            self.assertRaises(BadFilterError, get_filters_from_query_string)

    def test_limit_filter(self):
        with self.app:
            self.app.get("/?limit=10")
            filters = get_filters_from_query_string()
            self.assertEqual(
                1, len(filters), msg="Returned incorrect number of filters"
            )
            self.assertIs(LimitFilter, type(filters[0]), msg="Incorrect type of filter")

    def test_order_filter(self):
        with self.app:
            self.app.get('/?order="ID DESC"')
            filters = get_filters_from_query_string()
            self.assertEqual(
                1, len(filters), msg="Returned incorrect number of filters"
            )
            self.assertIs(
                OrderFilter, type(filters[0]), msg="Incorrect type of filter returned"
            )

    def test_where_filter(self):
        with self.app:
            self.app.get('/?where={"ID":{"eq":3}}')
            filters = get_filters_from_query_string()
            self.assertEqual(
                1, len(filters), msg="Returned incorrect number of filters"
            )
            self.assertIs(
                WhereFilter, type(filters[0]), msg="Incorrect type of filter returned"
            )

    def test_skip_filter(self):
        with self.app:
            self.app.get("/?skip=10")
            filters = get_filters_from_query_string()
            self.assertEqual(
                1, len(filters), msg="Returned incorrect number of filters"
            )
            self.assertIs(
                SkipFilter, type(filters[0]), msg="Incorrect type of filter returned"
            )

    def test_include_filter(self):
        with self.app:
            self.app.get('/?include="TEST"')
            filters = get_filters_from_query_string()
            self.assertEqual(
                1, len(filters), msg="Incorrect number of filters returned"
            )
            self.assertIs(
                IncludeFilter, type(filters[0]), msg="Incorrect type of filter returned"
            )

    def test_distinct_filter(self):
        with self.app:
            self.app.get('/?distinct="ID"')
            filters = get_filters_from_query_string()
            self.assertEqual(
                1, len(filters), msg="Incorrect number of filters returned"
            )
            self.assertIs(
                DistinctFieldFilter,
                type(filters[0]),
                msg="Incorrect type of filter returned",
            )

    def test_multiple_filters(self):
        with self.app:
            self.app.get("/?limit=10&skip=4")
            filters = get_filters_from_query_string()
            self.assertEqual(2, len(filters))
