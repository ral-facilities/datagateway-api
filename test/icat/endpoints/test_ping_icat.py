from unittest.mock import patch

from icat.exception import ICATError
import pytest

from datagateway_api.common.backends import create_backend
from datagateway_api.common.constants import Constants
from datagateway_api.common.exceptions import PythonICATError
from datagateway_api.common.icat.icat_client_pool import create_client_pool


class TestICATPing:
    def test_valid_ping(self, flask_test_app_icat):
        test_response = flask_test_app_icat.get("/ping")

        assert test_response.json == Constants.PING_OK_RESPONSE

    def test_invalid_ping(self):
        with patch(
            "icat.client.Client.getEntityNames",
            side_effect=ICATError("Mocked Exception"),
        ):
            with pytest.raises(PythonICATError):
                backend = create_backend("python_icat")
                client_pool = create_client_pool()
                backend.ping(client_pool=client_pool)
