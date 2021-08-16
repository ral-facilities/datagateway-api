from icat.client import Client

from datagateway_api.common.icat.icat_client_pool import ICATClient


class TestICATClient:
    def test_init(self):
        test_icat_client = ICATClient()
        assert isinstance(test_icat_client, Client)

        assert not test_icat_client.autoLogout

    def test_clean_up(self):
        test_icat_client = ICATClient()
        assert id(test_icat_client) in Client.Register
        test_icat_client.clean_up()
        assert id(test_icat_client) not in Client.Register
