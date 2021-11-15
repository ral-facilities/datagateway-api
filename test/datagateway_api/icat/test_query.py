from datetime import datetime

from icat.entity import Entity
import pytest

from datagateway_api.src.common.date_handler import DateHandler
from datagateway_api.src.common.exceptions import PythonICATError
from datagateway_api.src.datagateway_api.icat.filters import (
    PythonICATSkipFilter,
    PythonICATWhereFilter,
)
from datagateway_api.src.datagateway_api.icat.query import ICATQuery


def prepare_icat_data_for_assertion(data, remove_id=False, remove_visit_id=False):
    """
    Remove meta attributes from ICAT data. Meta attributes contain data about data
    creation/modification, and should be removed to ensure correct assertion values

    :param data: ICAT data containing meta attributes such as modTime
    :type data: :class:`list` or :class:`icat.entity.EntityList`
    """
    assertable_data = []
    meta_attributes = Entity.MetaAttr

    for entity in data:
        # Convert to dictionary if an ICAT entity object
        if isinstance(entity, Entity):
            entity = entity.as_dict()

        for attr in meta_attributes:
            entity.pop(attr)

        for attr in entity.keys():
            if isinstance(entity[attr], datetime):
                entity[attr] = DateHandler.datetime_object_to_str(entity[attr])

        # meta_attributes is immutable
        if remove_id:
            entity.pop("id")
        if remove_visit_id:
            entity.pop("visitId")

        assertable_data.append(entity)

    return assertable_data


