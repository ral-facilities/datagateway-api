import pytest

from datagateway_api.src.common.exceptions import (
    ApiError,
    BadRequestError,
    FilterError,
    MissingRecordError,
    ScoringAPIError,
    SearchAPIError,
)
from datagateway_api.src.search_api.helpers import search_api_error_handling
from datagateway_api.src.search_api.models import Document


class TestErrorHandling:
    @pytest.mark.parametrize(
        "raised_exception, expected_exception, status_code",
        [
            pytest.param(BadRequestError, BadRequestError, 400, id="Bad request error"),
            pytest.param(FilterError, FilterError, 400, id="Invalid filter"),
            pytest.param(
                MissingRecordError, MissingRecordError, 404, id="Missing record",
            ),
            pytest.param(ScoringAPIError, SearchAPIError, 500, id="Scoring API error"),
            pytest.param(SearchAPIError, SearchAPIError, 500, id="Search API error"),
            pytest.param(TypeError, BadRequestError, 400, id="Type error"),
            pytest.param(ValueError, BadRequestError, 400, id="Value error"),
            pytest.param(AttributeError, BadRequestError, 400, id="Attribute error"),
            pytest.param(ImportError, ImportError, 500, id="Import error"),
            pytest.param(Document, SearchAPIError, 500, id="Validation error"),
        ],
    )
    def test_valid_error_raised(
        self, raised_exception, expected_exception, status_code,
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
