import pytest
from fastapi import status
from pydantic import ValidationError

from datagateway_api.common.exceptions import (
    BadRequestError,
    FilterError,
    MissingRecordError,
)
from datagateway_api.common.helpers import queries_records


class TestQueriesRecords:
    @pytest.mark.parametrize(
        "raised_exception, expected_exception, status_code",
        [
            pytest.param(BadRequestError, BadRequestError, status.HTTP_400_BAD_REQUEST, id="bad request error"),
            pytest.param(ValidationError, BadRequestError, status.HTTP_400_BAD_REQUEST, id="validation error"),
            pytest.param(FilterError, FilterError, status.HTTP_400_BAD_REQUEST, id="invalid filter"),
            pytest.param(
                MissingRecordError,
                MissingRecordError,
                status.HTTP_404_NOT_FOUND,
                id="missing record",
            ),
            pytest.param(TypeError, BadRequestError, status.HTTP_400_BAD_REQUEST, id="type error"),
            pytest.param(ValueError, BadRequestError, status.HTTP_400_BAD_REQUEST, id="value error"),
        ],
    )
    def test_valid_error_raised(
        self,
        raised_exception,
        expected_exception,
        status_code,
    ):
        @queries_records
        def raise_exception():
            raise raised_exception()

        try:
            raise_exception()
        except Exception as e:
            assert e.status_code == status_code

        with pytest.raises(expected_exception):
            raise_exception()
