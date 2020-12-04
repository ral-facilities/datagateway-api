from datetime import datetime, timedelta
import uuid

from flask import Flask
import pytest

from datagateway_api.common.database.helpers import (
    delete_row_by_id,
    insert_row_into_table,
)
from datagateway_api.common.database.models import INVESTIGATION, SESSION
from datagateway_api.src.main import create_api_endpoints, create_app_infrastructure


@pytest.fixture()
def single_investigation_test_data_db():
    investigation = INVESTIGATION()
    investigation.NAME = "Test Data for DataGateway API Testing (DB)"
    investigation.TITLE = "Title for DataGateway API Testing (DB)"
    investigation.STARTDATE = datetime(
        year=2020, month=1, day=4, hour=1, minute=1, second=1,
    )
    investigation.ENDDATE = datetime(
        year=2020, month=1, day=8, hour=1, minute=1, second=1,
    )
    investigation.VISIT_ID = str(uuid.uuid1())
    investigation.FACILITY_ID = 1
    investigation.TYPE_ID = 1

    investigation.CREATE_TIME = datetime(2000, 1, 1)
    investigation.MOD_TIME = datetime(2000, 1, 1)
    investigation.CREATE_ID = "test create id"
    investigation.MOD_ID = "test mod id"

    insert_row_into_table(INVESTIGATION, investigation)

    yield investigation

    delete_row_by_id(INVESTIGATION, investigation.ID)
