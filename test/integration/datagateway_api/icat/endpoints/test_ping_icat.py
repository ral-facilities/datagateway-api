from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
import pytest

from datagateway_api.common.constants import Constants
from datagateway_api.common.exceptions import PythonICATError
from datagateway_api.main import logger


class TestICATPing:
    def test_valid_ping(self, test_client):
        test_response = test_client.get("/datagateway-api/ping")

        assert test_response.json() == Constants.PING_OK_RESPONSE

    def test_invalid_ping_api_error(self, test_client: TestClient) -> None:
        with patch("icat.client.Client.getEntityNames", side_effect=PythonICATError("Mocked Exception")):
            test_response = test_client.get("/datagateway-api/ping")

        assert test_response.status_code == 500
        assert test_response.json() == {"message": "Mocked Exception"}

    def test_invalid_ping_generic_error(self, test_client: TestClient) -> None:
        """
        Note that as per https://starlette.dev/exceptions/#errors-and-handled-exceptions, 500 codes or instances of
        Exception seem to "bubble through the entire middleware stack as exceptions", i.e. need to be caught with
        `pytest.raises` when calling `test_client.get`. We can still assert that `custom_general_exception_handler` was
        called, by checking the logging within it is called even if we can't assert on the return value like we can for
        an API error, as in the above test.
        """
        mocked = MagicMock(side_effect=logger.exception)
        exception = Exception("Mocked Exception")
        with (
            patch("icat.client.Client.getEntityNames", side_effect=exception),
            patch.object(logger, "exception", new=mocked),
            pytest.raises(Exception, match="Mocked Exception"),
        ):
            test_client.get("/datagateway-api/ping")

        mocked.assert_called_once_with(exception)