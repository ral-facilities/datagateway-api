import pytest

from datagateway_api.common.database.filters import DatabaseFilterUtilities
from datagateway_api.common.database.helpers import ReadQuery
from datagateway_api.common.exceptions import FilterError
from datagateway_api.common.helpers import get_entity_object_from_name


class TestDatabaseFilterUtilities:
    @pytest.mark.parametrize(
        "input_field, expected_fields",
        [
            pytest.param("name", ("name", None, None), id="Unrelated field"),
            pytest.param(
                "facility.daysUntilRelease",
                ("facility", "daysUntilRelease", None),
                id="Related field matching ICAT schema name",
            ),
            pytest.param(
                "FACILITY.daysUntilRelease",
                ("FACILITY", "daysUntilRelease", None),
                id="Related field matching database format (uppercase)",
            ),
            pytest.param(
                "user.investigationUsers.role",
                ("user", "investigationUsers", "role"),
                id="Related related field (2 levels deep)",
            ),
        ],
    )
    def test_valid_extract_filter_fields(self, input_field, expected_fields):
        test_utility = DatabaseFilterUtilities()
        test_utility._extract_filter_fields(input_field)

        assert test_utility.field == expected_fields[0]
        assert test_utility.related_field == expected_fields[1]
        assert test_utility.related_related_field == expected_fields[2]

    def test_invalid_extract_filter_fields(self):
        test_utility = DatabaseFilterUtilities()

        with pytest.raises(ValueError):
            test_utility._extract_filter_fields(
                "user.investigationUsers.investigation.summary",
            )

    @pytest.mark.parametrize(
        "input_field",
        [
            pytest.param("name", id="No related fields"),
            pytest.param("facility.daysUntilRelease", id="Related field"),
            pytest.param(
                "investigationUsers.user.fullName", id="Related related field",
            ),
        ],
    )
    def test_valid_add_query_join(
        self, flask_test_app_db, input_field,
    ):
        table = get_entity_object_from_name("Investigation")

        test_utility = DatabaseFilterUtilities()
        test_utility._extract_filter_fields(input_field)

        expected_query = ReadQuery(table)
        if test_utility.related_related_field:
            expected_table = get_entity_object_from_name(test_utility.related_field)

            included_table = get_entity_object_from_name(test_utility.field)
            expected_query.base_query = expected_query.base_query.join(
                included_table,
            ).join(expected_table)
        elif test_utility.related_field:
            expected_table = get_entity_object_from_name(test_utility.field)

            expected_query = ReadQuery(table)
            expected_query.base_query = expected_query.base_query.join(expected_table)
        else:
            expected_table = table

        with ReadQuery(table) as test_query:
            test_utility._add_query_join(test_query)

        # Check the JOIN has been applied
        assert str(test_query.base_query) == str(expected_query.base_query)

    @pytest.mark.parametrize(
        "input_field",
        [
            pytest.param("name", id="No related fields"),
            pytest.param("facility.daysUntilRelease", id="Related field"),
            pytest.param(
                "investigationUsers.user.fullName", id="Related related field",
            ),
        ],
    )
    def test_valid_get_entity_model_for_filter(self, input_field):
        table = get_entity_object_from_name("Investigation")

        test_utility = DatabaseFilterUtilities()
        test_utility._extract_filter_fields(input_field)

        if test_utility.related_related_field:
            expected_table = get_entity_object_from_name(test_utility.related_field)
        elif test_utility.related_field:
            expected_table = get_entity_object_from_name(test_utility.field)
        else:
            expected_table = table

        with ReadQuery(table) as test_query:
            output_field = test_utility._get_entity_model_for_filter(test_query)

        # Check the output is correct
        field_name_to_fetch = input_field.split(".")[-1]
        assert output_field == getattr(expected_table, field_name_to_fetch)

    def test_valid_get_field(self, flask_test_app_db):
        table = get_entity_object_from_name("Investigation")

        test_utility = DatabaseFilterUtilities()
        field = test_utility._get_field(table, "name")

        assert field == table.name

    def test_invalid_get_field(self, flask_test_app_db):
        table = get_entity_object_from_name("Investigation")

        test_utility = DatabaseFilterUtilities()
        with pytest.raises(FilterError):
            test_utility._get_field(table, "unknown")
