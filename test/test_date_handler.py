from datetime import datetime

import pytest

from datagateway_api.common.date_handler import DateHandler
from datagateway_api.common.exceptions import BadRequestError


class TestIsStrADate:
    def test_valid_date(self):
        date_output = DateHandler.is_str_a_date("2008-10-15")
        assert date_output is True

    def test_valid_boundary_date(self):
        date_output = DateHandler.is_str_a_date("29/2/2020")
        assert date_output is True

    def test_invalid_boundary_date(self):
        date_output = DateHandler.is_str_a_date("29/2/2019")
        # There was no leap year in 2019
        assert date_output is False

    def test_invalid_date(self):
        date_output = DateHandler.is_str_a_date("25/25/2020")
        assert date_output is False


class TestStrToDatetime:
    def test_valid_str(self):
        datetime_output = DateHandler.str_to_datetime_object("2008-10-15 12:05:09")
        assert datetime_output == datetime(
            year=2008, month=10, day=15, hour=12, minute=5, second=9,
        )

    def test_valid_boundary_str(self):
        datetime_output = DateHandler.str_to_datetime_object("2020-02-29 20:20:20")
        assert datetime_output == datetime(
            year=2020, month=2, day=29, hour=20, minute=20, second=20,
        )

    def test_invalid_boundary_str(self):
        with pytest.raises(BadRequestError):
            DateHandler.str_to_datetime_object("2019-02-29 12:05:09")

    def test_invalid_str_format_symbols(self):
        with pytest.raises(BadRequestError):
            DateHandler.str_to_datetime_object("2019/10/05 12:05:09")

    def test_invalid_str_format_order(self):
        with pytest.raises(BadRequestError):
            DateHandler.str_to_datetime_object("12:05:09 2019-10-05")


class TestDatetimeToStr:
    def test_valid_datetime(self):
        example_date = datetime(
            year=2008, month=10, day=15, hour=12, minute=5, second=9,
        )
        str_date_output = DateHandler.datetime_object_to_str(example_date)
        assert str_date_output == "2008-10-15 12:05:09"

    def test_valid_datetime_no_time(self):
        example_date = datetime(year=2008, month=10, day=15)
        str_date_output = DateHandler.datetime_object_to_str(example_date)
        assert str_date_output == "2008-10-15 00:00:00"

    def test_valid_boundary_datetime(self):
        # Can't test invalid leap years as invalid datetime objects can't be created
        example_date = datetime(
            year=2020, month=2, day=29, hour=23, minute=59, second=59,
        )
        str_date_output = DateHandler.datetime_object_to_str(example_date)
        assert str_date_output == "2020-02-29 23:59:59"
