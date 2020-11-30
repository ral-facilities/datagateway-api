from datetime import datetime
import uuid

from icat.client import Client
from icat.exception import ICATNoObjectError
from icat.query import Query
import pytest

from datagateway_api.common.config import config
from datagateway_api.src.main import app
from test.icat.test_query import prepare_icat_data_for_assertion


@pytest.fixture(scope="package")
def icat_client():
    client = Client(config.get_icat_url(), checkCert=config.get_icat_check_cert())
    client.login(config.get_test_mechanism(), config.get_test_user_credentials())
    return client


@pytest.fixture()
def valid_credentials_header(icat_client):
    return {"Authorization": f"Bearer {icat_client.sessionId}"}


@pytest.fixture()
def invalid_credentials_header():
    return {"Authorization": "Bearer Invalid"}


@pytest.fixture()
def icat_query(icat_client):
    return Query(icat_client, "Investigation")


def create_investigation_test_data(client, num_entities=1):
    test_data = []

    for i in range(num_entities):
        investigation = client.new("investigation")
        investigation.name = f"Test Data for DataGateway API Testing {i}"
        investigation.title = (
            f"Test data for the Python ICAT Backend on DataGateway API {i}"
        )
        investigation.startDate = datetime(
            year=2020, month=1, day=4, hour=1, minute=1, second=1,
        )
        investigation.endDate = datetime(
            year=2020, month=1, day=8, hour=1, minute=1, second=1,
        )
        # UUID visit ID means uniquesness constraint should always be met
        investigation.visitId = str(uuid.uuid1())
        investigation.facility = client.get("Facility", 1)
        investigation.type = client.get("InvestigationType", 1)
        investigation.create()

        test_data.append(investigation)

    if len(test_data) == 1:
        return test_data[0]
    else:
        return test_data


@pytest.fixture()
def single_investigation_test_data(icat_client):
    investigation = create_investigation_test_data(icat_client)
    investigation_dict = prepare_icat_data_for_assertion([investigation])

    yield investigation_dict

    # Remove data from ICAT
    try:
        icat_client.delete(investigation)
    except ICATNoObjectError as e:
        # This should occur on DELETE endpoints, normal behaviour for those tests
        print(e)


@pytest.fixture()
def multiple_investigation_test_data(icat_client):
    investigation_dicts = []
    investigations = create_investigation_test_data(icat_client, num_entities=5)
    investigation_dicts = prepare_icat_data_for_assertion(investigations)

    yield investigation_dicts

    for investigation in investigations:
        icat_client.delete(investigation)


@pytest.fixture()
def flask_test_app():
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture()
def isis_specific_endpoint_data(icat_client):
    facility_cycle = icat_client.new("facilityCycle")
    facility_cycle.name = "Test cycle for DataGateway API testing"
    facility_cycle.startDate = datetime(
        year=2020, month=1, day=1, hour=1, minute=1, second=1,
    )
    facility_cycle.endDate = datetime(
        year=2020, month=2, day=1, hour=1, minute=1, second=1,
    )
    facility_cycle.facility = icat_client.get("Facility", 1)
    facility_cycle.create()

    investigation = create_investigation_test_data(icat_client)
    investigation_dict = prepare_icat_data_for_assertion([investigation])

    instrument = icat_client.new("instrument")
    instrument.name = "Test Instrument for DataGateway API Endpoint Testing"
    instrument.facility = icat_client.get("Facility", 1)
    instrument.create()

    investigation_instrument = icat_client.new("investigationInstrument")
    investigation_instrument.investigation = investigation
    investigation_instrument.instrument = instrument
    investigation_instrument.create()

    facility_cycle_dict = prepare_icat_data_for_assertion([facility_cycle])

    yield (instrument.id, facility_cycle_dict, facility_cycle.id, investigation_dict)

    try:
        # investigation_instrument removed when deleting the objects its related objects
        icat_client.delete(facility_cycle)
        icat_client.delete(investigation)
        icat_client.delete(instrument)
    except ICATNoObjectError as e:
        print(e)
