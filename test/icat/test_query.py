from datetime import datetime

from icat.entity import Entity
import pytest

from datagateway_api.common.date_handler import DateHandler
from datagateway_api.common.exceptions import PythonICATError
from datagateway_api.common.icat.filters import (
    PythonICATSkipFilter,
    PythonICATWhereFilter,
)
from datagateway_api.common.icat.query import ICATQuery


def prepare_icat_data_for_assertion(data, remove_id=False):
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

        assertable_data.append(entity)

    return assertable_data


class TestICATQuery:
    def test_valid_query_creation(self, icat_client):
        # Paramatise and add inputs for conditions, aggregate and includes
        test_query = ICATQuery(icat_client, "User")

        assert test_query.query.entity == icat_client.getEntityClass("User")

    def test_invalid_query_creation(self, icat_client):
        with pytest.raises(PythonICATError):
            ICATQuery(icat_client, "User", conditions={"invalid": "invalid"})

    def test_valid_query_exeuction(
        self, icat_client, single_investigation_test_data,
    ):
        test_query = ICATQuery(icat_client, "Investigation")
        test_data_filter = PythonICATWhereFilter(
            "title", "Test data for the Python ICAT Backend on DataGateway API", "like",
        )
        test_data_filter.apply_filter(test_query.query)
        query_data = test_query.execute_query(icat_client)

        query_output_dicts = prepare_icat_data_for_assertion(query_data)

        assert query_output_dicts == single_investigation_test_data

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

    @pytest.mark.parametrize(
        "included_entity_name, input_fields, expected_fields",
        [
            pytest.param(
                "dataset",
                {"base": ["id"]},
                {"base": []},
                id="Include filter used but no included attributes on distinct filter,"
                " no entity name match",
            ),
            pytest.param(
                "no match",
                {"base": ["id"], "dataset": ["name"]},
                {"base": [], "dataset": ["name"]},
                id="Distinct filter contains included attributes, no entity name match",
            ),
            pytest.param(
                "dataset",
                {"base": ["id"], "dataset": ["name"]},
                {"base": ["name"], "dataset": ["name"]},
                id="Distinct filter contains included attributes, entity name match",
            ),
            pytest.param(
                "dataset",
                {"base": ["id"], "dataset": [], "investigation": ["name"]},
                {"base": [], "dataset": [], "investigation": ["name"]},
                id="Distinct filter contains nested included attributes, no entity name"
                " match",
            ),
            pytest.param(
                "investigation",
                {"base": ["id"], "dataset": [], "investigation": ["name"]},
                {"base": ["name"], "dataset": [], "investigation": ["name"]},
                id="Distinct filter contains nested included attributes, entity name"
                " match",
            ),
        ],
    )
    def test_prepare_distinct_fields(
        self, icat_client, included_entity_name, input_fields, expected_fields,
    ):
        """
        The function tested here should move the list from
        `input_fields[included_entity_name]` to `input_fields["base"]` ready for when
        `entity_to_dict()` is called as part of a recursive call, but the original
        `input_fields` should not be modified. This caused a bug previously
        """
        unmodded_distinct_fields = input_fields.copy()
        test_query = ICATQuery(icat_client, "Datafile")

        distinct_fields_for_recursive_call = test_query.prepare_distinct_fields(
            included_entity_name, input_fields
        )
        print(distinct_fields_for_recursive_call)
        print(input_fields)

        assert distinct_fields_for_recursive_call == expected_fields
        # prepare_distinct_fields() should not modify the original `distinct_fields`
        assert input_fields == unmodded_distinct_fields

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
