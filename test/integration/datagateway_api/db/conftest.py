from datetime import datetime
import uuid

import pytest

from datagateway_api.src.common.config import Config
from datagateway_api.src.common.constants import Constants
from datagateway_api.src.common.exceptions import MissingRecordError
from datagateway_api.src.datagateway_api.database.helpers import (
    delete_row_by_id,
    insert_row_into_table,
)
from datagateway_api.src.datagateway_api.database.models import (
    INSTRUMENT,
    INVESTIGATION,
    INVESTIGATIONINSTRUMENT,
)
from test.integration.datagateway_api.db.endpoints.test_create_db import (
    TestDBCreateData,
)


def set_meta_attributes(entity):
    db_meta_attributes = {
        "createTime": Constants.TEST_MOD_CREATE_DATETIME,
        "modTime": Constants.TEST_MOD_CREATE_DATETIME,
        "createId": "test create id",
        "modId": "test mod id",
    }

    for attr, value in db_meta_attributes.items():
        setattr(entity, attr, value)


def create_investigation_db_data(num_entities=1):
    test_data = []

    for i in range(num_entities):
        investigation = INVESTIGATION()
        investigation.name = f"Test Data for DataGateway API Testing (DB) {i}"
        investigation.title = f"Title for DataGateway API Testing (DB) {i}"
        investigation.startDate = datetime(
            year=2020, month=1, day=4, hour=1, minute=1, second=1,
        )
        investigation.endDate = datetime(
            year=2020, month=1, day=8, hour=1, minute=1, second=1,
        )
        investigation.visitId = str(uuid.uuid1())
        investigation.facilityID = 1
        investigation.typeID = 1
        investigation.fileSize = 1073741824
        investigation.fileCount = 3

        set_meta_attributes(investigation)

        insert_row_into_table(INVESTIGATION, investigation)

        test_data.append(investigation)

    if len(test_data) == 1:
        return test_data[0]
    else:
        return test_data


@pytest.fixture()
def single_investigation_test_data_db():
    investigation = create_investigation_db_data()

    yield investigation
    try:
        delete_row_by_id(INVESTIGATION, investigation.id)
    except MissingRecordError as e:
        # This should occur on DELETE endpoints, normal behaviour for those tests
        print(e)


@pytest.fixture()
def multiple_investigation_test_data_db():
    investigations = create_investigation_db_data(num_entities=5)

    yield investigations

    for investigation in investigations:
        delete_row_by_id(INVESTIGATION, investigation.id)


@pytest.fixture()
def related_distinct_data_db():
    investigation = create_investigation_db_data()

    instrument = INSTRUMENT()
    instrument.name = "Test Instrument for DataGateway API Endpoint Testing (DB)"
    instrument.facilityID = 1
    set_meta_attributes(instrument)
    insert_row_into_table(INSTRUMENT, instrument)

    investigation_instrument = INVESTIGATIONINSTRUMENT()
    investigation_instrument.investigationID = investigation.id
    investigation_instrument.instrumentID = instrument.id
    set_meta_attributes(investigation_instrument)

    insert_row_into_table(INVESTIGATIONINSTRUMENT, investigation_instrument)

    yield (instrument.id, investigation)

    delete_row_by_id(INVESTIGATIONINSTRUMENT, investigation_instrument.id)
    delete_row_by_id(INVESTIGATION, investigation.id)
    delete_row_by_id(INSTRUMENT, instrument.id)


@pytest.fixture()
def final_instrument_id(flask_test_app_db, valid_db_credentials_header):
    final_instrument_result = flask_test_app_db.get(
        f"{Config.config.datagateway_api.extension}/instruments/findone"
        '?order="id DESC"',
        headers=valid_db_credentials_header,
    )
    return final_instrument_result.json["id"]


@pytest.fixture()
def final_facilitycycle_id(flask_test_app_db, valid_db_credentials_header):
    final_facilitycycle_result = flask_test_app_db.get(
        f"{Config.config.datagateway_api.extension}/facilitycycles/findone"
        '?order="id DESC"',
        headers=valid_db_credentials_header,
    )
    return final_facilitycycle_result.json["id"]


@pytest.fixture()
def remove_test_created_investigation_data(
    flask_test_app_db, valid_db_credentials_header,
):
    yield

    created_test_data = flask_test_app_db.get(
        f"{Config.config.datagateway_api.extension}/investigations?where="
        '{"name":{"like":'
        f'"{TestDBCreateData.investigation_name_prefix}"'
        "}}",
        headers=valid_db_credentials_header,
    )

    investigation_ids = []

    for investigation in created_test_data.json:
        investigation_ids.append(investigation["id"])

    for investigation_id in investigation_ids:
        flask_test_app_db.delete(
            f"{Config.config.datagateway_api.extension}/investigations"
            f"/{investigation_id}",
            headers=valid_db_credentials_header,
        )
