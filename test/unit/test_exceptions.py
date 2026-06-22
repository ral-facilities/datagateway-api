import pytest
from fastapi import status

from datagateway_api.common.exceptions import (
    ApiError,
    AuthenticationError,
    BadRequestError,
    DatabaseError,
    FilterError,
    MissingCredentialsError,
    MissingRecordError,
    MultipleIncludeError,
    PythonICATError,
    ScoringAPIError,
    SearchAPIError,
)


class TestExceptions:
    @pytest.mark.parametrize(
        "exception_class, expected_message",
        [
            pytest.param(
                AuthenticationError,
                "Authentication error",
                id="AuthenticationError",
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
                MissingRecordError,
                "No such record in table",
                id="MissingRecordError",
            ),
            pytest.param(
                MultipleIncludeError,
                "Bad request, only one include filter may be given per request",
                id="MultipleIncludeError",
            ),
            pytest.param(PythonICATError, "Python ICAT error", id="PythonICATError"),
            pytest.param(ScoringAPIError, "Scoring API error", id="ScoringAPIError"),
            pytest.param(SearchAPIError, "Search API error", id="SearchAPIError"),
        ],
    )
    def test_valid_exception_message(self, exception_class, expected_message):
        assert exception_class().args[0] == expected_message

    @pytest.mark.parametrize(
        "exception_class, expected_status_code",
        [
            pytest.param(ApiError, status.HTTP_500_INTERNAL_SERVER_ERROR, id="ApiError"),
            pytest.param(AuthenticationError, status.HTTP_403_FORBIDDEN, id="AuthenticationError"),
            pytest.param(BadRequestError, status.HTTP_400_BAD_REQUEST, id="BadRequestError"),
            pytest.param(DatabaseError, status.HTTP_500_INTERNAL_SERVER_ERROR, id="DatabaseError"),
            pytest.param(FilterError, status.HTTP_400_BAD_REQUEST, id="FilterError"),
            pytest.param(MissingCredentialsError, status.HTTP_401_UNAUTHORIZED, id="MissingCredentialsError"),
            pytest.param(MissingRecordError, status.HTTP_404_NOT_FOUND, id="MissingRecordError"),
            pytest.param(MultipleIncludeError, status.HTTP_400_BAD_REQUEST, id="MultipleIncludeError"),
            pytest.param(PythonICATError, status.HTTP_500_INTERNAL_SERVER_ERROR, id="PythonICATError"),
            pytest.param(ScoringAPIError, status.HTTP_500_INTERNAL_SERVER_ERROR, id="ScoringAPIError"),
            pytest.param(SearchAPIError, status.HTTP_500_INTERNAL_SERVER_ERROR, id="SearchAPIError"),
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
            pytest.param(ScoringAPIError, id="ScoringAPIError"),
            pytest.param(SearchAPIError, id="SearchAPIError"),
        ],
    )
    def test_valid_raise_exception(self, exception_class):
        def raise_exception():
            raise exception_class()

        with pytest.raises(exception_class):
            raise_exception()