class TestICATQuery:
    @pytest.mark.parametrize(
        "input_conditions, input_aggregate, input_includes, expected_conditions,"
        " expected_aggregate, expected_includes",
        [
            pytest.param(
                {"fullName": "like Bob"},
                None,
                None,
                {"fullName": ["%s like Bob"]},
                None,
                set(),
                id="Query with condition",
            ),
            pytest.param(
                None,
                "DISTINCT",
                None,
                {},
                "DISTINCT",
                set(),
                id="Query with aggregate",
            ),
            pytest.param(
                None,
                None,
                ["instrumentScientists"],
                {},
                None,
                {"instrumentScientists"},
                id="Query with included entity",
            ),
        ],
    )
    def test_valid_query_creation(
        self,
        icat_client,
        input_conditions,
        input_aggregate,
        input_includes,
        expected_conditions,
        expected_aggregate,
        expected_includes,
    ):
        test_query = ICATQuery(
            icat_client,
            "User",
            conditions=input_conditions,
            aggregate=input_aggregate,
            includes=input_includes,
        )

        assert test_query.query.entity == icat_client.getEntityClass("User")
        assert test_query.query.conditions == expected_conditions
        assert test_query.query.aggregate == expected_aggregate
        assert test_query.query.includes == expected_includes

    def test_valid_manual_count_flag_init(self, icat_client):
        """
        Flag required for distinct filters used on count endpoints should be initialised
        in `__init__()` of ICATQuery`
        """
        test_query = ICATQuery(icat_client, "User")

        assert not test_query.query.manual_count

    def test_invalid_query_creation(self, icat_client):
        with pytest.raises(PythonICATError):
            ICATQuery(icat_client, "User", conditions={"invalid": "invalid"})

    @pytest.mark.parametrize(
        "query_conditions, query_aggregate, query_includes, query_attributes"
        ", manual_count, return_json_format_flag, expected_query_result",
        [
            pytest.param(
                {
                    "title": "like '%Test data for the Python ICAT Backend on"
                    " DataGateway API%'",
                },
                None,
                None,
                None,
                False,
                True,
                [
                    {
                        "doi": None,
                        "endDate": "2020-01-08 01:01:01+00:00",
                        "name": "Test Data for DataGateway API Testing 0",
                        "releaseDate": None,
                        "startDate": "2020-01-04 01:01:01+00:00",
                        "summary": None,
                        "title": "Test data for the Python ICAT Backend on DataGateway"
                        " API 0",
                    },
                ],
                id="Ordinary query",
            ),
            pytest.param(
                {
                    "title": "like '%Test data for the Python ICAT Backend on"
                    " DataGateway API%'",
                },
                None,
                ["facility"],
                None,
                False,
                True,
                [
                    {
                        "doi": None,
                        "endDate": "2020-01-08 01:01:01+00:00",
                        "name": "Test Data for DataGateway API Testing 0",
                        "releaseDate": None,
                        "startDate": "2020-01-04 01:01:01+00:00",
                        "summary": None,
                        "title": "Test data for the Python ICAT Backend on DataGateway"
                        " API 0",
                        "facility": {
                            "createId": "user",
                            "createTime": "2002-11-27 06:20:36+00:00",
                            "daysUntilRelease": 10,
                            "description": "Lorem ipsum light source",
                            "fullName": None,
                            "id": 1,
                            "modId": "user",
                            "modTime": "2005-04-30 19:41:49+00:00",
                            "name": "LILS",
                            "url": None,
                        },
                    },
                ],
                id="Query with included entity",
            ),
            pytest.param(
                {
                    "title": "like '%Test data for the Python ICAT Backend on"
                    " DataGateway API%'",
                },
                "COUNT",
                None,
                None,
                False,
                True,
                [1],
                id="Count query",
            ),
            pytest.param(
                {
                    "title": "like '%Test data for the Python ICAT Backend on"
                    " DataGateway API%'",
                },
                None,
                None,
                None,
                False,
                False,
                [
                    {
                        "doi": None,
                        "endDate": "2020-01-08 01:01:01+00:00",
                        "name": "Test Data for DataGateway API Testing 0",
                        "releaseDate": None,
                        "startDate": "2020-01-04 01:01:01+00:00",
                        "summary": None,
                        "title": "Test data for the Python ICAT Backend on DataGateway"
                        " API 0",
                    },
                ],
                id="Data returned as entity objects",
            ),
            pytest.param(
                {
                    "title": "like '%Test data for the Python ICAT Backend on"
                    " DataGateway API%'",
                },
                "DISTINCT",
                None,
                "title",
                False,
                True,
                [
                    {
                        "title": "Test data for the Python ICAT Backend on DataGateway"
                        " API 0",
                    },
                ],
                id="Single distinct field",
            ),
            pytest.param(
                {
                    "title": "like '%Test data for the Python ICAT Backend on"
                    " DataGateway API%'",
                },
                "DISTINCT",
                None,
                ["title", "name"],
                False,
                True,
                [
                    {
                        "title": "Test data for the Python ICAT Backend on DataGateway"
                        " API 0",
                        "name": "Test Data for DataGateway API Testing 0",
                    },
                ],
                id="Multiple distinct fields",
            ),
            pytest.param(
                {
                    "title": "like '%Test data for the Python ICAT Backend on"
                    " DataGateway API%'",
                },
                "DISTINCT",
                None,
                ["title", "name"],
                True,
                True,
                [1],
                id="Multiple distinct fields on count query",
            ),
            pytest.param(
                {"title": "like '%Unknown testing data for DG API%'"},
                "DISTINCT",
                None,
                ["title", "name"],
                True,
                True,
                [0],
                id="Multiple distinct fields on count query to return 0 matches",
            ),
        ],
    )
    @pytest.mark.usefixtures("single_investigation_test_data")
    def test_valid_query_exeuction(
        self,
        icat_client,
        query_conditions,
        query_aggregate,
        query_includes,
        query_attributes,
        manual_count,
        return_json_format_flag,
        expected_query_result,
    ):
        test_query = ICATQuery(
            icat_client,
            "Investigation",
            conditions=query_conditions,
            aggregate=query_aggregate,
            includes=query_includes,
        )
        test_query.query.setAttributes(query_attributes)
        test_query.query.manual_count = manual_count
        query_data = test_query.execute_query(
            icat_client, return_json_formattable=return_json_format_flag,
        )

        if (
            test_query.query.aggregate != "COUNT"
            and test_query.query.aggregate != "DISTINCT"
        ):
            query_data = prepare_icat_data_for_assertion(
                query_data, remove_id=True, remove_visit_id=True,
            )

        assert query_data == expected_query_result

    def test_invalid_query_execution(self, icat_client):
        test_query = ICATQuery(icat_client, "Investigation")

        # Create filter with valid value, then change to invalid value that'll cause 500
        test_skip_filter = PythonICATSkipFilter(1)
        test_skip_filter.skip_value = -1
        test_skip_filter.apply_filter(test_query.query)

        with pytest.raises(PythonICATError):
            test_query.execute_query(icat_client)

    def test_json_format_execution_output(
        self, icat_client, single_investigation_test_data,
    ):
        test_query = ICATQuery(icat_client, "Investigation")
        test_data_filter = PythonICATWhereFilter(
            "title", "Test data for the Python ICAT Backend on DataGateway API", "like",
        )
        test_data_filter.apply_filter(test_query.query)
        query_data = test_query.execute_query(icat_client, True)

        query_output_json = prepare_icat_data_for_assertion(query_data)

        assert query_output_json == single_investigation_test_data

    def test_valid_get_distinct_attributes(self, icat_client):
        test_query = ICATQuery(icat_client, "Investigation")
        test_query.query.setAttributes(["summary", "name"])

        assert test_query.get_distinct_attributes() == ["summary", "name"]

    def test_include_fields_list_flatten(self, icat_client):
        included_field_set = {
            "investigationUsers.investigation.datasets",
            "userGroups",
            "instrumentScientists",
            "studies",
        }

        test_query = ICATQuery(icat_client, "User")
        flat_list = test_query.flatten_query_included_fields(included_field_set)

        assert flat_list == [
            "instrumentScientists",
            "investigationUsers",
            "investigation",
            "datasets",
            "studies",
            "userGroups",
        ]
