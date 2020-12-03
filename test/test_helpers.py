from datetime import datetime, timedelta
from unittest import TestCase

from sqlalchemy.exc import IntegrityError

from datagateway_api.common.database.filters import (
    DatabaseDistinctFieldFilter,
    DatabaseIncludeFilter,
    DatabaseLimitFilter,
    DatabaseOrderFilter,
    DatabaseSkipFilter,
    DatabaseWhereFilter,
)
from datagateway_api.common.database.helpers import (
    delete_row_by_id,
    insert_row_into_table,
)
from datagateway_api.common.database.models import SESSION
from datagateway_api.common.exceptions import (
    AuthenticationError,
    BadRequestError,
    FilterError,
    MissingCredentialsError,
    MissingRecordError,
)
from datagateway_api.common.helpers import (
    get_filters_from_query_string,
    get_session_id_from_auth_header,
    is_valid_json,
    queries_records,
)
from test.test_base import FlaskAppTest


class TestIsValidJSON(TestCase):
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


class TestRequiresSessionID(FlaskAppTest):
    def setUp(self):
        super().setUp()
        self.good_credentials_header = {"Authorization": "Bearer Test"}
        self.invalid_credentials_header = {"Authorization": "Test"}
        self.bad_credentials_header = {"Authorization": "Bearer BadTest"}
        session = SESSION()
        session.ID = "Test"
        session.EXPIREDATETIME = datetime.now() + timedelta(hours=1)
        session.username = "Test User"

        insert_row_into_table(SESSION, session)

    def tearDown(self):
        delete_row_by_id(SESSION, "Test")

    def test_missing_credentials(self):
        self.assertEqual(401, self.app.get("/datafiles").status_code)

    def test_invalid_credentials(self):
        self.assertEqual(
            403,
            self.app.get(
                "/datafiles", headers=self.invalid_credentials_header,
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
                "/datafiles?limit=0", headers=self.good_credentials_header,
            ).status_code,
        )


class TestQueriesRecords(TestCase):
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
            raise FilterError()

        with self.assertRaises(FilterError) as ctx:
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


class TestGetSessionIDFromAuthHeader(FlaskAppTest):
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


class TestGetFiltersFromQueryString(FlaskAppTest):
    def test_no_filters(self):
        with self.app:
            self.app.get("/")
            self.assertEqual([], get_filters_from_query_string())

    def test_bad_filter(self):
        with self.app:
            self.app.get('/?test="test"')
            self.assertRaises(FilterError, get_filters_from_query_string)

    def test_limit_filter(self):
        with self.app:
            self.app.get("/?limit=10")
            filters = get_filters_from_query_string()
            self.assertEqual(
                1, len(filters), msg="Returned incorrect number of filters",
            )
            self.assertIs(
                DatabaseLimitFilter, type(filters[0]), msg="Incorrect type of filter",
            )

    def test_order_filter(self):
        with self.app:
            self.app.get('/?order="ID DESC"')
            filters = get_filters_from_query_string()
            self.assertEqual(
                1, len(filters), msg="Returned incorrect number of filters",
            )
            self.assertIs(
                DatabaseOrderFilter,
                type(filters[0]),
                msg="Incorrect type of filter returned",
            )

    def test_where_filter(self):
        with self.app:
            self.app.get('/?where={"ID":{"eq":3}}')
            filters = get_filters_from_query_string()
            self.assertEqual(
                1, len(filters), msg="Returned incorrect number of filters",
            )
            self.assertIs(
                DatabaseWhereFilter,
                type(filters[0]),
                msg="Incorrect type of filter returned",
            )

    def test_skip_filter(self):
        with self.app:
            self.app.get("/?skip=10")
            filters = get_filters_from_query_string()
            self.assertEqual(
                1, len(filters), msg="Returned incorrect number of filters",
            )
            self.assertIs(
                DatabaseSkipFilter,
                type(filters[0]),
                msg="Incorrect type of filter returned",
            )

    def test_include_filter(self):
        with self.app:
            self.app.get('/?include="TEST"')
            filters = get_filters_from_query_string()
            self.assertEqual(
                1, len(filters), msg="Incorrect number of filters returned",
            )
            self.assertIs(
                DatabaseIncludeFilter,
                type(filters[0]),
                msg="Incorrect type of filter returned",
            )

    def test_distinct_filter(self):
        with self.app:
            self.app.get('/?distinct="ID"')
            filters = get_filters_from_query_string()
            self.assertEqual(
                1, len(filters), msg="Incorrect number of filters returned",
            )
            self.assertIs(
                DatabaseDistinctFieldFilter,
                type(filters[0]),
                msg="Incorrect type of filter returned",
            )

    def test_multiple_filters(self):
        with self.app:
            self.app.get("/?limit=10&skip=4")
            filters = get_filters_from_query_string()
            self.assertEqual(2, len(filters))
