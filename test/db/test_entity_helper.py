import pytest

from datagateway_api.common.constants import Constants
from datagateway_api.common.datagateway_api.database.models import (
    DATAFILE,
    DATAFILEFORMAT,
    DATASET,
    INVESTIGATION,
)


@pytest.fixture()
def dataset_entity():
    dataset = DATASET()
    investigation = INVESTIGATION()
    dataset.INVESTIGATION = investigation

    return dataset


@pytest.fixture()
def datafile_entity(dataset_entity):
    datafileformat = DATAFILEFORMAT()
    datafile = DATAFILE()
    datafile.id = 1
    datafile.location = "test location"
    datafile.DATASET = dataset_entity
    datafile.DATAFILEFORMAT = datafileformat
    datafile.name = "test name"
    datafile.modTime = Constants.TEST_MOD_CREATE_DATETIME
    datafile.createTime = Constants.TEST_MOD_CREATE_DATETIME
    datafile.checksum = "test checksum"
    datafile.fileSize = 64
    datafile.datafileModTime = Constants.TEST_MOD_CREATE_DATETIME
    datafile.datafileCreateTime = Constants.TEST_MOD_CREATE_DATETIME
    datafile.datasetID = 1
    datafile.doi = "test doi"
    datafile.description = "test description"
    datafile.createId = "test create id"
    datafile.modId = "test mod id"
    datafile.datafileFormatID = 1

    return datafile


class TestEntityHelper:
    def test_valid_to_dict(self, datafile_entity):
        expected_dict = {
            "id": 1,
            "location": "test location",
            "name": "test name",
            "modTime": str(Constants.TEST_MOD_CREATE_DATETIME),
            "checksum": "test checksum",
            "fileSize": 64,
            "datafileModTime": str(Constants.TEST_MOD_CREATE_DATETIME),
            "datafileCreateTime": str(Constants.TEST_MOD_CREATE_DATETIME),
            "datasetID": 1,
            "doi": "test doi",
            "description": "test description",
            "createId": "test create id",
            "modId": "test mod id",
            "datafileFormatID": 1,
            "createTime": str(Constants.TEST_MOD_CREATE_DATETIME),
        }

        test_data = datafile_entity.to_dict()

        assert expected_dict == test_data

    @pytest.mark.parametrize(
        "expected_dict, entity_names",
        [
            pytest.param(
                {
                    "id": 1,
                    "location": "test location",
                    "name": "test name",
                    "modTime": str(Constants.TEST_MOD_CREATE_DATETIME),
                    "checksum": "test checksum",
                    "fileSize": 64,
                    "datafileModTime": str(Constants.TEST_MOD_CREATE_DATETIME),
                    "datafileCreateTime": str(Constants.TEST_MOD_CREATE_DATETIME),
                    "doi": "test doi",
                    "description": "test description",
                    "createId": "test create id",
                    "modId": "test mod id",
                    "datafileFormatID": 1,
                    "createTime": str(Constants.TEST_MOD_CREATE_DATETIME),
                    "datasetID": 1,
                    "dataset": {
                        "id": None,
                        "createTime": None,
                        "modTime": None,
                        "createId": None,
                        "modId": None,
                        "investigationID": None,
                        "complete": None,
                        "description": None,
                        "doi": None,
                        "endDate": None,
                        "location": None,
                        "name": None,
                        "startDate": None,
                        "sampleID": None,
                        "typeID": None,
                    },
                },
                "dataset",
                id="Dataset",
            ),
            pytest.param(
                {
                    "id": 1,
                    "location": "test location",
                    "name": "test name",
                    "modTime": str(Constants.TEST_MOD_CREATE_DATETIME),
                    "checksum": "test checksum",
                    "fileSize": 64,
                    "datafileModTime": str(Constants.TEST_MOD_CREATE_DATETIME),
                    "datafileCreateTime": str(Constants.TEST_MOD_CREATE_DATETIME),
                    "doi": "test doi",
                    "description": "test description",
                    "createId": "test create id",
                    "modId": "test mod id",
                    "datafileFormatID": 1,
                    "createTime": str(Constants.TEST_MOD_CREATE_DATETIME),
                    "datasetID": 1,
                    "dataset": {
                        "id": None,
                        "createTime": None,
                        "modTime": None,
                        "createId": None,
                        "modId": None,
                        "complete": None,
                        "description": None,
                        "doi": None,
                        "endDate": None,
                        "location": None,
                        "name": None,
                        "startDate": None,
                        "sampleID": None,
                        "typeID": None,
                        "investigationID": None,
                        "investigation": {
                            "id": None,
                            "createId": None,
                            "createTime": None,
                            "doi": None,
                            "endDate": None,
                            "modId": None,
                            "modTime": None,
                            "name": None,
                            "releaseDate": None,
                            "startDate": None,
                            "summary": None,
                            "title": None,
                            "visitId": None,
                            "facilityID": None,
                            "typeID": None,
                        },
                    },
                },
                {"dataset": "investigation"},
                id="Dataset including investigation",
            ),
        ],
    )
    def test_valid_to_nested_dict(self, datafile_entity, expected_dict, entity_names):
        test_data = datafile_entity.to_nested_dict(entity_names)

        assert expected_dict == test_data

    def test_valid_get_related_entity(self, dataset_entity, datafile_entity):
        assert dataset_entity == datafile_entity.get_related_entity("DATASET")

    def test_valid_update_from_dict(self, datafile_entity):
        datafile = DATAFILE()
        test_dict_data = {
            "id": 1,
            "location": "test location",
            "name": "test name",
            "modTime": str(Constants.TEST_MOD_CREATE_DATETIME),
            "checksum": "test checksum",
            "fileSize": 64,
            "datafileModTime": str(Constants.TEST_MOD_CREATE_DATETIME),
            "datafileCreateTime": str(Constants.TEST_MOD_CREATE_DATETIME),
            "datasetID": 1,
            "doi": "test doi",
            "description": "test description",
            "createId": "test create id",
            "modId": "test mod id",
            "datafileFormatID": 1,
            "createTime": str(Constants.TEST_MOD_CREATE_DATETIME),
        }

        datafile.update_from_dict(test_dict_data)

        expected_datafile_dict = datafile_entity.to_dict()

        assert test_dict_data == expected_datafile_dict
