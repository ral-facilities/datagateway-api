import pytest

from datagateway_api.src.common.exceptions import (
    ApiError,
    AuthenticationError,
    BadRequestError,
    DatabaseError,
    FilterError,
    MissingCredentialsError,
    MissingRecordError,
    MultipleIncludeError,
    PythonICATError,
)


class TestExceptions:
    @pytest.mark.parametrize(
        "exception_class, expected_message",
        [
            pytest.param(
                AuthenticationError, "Authentication error", id="AuthenticationError",
            ),
            pytest.param(BadRequestError, "Bad request", id="BadRequestError"),
            pytest.param(DatabaseError, "Database error", id="DatabaseError"),
            pytest.param(FilterError, "Invalid filter requested", id="FilterError"),
            pytest.param(
                MissingCredentialsError,
                "No credentials provided in auth header",
                id="MissingCredentialsError",
            ),
            pytest.param(
                MissingRecordError, "No such record in table", id="MissingRecordError",
            ),
            pytest.param(
                MultipleIncludeError,
                "Bad request, only one include filter may be given per request",
                id="MultipleIncludeError",
            ),
            pytest.param(PythonICATError, "Python ICAT error", id="PythonICATError"),
        ],
    )
    def test_valid_exception_message(self, exception_class, expected_message):
        assert exception_class().args[0] == expected_message

    @pytest.mark.parametrize(
        "exception_class, expected_status_code",
        [
            pytest.param(ApiError, 500, id="ApiError"),
            pytest.param(AuthenticationError, 403, id="AuthenticationError"),
            pytest.param(BadRequestError, 400, id="BadRequestError"),
            pytest.param(DatabaseError, 500, id="DatabaseError"),
            pytest.param(FilterError, 400, id="FilterError"),
            pytest.param(MissingCredentialsError, 401, id="MissingCredentialsError"),
            pytest.param(MissingRecordError, 404, id="MissingRecordError"),
            pytest.param(MultipleIncludeError, 400, id="MultipleIncludeError"),
            pytest.param(PythonICATError, 500, id="PythonICATError"),
        ],
    )
    def test_valid_exception_status_code(self, exception_class, expected_status_code):
        assert exception_class().status_code == expected_status_code

    @pytest.mark.parametrize(
        "exception_class",
        [
            pytest.param(ApiError, id="ApiError"),
            pytest.param(AuthenticationError, id="AuthenticationError"),
            pytest.param(BadRequestError, id="BadRequestError"),
            pytest.param(DatabaseError, id="DatabaseError"),
            pytest.param(FilterError, id="FilterError"),
            pytest.param(MissingCredentialsError, id="MissingCredentialsError"),
            pytest.param(MissingRecordError, id="MissingRecordError"),
            pytest.param(MultipleIncludeError, id="MultipleIncludeError"),
            pytest.param(PythonICATError, id="PythonICATError"),
        ],
    )
    def test_valid_raise_exception(self, exception_class):
        def raise_exception():
            raise exception_class()

        with pytest.raises(exception_class):
            raise_exception()
