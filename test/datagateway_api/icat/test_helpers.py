from unittest.mock import patch

from icat.exception import ICATInternalError
import pytest

from datagateway_api.common.datagateway_api.icat.helpers import (
    get_icat_entity_name_as_camel_case,
    push_data_updates_to_icat,
)
from datagateway_api.common.exceptions import BadRequestError, PythonICATError


class TestICATHelpers:
    """Testing the helper functions which aren't covered in the endpoint tests"""

    @pytest.mark.parametrize(
        "input_entity_name, expected_entity_name",
        [
            pytest.param("User", "user", id="singular single word entity name"),
            pytest.param(
                "PublicStep", "publicStep", id="singular two word entity name",
            ),
            pytest.param(
                "PermissibleStringValue",
                "permissibleStringValue",
                id="singular multi-word entity name",
            ),
        ],
    )
    def test_valid_get_icat_entity_name_as_camel_case(
        self, icat_client, input_entity_name, expected_entity_name,
    ):
        camel_case_entity_name = get_icat_entity_name_as_camel_case(
            icat_client, input_entity_name,
        )
        assert camel_case_entity_name == expected_entity_name

    def test_invalid_get_icat_entity_name_as_camel_case(self, icat_client):
        with pytest.raises(BadRequestError):
            get_icat_entity_name_as_camel_case(icat_client, "UnknownEntityName")

    def test_invalid_update_pushes(self, icat_client):
        with patch(
            "icat.entity.Entity.update",
            side_effect=ICATInternalError("Mocked Exception"),
        ):
            inv_entity = icat_client.new("investigation", name="Investigation A")
            with pytest.raises(PythonICATError):
                push_data_updates_to_icat(inv_entity)
