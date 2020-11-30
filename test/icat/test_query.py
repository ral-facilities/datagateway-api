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
        # Paramitise and add inputs for conditions, aggregate and includes
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
            "title", "Test data for the Python ICAT Backend on DataGateway API", "eq",
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

    def test_valid_count_query_execution(self, icat_client):
        pass

    def test_valid_distinct_query_execution(self, icat_client):
        pass

    def test_json_format_execution_output(
        self, icat_client, single_investigation_test_data,
    ):
        test_query = ICATQuery(icat_client, "Investigation")
        test_data_filter = PythonICATWhereFilter(
            "title", "Test data for the Python ICAT Backend on DataGateway API", "eq",
        )
        test_data_filter.apply_filter(test_query.query)
        query_data = test_query.execute_query(icat_client, True)

        query_output_json = prepare_icat_data_for_assertion(query_data)

        assert query_output_json == single_investigation_test_data

    # gap in function testing

    def test_valid_entity_to_dict_conversion(self, icat_client):
        # Want just a typical entity and an entity with an entity list in it
        pass

    def test_valid_distinct_attribute_mapping(self):
        pass

    # another gap

    def test_include_fields_list_flatten(self, icat_client):
        included_field_set = {
            "investigationUsers.investigation.datasets",
            "userGroups",
            "instrumentScientists",
            "studies",
        }

        test_query = ICATQuery(icat_client, "User")

        flat_list = test_query.flatten_query_included_fields(included_field_set)
        print(flat_list)

        assert flat_list == [
            "instrumentScientists",
            "investigationUsers",
            "investigation",
            "datasets",
            "studies",
            "userGroups",
        ]
