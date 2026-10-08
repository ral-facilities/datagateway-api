from typing import Any
from unittest.mock import patch

from icat.client import Client
from icat.exception import ICATInternalError
import pytest

from datagateway_api.common.exceptions import BadRequestError, PythonICATError
from datagateway_api.datagateway_api.icat.helpers import create_entities, push_data_updates_to_icat, update_attributes


class TestICATHelpers:
    """Testing the helper functions which aren't covered in the endpoint tests"""

    def test_invalid_update_pushes(self, icat_client):
        with patch(
            "icat.entity.Entity.update",
            side_effect=ICATInternalError("Mocked Exception"),
        ):
            inv_entity = icat_client.new("investigation", name="Investigation A")
            with pytest.raises(PythonICATError):
                push_data_updates_to_icat(inv_entity)

    def test_update_attributes(self, icat_client: Client) -> None:
        with pytest.raises(
            expected_exception=BadRequestError,
            match="Bad request made, cannot find attribute `key` within the Investigation entity",
        ):
            update_attributes(old_entity=icat_client.new("Investigation"), new_entity={"key": "value"})

    @pytest.mark.parametrize(
        ["data", "match"],
        [
            pytest.param(
                {"facility": [999999999]},
                r"Facility\[id:999999999\] not found\.",
                id="ICATNoObjectError handling",
            ),
            pytest.param({"unknown": ""}, r"Unknown attribute name 'unknown'\.", id="ValueError handling"),
        ],
    )
    def test_create_entities(self, icat_client: Client, data: dict[str, Any], match: str) -> None:
        with pytest.raises(expected_exception=BadRequestError, match=match):
            create_entities(client=icat_client, entity_type="Investigation", data=data)

    def test_create_entities_internal_error(self, icat_client: Client) -> None:
        with (
            pytest.raises(expected_exception=PythonICATError, match="Test"),
            patch.object(icat_client, "create", side_effect=ICATInternalError("Test")),
        ):
            create_entities(client=icat_client, entity_type="Investigation", data={})
