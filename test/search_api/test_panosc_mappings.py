import pytest

from datagateway_api.src.common.exceptions import FilterError, SearchAPIError
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

    @pytest.mark.parametrize(
        "test_panosc_entity_name, expected_non_related_field_names",
        [
            pytest.param(
                "Affiliation",
                ["id", "name", "address", "city", "country"],
                id="Affiliation",
            ),
            pytest.param(
                "Dataset",
                ["pid", "title", "isPublic", "creationDate", "size"],
                id="Dataset",
            ),
            pytest.param(
                "Document",
                [
                    "pid",
                    "isPublic",
                    "type",
                    "title",
                    "summary",
                    "doi",
                    "startDate",
                    "endDate",
                    "releaseDate",
                    "license",
                    "keywords",
                ],
                id="Document",
            ),
            pytest.param("File", ["id", "name", "path", "size"], id="File"),
            pytest.param("Instrument", ["pid", "name", "facility"], id="Instrument"),
            pytest.param("Member", ["id", "role"], id="Member"),
            pytest.param("Parameter", ["id", "name", "value", "unit"], id="Parameter"),
            pytest.param(
                "Person",
                ["id", "fullName", "orcid", "researcherId", "firstName", "lastName"],
                id="Person",
            ),
            pytest.param("Sample", ["name", "pid", "description"], id="Sample"),
            pytest.param("Technique", ["pid", "name"], id="Technique"),
        ],
    )
    def test_valid_get_panosc_non_related_field_names(
        self,
        test_panosc_mappings,
        test_panosc_entity_name,
        expected_non_related_field_names,
    ):
        non_related_field_names = test_panosc_mappings.get_panosc_non_related_field_names(  # noqa: B950
            test_panosc_entity_name,
        )
        assert non_related_field_names == expected_non_related_field_names

    def test_invalid_get_panosc_non_related_field_names(
        self, test_panosc_mappings,
    ):
        with pytest.raises(FilterError):
            test_panosc_mappings.get_panosc_non_related_field_names("UnknownEntity")
