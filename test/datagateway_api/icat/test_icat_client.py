import json
from unittest.mock import mock_open, patch

from icat.client import Client
import pytest

from datagateway_api.src.common.config import APIConfig
from datagateway_api.src.datagateway_api.icat.icat_client_pool import ICATClient


class TestICATClient:
    def test_init(self):
        test_icat_client = ICATClient()
        assert isinstance(test_icat_client, Client)

        assert not test_icat_client.autoLogout

    @pytest.mark.parametrize(
        "client_use, expected_url, expected_check_cert",
        [
            pytest.param(
                "datagateway_api",
                "https://localhost:8181/ICATService/ICAT?wsdl",
                False,
                id="DataGateway API Usage",
            ),
            pytest.param(
                "search_api",
                "https://localhost.testdomain:8181/ICATService/ICAT?wsdl",
                True,
                id="Search API Usage",
            ),
        ],
    )
    def test_client_use(
        self, test_config_data, client_use, expected_url, expected_check_cert,
    ):
        with patch("builtins.open", mock_open(read_data=json.dumps(test_config_data))):
            api_config = APIConfig.load("test/path")

            class MockClient:
                def __init__(url, checkCert=True):  # noqa
                    print(f"URL: {url}, Cert: {checkCert}")
                    # Would've preferred to assign these values to self but this didn't
                    # seem to be possible
                    Client.url = f"{url}/ICATService/ICAT?wsdl"
                    Client.checkCert = checkCert

            with patch(
                "datagateway_api.src.common.config.Config.config", api_config,
            ):
                with patch(
                    "icat.client.Client.__init__", side_effect=MockClient.__init__,
                ):
                    test_icat_client = ICATClient(client_use)
                    assert test_icat_client.url == expected_url
                    assert test_icat_client.checkCert == expected_check_cert

    def test_clean_up(self):
        test_icat_client = ICATClient()
        assert id(test_icat_client) in Client.Register
        test_icat_client.clean_up()
        assert id(test_icat_client) not in Client.Register
