from datetime import datetime
import uuid

from dateutil.tz import tzlocal
from flask import Flask
from icat.client import Client
from icat.exception import ICATNoObjectError
from icat.query import Query
import pytest

from datagateway_api.common.config import config
from datagateway_api.src.api_start_utils import (
    create_api_endpoints,
    create_app_infrastructure,
)
from test.datagateway_api.icat.endpoints.test_create_icat import TestICATCreateData
from test.datagateway_api.icat.test_query import prepare_icat_data_for_assertion


@pytest.fixture(scope="package")
def icat_client():
    client = Client(
        config.datagateway_api.icat_url,
        checkCert=config.datagateway_api.icat_check_cert,
    )
    client.login(
        config.test_mechanism, config.test_user_credentials.dict(),
    )
    return client


@pytest.fixture()
def valid_icat_credentials_header(icat_client):
    return {"Authorization": f"Bearer {icat_client.sessionId}"}


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
            year=2020, month=1, day=4, hour=1, minute=1, second=1, tzinfo=tzlocal(),
        )
        investigation.endDate = datetime(
            year=2020, month=1, day=8, hour=1, minute=1, second=1, tzinfo=tzlocal(),
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


@pytest.fixture(scope="package")
def flask_test_app_icat(flask_test_app):
    icat_app = Flask(__name__)
    icat_app.config["TESTING"] = True
    icat_app.config["TEST_BACKEND"] = "python_icat"

    api, spec = create_app_infrastructure(icat_app)
    create_api_endpoints(icat_app, api, spec)

    yield icat_app.test_client()


@pytest.fixture()
def isis_specific_endpoint_data(icat_client):
    facility_cycle = icat_client.new("facilityCycle")
    facility_cycle.name = "Test cycle for DataGateway API testing"
    facility_cycle.startDate = datetime(
        year=2020, month=1, day=1, hour=1, minute=1, second=1, tzinfo=tzlocal(),
    )
    facility_cycle.endDate = datetime(
        year=2020, month=2, day=1, hour=1, minute=1, second=1, tzinfo=tzlocal(),
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


@pytest.fixture()
def final_instrument_id(flask_test_app_icat, valid_icat_credentials_header):
    final_instrument_result = flask_test_app_icat.get(
        '/instruments/findone?order="id DESC"', headers=valid_icat_credentials_header,
    )
    return final_instrument_result.json["id"]


@pytest.fixture()
def final_facilitycycle_id(flask_test_app_icat, valid_icat_credentials_header):
    final_facilitycycle_result = flask_test_app_icat.get(
        '/facilitycycles/findone?order="id DESC"',
        headers=valid_icat_credentials_header,
    )
    return final_facilitycycle_result.json["id"]


@pytest.fixture()
def remove_test_created_investigation_data(
    flask_test_app_icat, valid_icat_credentials_header,
):
    """
    This is used to delete the data created inside `test_valid` test functions in
    TestICATCreateData

    This is done by fetching the data which has been created in
    those functions (by using the investigation name prefix, as defined in the test
    class), extracting the IDs from the results, and iterating over those to perform
    DELETE by ID requests
    """

    yield

    created_test_data = flask_test_app_icat.get(
        '/investigations?where={"name":{"like":'
        f'"{TestICATCreateData.investigation_name_prefix}"'
        "}}",
        headers=valid_icat_credentials_header,
    )

    investigation_ids = []
    for investigation in created_test_data.json:
        investigation_ids.append(investigation["id"])

    for investigation_id in investigation_ids:
        flask_test_app_icat.delete(
            f"/investigations/{investigation_id}",
            headers=valid_icat_credentials_header,
        )
