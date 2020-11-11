from icat.client import Client
from icat.query import Query
import pytest

from datagateway_api.common.config import config


@pytest.fixture(scope="package")
def icat_client():
    client = Client(config.get_icat_url(), checkCert=config.get_icat_check_cert())
    client.login(config.get_test_mechanism(), config.get_test_user_credentials())
    print(f"ID: {client.sessionId}")
    return client


@pytest.fixture()
def icat_query(icat_client):
    query = Query(icat_client, "Investigation")

    return query
