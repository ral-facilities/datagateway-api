from icat.entity import Entity
import pytest

from datagateway_api.common.exceptions import PythonICATError
from datagateway_api.common.icat.filters import PythonICATWhereFilter
from datagateway_api.common.icat.query import ICATQuery


def remove_meta_attributes(entity_dict):
    meta_attributes = Entity.MetaAttr
    for attr in meta_attributes:
        entity_dict.pop(attr)


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

        query_output_dicts = []
        for entity in query_data:
            entity_dict = entity.as_dict()
            remove_meta_attributes(entity_dict)
            query_output_dicts.append(entity_dict)

        assert query_output_dicts == single_investigation_test_data

    def test_invalid_query_execution(self, icat_client):
        # Try to get ICATValidationError raised
        pass

    def test_valid_count_query_execution(self, icat_client):
        pass

    def test_valid_distinct_query_execution(self, icat_client):
        pass

    def test_json_format_execution_output(self, icat_client):
        pass

    def test_icat_execution_output(self, icat_client):
        pass

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
