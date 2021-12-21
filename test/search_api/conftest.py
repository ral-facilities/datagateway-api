from icat.client import Client
from icat.query import Query
import pytest

from datagateway_api.src.common.config import Config
from datagateway_api.src.search_api.query import SearchAPIQuery


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
def search_api_query_dataset():
    return SearchAPIQuery("Dataset")


@pytest.fixture()
def search_api_query_document():
    return SearchAPIQuery("Document")


@pytest.fixture()
def search_api_query_instrument():
    return SearchAPIQuery("Instrument")
