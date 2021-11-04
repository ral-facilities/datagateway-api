from datetime import datetime
import uuid

import pytest

from datagateway_api.common.constants import Constants
from datagateway_api.common.datagateway_api.database.helpers import (
    delete_row_by_id,
    insert_row_into_table,
)
from datagateway_api.common.datagateway_api.database.models import (
    FACILITYCYCLE,
    INSTRUMENT,
    INVESTIGATION,
    INVESTIGATIONINSTRUMENT,
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

    delete_row_by_id(INVESTIGATION, investigation.id)


@pytest.fixture()
def multiple_investigation_test_data_db():
    investigations = create_investigation_db_data(num_entities=5)

    yield investigations

    for investigation in investigations:
        delete_row_by_id(INVESTIGATION, investigation.id)


@pytest.fixture()
def isis_specific_endpoint_data_db():
    facility_cycle = FACILITYCYCLE()
    facility_cycle.name = "Test cycle for DG API testing (DB)"
    facility_cycle.startDate = datetime(
        year=2020, month=1, day=1, hour=1, minute=1, second=1,
    )
    facility_cycle.endDate = datetime(
        year=2020, month=2, day=1, hour=1, minute=1, second=1,
    )
    facility_cycle.facilityID = 1
    set_meta_attributes(facility_cycle)
    insert_row_into_table(FACILITYCYCLE, facility_cycle)

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

    yield (instrument.id, facility_cycle, investigation)

    delete_row_by_id(INVESTIGATIONINSTRUMENT, investigation_instrument.id)
    delete_row_by_id(FACILITYCYCLE, facility_cycle.id)
    delete_row_by_id(INVESTIGATION, investigation.id)
    delete_row_by_id(INSTRUMENT, instrument.id)


@pytest.fixture()
def final_instrument_id(flask_test_app_db, valid_db_credentials_header):
    final_instrument_result = flask_test_app_db.get(
        '/instruments/findone?order="id DESC"', headers=valid_db_credentials_header,
    )
    return final_instrument_result.json["id"]


@pytest.fixture()
def final_facilitycycle_id(flask_test_app_db, valid_db_credentials_header):
    final_facilitycycle_result = flask_test_app_db.get(
        '/facilitycycles/findone?order="id DESC"', headers=valid_db_credentials_header,
    )
    return final_facilitycycle_result.json["id"]
