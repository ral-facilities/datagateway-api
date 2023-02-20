import pytest
from sqlalchemy.exc import IntegrityError

from datagateway_api.src.common.exceptions import (
    BadRequestError,
    FilterError,
    MissingRecordError,
)
from datagateway_api.src.common.helpers import queries_records


class TestQueriesRecords:
    @pytest.mark.parametrize(
        "raised_exception, expected_exception, status_code",
        [
            pytest.param(BadRequestError, BadRequestError, 400, id="bad request error"),
            pytest.param(IntegrityError, BadRequestError, 400, id="integrity error"),
            pytest.param(FilterError, FilterError, 400, id="invalid filter"),
            pytest.param(
                MissingRecordError, MissingRecordError, 404, id="missing record",
            ),
            pytest.param(TypeError, BadRequestError, 400, id="type error"),
            pytest.param(ValueError, BadRequestError, 400, id="value error"),
        ],
    )
    def test_valid_error_raised(
        self, raised_exception, expected_exception, status_code,
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
