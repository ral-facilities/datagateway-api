import pytest

from datagateway_api.src.common.exceptions import FilterError
from datagateway_api.src.common.helpers import get_entity_object_from_name
from datagateway_api.src.datagateway_api.database.filters import (
    DatabaseFilterUtilities,
    DatabaseWhereFilter,
)
from datagateway_api.src.datagateway_api.database.helpers import ReadQuery
from test.datagateway_api.db.endpoints.test_create_db import (
    prepare_db_data_for_assertion,
)


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
        test_utility.extract_filter_fields(input_field)

        assert test_utility.field == expected_fields[0]
        assert test_utility.related_field == expected_fields[1]
        assert test_utility.related_related_field == expected_fields[2]

    def test_invalid_extract_filter_fields(self):
        test_utility = DatabaseFilterUtilities()

        with pytest.raises(ValueError):
            test_utility.extract_filter_fields(
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
        test_utility.extract_filter_fields(input_field)

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
            test_utility.add_query_join(test_query)

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
        test_utility.extract_filter_fields(input_field)

        if test_utility.related_related_field:
            expected_table = get_entity_object_from_name(test_utility.related_field)
        elif test_utility.related_field:
            expected_table = get_entity_object_from_name(test_utility.field)
        else:
            expected_table = table

        with ReadQuery(table) as test_query:
            output_field = test_utility.get_entity_model_for_filter(test_query)

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

    @pytest.mark.parametrize(
        "operation, value, expected_output",
        [
            pytest.param(
                "eq",
                "Title for DataGateway API Testing (DB) 0",
                {
                    "doi": None,
                    "endDate": "2020-01-08 01:01:01+00:00",
                    "name": "Test Data for DataGateway API Testing (DB) 0",
                    "releaseDate": None,
                    "startDate": "2020-01-04 01:01:01+00:00",
                    "summary": None,
                    "title": "Title for DataGateway API Testing (DB) 0",
                    "facilityID": 1,
                    "typeID": 1,
                    "fileSize": 1073741824,
                    "fileCount": 3,
                },
                id="equal",
            ),
            pytest.param(
                "ne",
                "Title for DataGateway API Testing (DB) 0",
                {
                    "doi": "0-449-78690-0",
                    "endDate": "2000-07-09 00:00:00",
                    "name": "INVESTIGATION 1",
                    "releaseDate": "2000-07-05 00:00:00",
                    "startDate": "2000-04-03 00:00:00",
                    "summary": "Season identify professor happen third."
                    " Beat professional blue clear style have. "
                    "Light final summer.",
                    "title": "Including spend increase ability music"
                    " skill former. Agreement director concern once "
                    "technology sometimes someone staff."
                    "\nSuccess pull bar. Laugh senior example.",
                    "facilityID": 1,
                    "typeID": 2,
                    "fileSize": None,
                    "fileCount": None,
                },
                id="not equal (ne)",
            ),
            pytest.param(
                "like",
                "Title for DataGateway API Testing (DB) 0",
                {
                    "doi": None,
                    "endDate": "2020-01-08 01:01:01+00:00",
                    "name": "Test Data for DataGateway API Testing (DB) 0",
                    "releaseDate": None,
                    "startDate": "2020-01-04 01:01:01+00:00",
                    "summary": None,
                    "title": "Title for DataGateway API Testing (DB) 0",
                    "facilityID": 1,
                    "typeID": 1,
                    "fileSize": 1073741824,
                    "fileCount": 3,
                },
                id="like",
            ),
            pytest.param(
                "nlike",
                "Title for DataGateway API Testing (DB) 0",
                {
                    "doi": "0-449-78690-0",
                    "endDate": "2000-07-09 00:00:00",
                    "name": "INVESTIGATION 1",
                    "releaseDate": "2000-07-05 00:00:00",
                    "startDate": "2000-04-03 00:00:00",
                    "summary": "Season identify professor happen third."
                    " Beat professional blue clear style have. "
                    "Light final summer.",
                    "title": "Including spend increase ability music"
                    " skill former. Agreement director concern once "
                    "technology sometimes someone staff."
                    "\nSuccess pull bar. Laugh senior example.",
                    "facilityID": 1,
                    "typeID": 2,
                    "fileSize": None,
                    "fileCount": None,
                },
                id="not like",
            ),
            pytest.param(
                "lt",
                "Title for DataGateway API Testing (DB) 0",
                {
                    "doi": "0-449-78690-0",
                    "endDate": "2000-07-09 00:00:00",
                    "name": "INVESTIGATION 1",
                    "releaseDate": "2000-07-05 00:00:00",
                    "startDate": "2000-04-03 00:00:00",
                    "summary": "Season identify professor happen third."
                    " Beat professional blue clear style have. "
                    "Light final summer.",
                    "title": "Including spend increase ability music"
                    " skill former. Agreement director concern once "
                    "technology sometimes someone staff."
                    "\nSuccess pull bar. Laugh senior example.",
                    "facilityID": 1,
                    "typeID": 2,
                    "fileSize": None,
                    "fileCount": None,
                },
                id="less than",
            ),
            pytest.param(
                "lte",
                "Title for DataGateway API Testing (DB) 0",
                {
                    "doi": "0-449-78690-0",
                    "endDate": "2000-07-09 00:00:00",
                    "name": "INVESTIGATION 1",
                    "releaseDate": "2000-07-05 00:00:00",
                    "startDate": "2000-04-03 00:00:00",
                    "summary": "Season identify professor happen third."
                    " Beat professional blue clear style have. "
                    "Light final summer.",
                    "title": "Including spend increase ability music"
                    " skill former. Agreement director concern once "
                    "technology sometimes someone staff."
                    "\nSuccess pull bar. Laugh senior example.",
                    "facilityID": 1,
                    "typeID": 2,
                    "fileSize": None,
                    "fileCount": None,
                },
                id="less than or equal",
            ),
            pytest.param(
                "gt",
                "Title for DataGateway API Testing (DB) 0",
                {
                    "doi": "0-9634101-9-9",
                    "endDate": "2001-05-04 00:00:00",
                    "name": "INVESTIGATION 4",
                    "releaseDate": "2001-09-26 00:00:00",
                    "startDate": "2001-02-02 00:00:00",
                    "summary": "Fast purpose right power away health south."
                    "\nQuality serve food buy responsibility go much."
                    " Situation raise manage positive help daughter."
                    " Yes player reveal.",
                    "title": "Would easy whom fact again return choose."
                    " Site suffer should spring painting glass."
                    "\nThem name charge strategy machine level."
                    " Establish better opportunity.",
                    "facilityID": 1,
                    "typeID": 3,
                    "fileSize": None,
                    "fileCount": None,
                },
                id="greater than",
            ),
            pytest.param(
                "gte",
                "Title for DataGateway API Testing (DB) 0",
                {
                    "doi": "0-9634101-9-9",
                    "endDate": "2001-05-04 00:00:00",
                    "name": "INVESTIGATION 4",
                    "releaseDate": "2001-09-26 00:00:00",
                    "startDate": "2001-02-02 00:00:00",
                    "summary": "Fast purpose right power away health south."
                    "\nQuality serve food buy responsibility go much."
                    " Situation raise manage positive help daughter."
                    " Yes player reveal.",
                    "title": "Would easy whom fact again return choose."
                    " Site suffer should spring painting glass."
                    "\nThem name charge strategy machine level."
                    " Establish better opportunity.",
                    "facilityID": 1,
                    "typeID": 3,
                    "fileSize": None,
                    "fileCount": None,
                },
                id="greater than or equal",
            ),
        ],
    )
    def test_valid_where_operation(
        self,
        flask_test_app_db,
        operation,
        value,
        expected_output,
        single_investigation_test_data_db,
    ):
        test_utility = DatabaseWhereFilter("title", value, operation)
        table = get_entity_object_from_name("Investigation")

        test_query = ReadQuery(table)

        test_utility.apply_filter(test_query)

        response_json = prepare_db_data_for_assertion(
            test_query.base_query.first().to_dict(),
        )

        assert response_json == expected_output
