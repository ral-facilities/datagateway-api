import pytest

from datagateway_api.common.exceptions import BadRequestError
from datagateway_api.common.icat.helpers import get_icat_entity_name_as_camel_case


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
