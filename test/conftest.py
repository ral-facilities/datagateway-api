from datetime import datetime, timedelta

from flask import Flask
import pytest

from datagateway_api.common.database.helpers import (
    delete_row_by_id,
    insert_row_into_table,
)
from datagateway_api.common.database.models import SESSION
from datagateway_api.src.api_start_utils import (
    create_api_endpoints,
    create_app_infrastructure,
)


@pytest.fixture()
def bad_credentials_header():
    return {"Authorization": "Bearer Invalid"}


@pytest.fixture()
def invalid_credentials_header():
    return {"Authorization": "Test"}


@pytest.fixture(scope="package")
def flask_test_app():
    """This is used to check the endpoints exist and have the correct HTTP methods"""
    test_app = Flask(__name__)
    api, spec = create_app_infrastructure(test_app)
    create_api_endpoints(test_app, api, spec)

    yield test_app


@pytest.fixture(scope="package")
def flask_test_app_db():
    """
    This is in the common conftest file because this test app is also used in
    non-backend specific tests
    """
    db_app = Flask(__name__)
    db_app.config["TESTING"] = True
    db_app.config["TEST_BACKEND"] = "db"

    api, spec = create_app_infrastructure(db_app)
    create_api_endpoints(db_app, api, spec)
    db_app.app_context().push()

    yield db_app.test_client()


@pytest.fixture()
def valid_db_credentials_header():
    session = SESSION()
    session.ID = "Test"
    session.EXPIREDATETIME = datetime.now() + timedelta(hours=1)
    session.username = "Test User"

    insert_row_into_table(SESSION, session)

    yield {"Authorization": f"Bearer {session.ID}"}

    delete_row_by_id(SESSION, "Test")
