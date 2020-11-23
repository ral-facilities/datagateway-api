import uuid

from icat.client import Client
from icat.entity import Entity
from icat.query import Query
import pytest

from datagateway_api.common.config import config


@pytest.fixture(scope="package")
def icat_client():
    client = Client(config.get_icat_url(), checkCert=config.get_icat_check_cert())
    client.login(config.get_test_mechanism(), config.get_test_user_credentials())
    return client


@pytest.fixture()
def valid_credentials_header(icat_client):
    return {"Authorization": f"Bearer {icat_client.sessionId}"}


@pytest.fixture()
def icat_query(icat_client):
    query = Query(icat_client, "Investigation")

    return query


@pytest.fixture()
def single_investigation_test_data(icat_client):
    # Inject data
    investigation = icat_client.new("investigation")
    investigation.name = "Test Data for DataGateway API Testing"
    investigation.title = "Test data for the Python ICAT Backend on DataGateway API"
    # UUID visit ID means uniquesness constraint should always be met
    investigation.visitId = str(uuid.uuid1())
    investigation.facility = icat_client.get("Facility", 1)
    investigation.type = icat_client.get("InvestigationType", 1)
    investigation.create()
    investigation_dict = investigation.as_dict()

    meta_attributes = Entity.MetaAttr
    for attr in meta_attributes:
        investigation_dict.pop(attr)

    yield [investigation_dict]

    # Remove data from ICAT
    icat_client.delete(investigation)


@pytest.fixture()
def remove_single_investiation_result():
    pass
