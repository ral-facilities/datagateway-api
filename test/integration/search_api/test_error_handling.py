import pytest
from fastapi import status

from datagateway_api.common.exceptions import (
    ApiError,
    BadRequestError,
    FilterError,
    MissingRecordError,
    ScoringAPIError,
    SearchAPIError,
)
from datagateway_api.search_api.helpers import search_api_error_handling
from datagateway_api.search_api.models import Document


class TestErrorHandling:
    @pytest.mark.parametrize(
        "raised_exception, expected_exception, status_code",
        [
            pytest.param(BadRequestError, BadRequestError, status.HTTP_400_BAD_REQUEST, id="Bad request error"),
            pytest.param(FilterError, FilterError, status.HTTP_400_BAD_REQUEST, id="Invalid filter"),
            pytest.param(
                MissingRecordError,
                MissingRecordError,
                status.HTTP_404_NOT_FOUND,
                id="Missing record",
            ),
            pytest.param(
                ScoringAPIError, SearchAPIError, status.HTTP_500_INTERNAL_SERVER_ERROR, id="Scoring API error"
            ),
            pytest.param(SearchAPIError, SearchAPIError, status.HTTP_500_INTERNAL_SERVER_ERROR, id="Search API error"),
            pytest.param(TypeError, BadRequestError, status.HTTP_400_BAD_REQUEST, id="Type error"),
            pytest.param(ValueError, BadRequestError, status.HTTP_400_BAD_REQUEST, id="Value error"),
            pytest.param(AttributeError, BadRequestError, status.HTTP_400_BAD_REQUEST, id="Attribute error"),
            pytest.param(ImportError, ImportError, status.HTTP_500_INTERNAL_SERVER_ERROR, id="Import error"),
            pytest.param(Document, SearchAPIError, status.HTTP_500_INTERNAL_SERVER_ERROR, id="Validation error"),
        ],
    )
    def test_valid_error_raised(
        self,
        raised_exception,
        expected_exception,
        status_code,
    ):
        @search_api_error_handling
        def raise_exception():
            if isinstance(raised_exception(), Exception):
                raise raised_exception()
            else:
                # To raise Pydantic ValidationError from object creation
                raised_exception()

        try:
            raise_exception()
        except Exception as e:
            assert isinstance(e.args[0], dict)
            # Non-API defined exception won't have a `status_code` attribute
            if isinstance(e, ApiError):
                assert e.status_code == status_code
            assert list(e.args[0]["error"].keys()) == ["statusCode", "name", "message"]

        with pytest.raises(expected_exception):
            raise_exception()
