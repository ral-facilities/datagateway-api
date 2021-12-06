from icat.client import Client
from icat.query import Query
import pytest

from datagateway_api.src.common.config import Config


@pytest.fixture(scope="package")
def icat_client():
    client = Client(
        Config.config.search_api.icat_url,
        checkCert=Config.config.search_api.icat_check_cert,
    )
    client.login(
        Config.config.test_mechanism, Config.config.test_user_credentials.dict(),
    )
    return client


@pytest.fixture()
def icat_query(icat_client):
    return Query(icat_client, "Investigation")
