from datetime import datetime
import json
import uuid

from dateutil.tz import tzlocal
from icat.exception import ICATNoObjectError
import pytest

from test.integration.datagateway_api.icat.endpoints.test_create_icat import (
    TestICATCreateData,
)
from test.integration.datagateway_api.icat.test_query import (
    prepare_icat_data_for_assertion,
)


@pytest.fixture()
def valid_icat_credentials_header(icat_client):
    return {"Authorization": f"Bearer {icat_client.sessionId}"}


def create_investigation_test_data(client, num_entities=1):
    test_data = []

    for i in range(num_entities):
        investigation = client.new("investigation")
        investigation.name = f"Test Data for DataGateway API Testing {i}"
        investigation.title = f"Test data for Python ICAT on DataGateway API {i}"
        investigation.startDate = datetime(
            year=2020,
            month=1,
            day=4,
            hour=1,
            minute=1,
            second=1,
            tzinfo=tzlocal(),
        )
        investigation.endDate = datetime(
            year=2020,
            month=1,
            day=8,
            hour=1,
            minute=1,
            second=1,
            tzinfo=tzlocal(),
        )
        investigation.fileSize = 1073741824
        investigation.fileCount = 3
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
def final_instrument_id(test_client, valid_icat_credentials_header):
    final_instrument_result = test_client.get(
        '/instruments/findone?order="id DESC"',
        headers=valid_icat_credentials_header,
    )
    return final_instrument_result.json["id"]


@pytest.fixture()
def final_facilitycycle_id(test_client, valid_icat_credentials_header):
    final_facilitycycle_result = test_client.get(
        '/facilitycycles/findone?order="id DESC"',
        headers=valid_icat_credentials_header,
    )
    return final_facilitycycle_result.json["id"]


@pytest.fixture()
def remove_test_created_investigation_data(
    test_client,
    valid_icat_credentials_header,
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

    where = {"name": {"like": TestICATCreateData.investigation_name_prefix}}

    created_test_data = test_client.get(
        f"/investigations?where={json.dumps(where)}",
        headers=valid_icat_credentials_header,
    )
    investigation_ids = []
    for investigation in created_test_data.json():
        investigation_ids.append(investigation["id"])

    for investigation_id in investigation_ids:
        test_client.delete(
            f"/investigations/{investigation_id}",
            headers=valid_icat_credentials_header,
        )
