from datetime import datetime
import uuid

import pytest

from datagateway_api.common.database.helpers import (
    delete_row_by_id,
    insert_row_into_table,
)
from datagateway_api.common.database.models import (
    FACILITYCYCLE,
    INSTRUMENT,
    INVESTIGATION,
    INVESTIGATIONINSTRUMENT,
)


def set_meta_attributes(entity):
    db_meta_attributes = {
        "CREATE_TIME": datetime(2000, 1, 1),
        "MOD_TIME": datetime(2000, 1, 1),
        "CREATE_ID": "test create id",
        "MOD_ID": "test mod id",
    }

    for attr, value in db_meta_attributes.items():
        setattr(entity, attr, value)


def create_investigation_db_data(num_entities=1):
    test_data = []

    for i in range(num_entities):
        investigation = INVESTIGATION()
        investigation.NAME = f"Test Data for DataGateway API Testing (DB) {i}"
        investigation.TITLE = f"Title for DataGateway API Testing (DB) {i}"
        investigation.STARTDATE = datetime(
            year=2020, month=1, day=4, hour=1, minute=1, second=1,
        )
        investigation.ENDDATE = datetime(
            year=2020, month=1, day=8, hour=1, minute=1, second=1,
        )
        investigation.VISIT_ID = str(uuid.uuid1())
        investigation.FACILITY_ID = 1
        investigation.TYPE_ID = 1

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

    delete_row_by_id(INVESTIGATION, investigation.ID)


@pytest.fixture()
def multiple_investigation_test_data_db():
    investigations = create_investigation_db_data(num_entities=5)

    yield investigations

    for investigation in investigations:
        delete_row_by_id(INVESTIGATION, investigation.ID)


@pytest.fixture()
def isis_specific_endpoint_data_db():
    facility_cycle = FACILITYCYCLE()
    facility_cycle.NAME = "Test cycle for DG API testing (DB)"
    facility_cycle.STARTDATE = datetime(
        year=2020, month=1, day=1, hour=1, minute=1, second=1,
    )
    facility_cycle.ENDDATE = datetime(
        year=2020, month=2, day=1, hour=1, minute=1, second=1,
    )
    facility_cycle.FACILITY_ID = 1
    set_meta_attributes(facility_cycle)

    investigation = create_investigation_db_data()

    instrument = INSTRUMENT()
    instrument.NAME = "Test Instrument for DataGateway API Endpoint Testing (DB)"
    instrument.FACILITY_ID = 1
    set_meta_attributes(instrument)

    insert_row_into_table(INSTRUMENT, instrument)

    investigation_instrument = INVESTIGATIONINSTRUMENT()
    investigation_instrument.INVESTIGATION_ID = investigation.ID
    investigation_instrument.INSTRUMENT_ID = instrument.ID
    set_meta_attributes(investigation_instrument)

    insert_row_into_table(INVESTIGATIONINSTRUMENT, investigation_instrument)

    yield (instrument.ID, facility_cycle, investigation)

    delete_row_by_id(FACILITYCYCLE, facility_cycle.ID)
    delete_row_by_id(INVESTIGATION, investigation.ID)
    delete_row_by_id(INSTRUMENT, instrument.ID)
