import pytest

from datagateway_api.src.common.exceptions import SearchAPIError
from datagateway_api.src.search_api.panosc_mappings import PaNOSCMappings


class TestPaNOSCMappings:
    def test_valid_load_mappings(self, test_panosc_mappings):
        test_mappings = PaNOSCMappings()
        assert test_mappings.mappings == test_panosc_mappings.mappings

    @pytest.mark.parametrize(
        "test_panosc_entity_name, test_panosc_related_field_name, expected_entity_name",
        [
            pytest.param("Dataset", "files", "File", id="Dataset.files"),
            pytest.param(
                "Document", "parameters", "Parameter", id="Document.parameters",
            ),
            pytest.param("Person", "members", "Member", id="Person.members"),
        ],
    )
    def test_valid_get_panosc_related_entity_name(
        self,
        test_panosc_mappings,
        test_panosc_entity_name,
        test_panosc_related_field_name,
        expected_entity_name,
    ):
        test_related_name = test_panosc_mappings.get_panosc_related_entity_name(
            test_panosc_entity_name, test_panosc_related_field_name,
        )
        assert test_related_name == expected_entity_name

    def test_invalid_get_panosc_related_entity_name(self, test_panosc_mappings):
        with pytest.raises(SearchAPIError):
            test_panosc_mappings.get_panosc_related_entity_name(
                "UnknownField", "unknownField",
            )
