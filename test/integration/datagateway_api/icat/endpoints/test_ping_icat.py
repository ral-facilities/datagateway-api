from unittest.mock import patch

from icat.exception import ICATError
import pytest

from datagateway_api.src.common.constants import Constants
from datagateway_api.src.common.exceptions import PythonICATError
from datagateway_api.src.datagateway_api.icat.icat_client_pool import create_client_pool
from datagateway_api.src.datagateway_api.icat.python_icat import PythonICAT


class TestICATPing:
    def test_valid_ping(self, test_client):
        test_response = test_client.get("/ping")

        assert test_response.json() == Constants.PING_OK_RESPONSE

    def test_invalid_ping(self):
        with patch(
            "icat.client.Client.getEntityNames",
            side_effect=ICATError("Mocked Exception"),
        ):
            python_icat = PythonICAT()
            client_pool = create_client_pool()
            with pytest.raises(PythonICATError):
                python_icat.ping(client_pool=client_pool)
