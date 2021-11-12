from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from datagateway_api.src.common.constants import Constants
from datagateway_api.src.common.exceptions import DatabaseError
from datagateway_api.src.datagateway_api.backends import create_backend


class TestICATPing:
    def test_valid_ping(self, flask_test_app_db):
        test_response = flask_test_app_db.get("/ping")

        assert test_response.json == Constants.PING_OK_RESPONSE

    def test_invalid_ping(self):
        with patch(
            "sqlalchemy.engine.reflection.Inspector.get_table_names",
            side_effect=SQLAlchemyError("Mocked Exception"),
        ):
            with pytest.raises(DatabaseError):
                backend = create_backend("db")
                backend.ping()
