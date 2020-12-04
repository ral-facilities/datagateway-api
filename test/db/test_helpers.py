from unittest import TestCase

from sqlalchemy.exc import IntegrityError

from datagateway_api.common.exceptions import (
    BadRequestError,
    FilterError,
    MissingRecordError,
)
from datagateway_api.common.helpers import queries_records


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
