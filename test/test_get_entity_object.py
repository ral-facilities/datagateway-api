import pytest

from datagateway_api.src.datagateway_api.database.models import (
    FACILITY,
    INVESTIGATION,
    JOB,
)
from datagateway_api.src.common.exceptions import ApiError
from datagateway_api.src.common.helpers import get_entity_object_from_name


class TestGetEntityObject:
    @pytest.mark.parametrize(
        "entity_name, expected_object_type",
        [
            pytest.param(
                "investigation", type(INVESTIGATION), id="singular entity name",
            ),
            pytest.param("jobs", type(JOB), id="plural entity name, 's' added"),
            pytest.param(
                "facilities", type(FACILITY), id="plural entity name, 'y' to 'ies'",
            ),
        ],
    )
    def test_valid_get_entity_object_from_name(self, entity_name, expected_object_type):
        database_entity = get_entity_object_from_name(entity_name)

        assert type(database_entity) == expected_object_type

    def test_invalid_get_entity_object_from_name(self):
        with pytest.raises(ApiError):
            get_entity_object_from_name("Application1234s")
