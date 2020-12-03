import datetime

import pytest

from datagateway_api.common.database.models import (
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
    datafile.ID = 1
    datafile.LOCATION = "test location"
    datafile.DATASET = dataset_entity
    datafile.DATAFILEFORMAT = datafileformat
    datafile.NAME = "test name"
    datafile.MOD_TIME = datetime.datetime(2000, 1, 1)
    datafile.CREATE_TIME = datetime.datetime(2000, 1, 1)
    datafile.CHECKSUM = "test checksum"
    datafile.FILESIZE = 64
    datafile.DATAFILEMODTIME = datetime.datetime(2000, 1, 1)
    datafile.DATAFILECREATETIME = datetime.datetime(2000, 1, 1)
    datafile.DATASET_ID = 1
    datafile.DOI = "test doi"
    datafile.DESCRIPTION = "test description"
    datafile.CREATE_ID = "test create id"
    datafile.MOD_ID = "test mod id"
    datafile.DATAFILEFORMAT_ID = 1

    return datafile


class TestEntityHelper:
    def test_valid_to_dict(self, datafile_entity):
        expected_dict = {
            "ID": 1,
            "LOCATION": "test location",
            "NAME": "test name",
            "MOD_TIME": str(datetime.datetime(2000, 1, 1)),
            "CHECKSUM": "test checksum",
            "FILESIZE": 64,
            "DATAFILEMODTIME": str(datetime.datetime(2000, 1, 1)),
            "DATAFILECREATETIME": str(datetime.datetime(2000, 1, 1)),
            "DATASET_ID": 1,
            "DOI": "test doi",
            "DESCRIPTION": "test description",
            "CREATE_ID": "test create id",
            "MOD_ID": "test mod id",
            "DATAFILEFORMAT_ID": 1,
            "CREATE_TIME": str(datetime.datetime(2000, 1, 1)),
        }

        test_data = datafile_entity.to_dict()

        assert expected_dict == test_data

    @pytest.mark.parametrize(
        "expected_dict, entity_names",
        [
            pytest.param(
                {
                    "ID": 1,
                    "LOCATION": "test location",
                    "NAME": "test name",
                    "MOD_TIME": str(datetime.datetime(2000, 1, 1)),
                    "CHECKSUM": "test checksum",
                    "FILESIZE": 64,
                    "DATAFILEMODTIME": str(datetime.datetime(2000, 1, 1)),
                    "DATAFILECREATETIME": str(datetime.datetime(2000, 1, 1)),
                    "DATASET_ID": 1,
                    "DOI": "test doi",
                    "DESCRIPTION": "test description",
                    "CREATE_ID": "test create id",
                    "MOD_ID": "test mod id",
                    "DATAFILEFORMAT_ID": 1,
                    "CREATE_TIME": str(datetime.datetime(2000, 1, 1)),
                    "DATASET": {
                        "ID": None,
                        "CREATE_TIME": None,
                        "MOD_TIME": None,
                        "CREATE_ID": None,
                        "MOD_ID": None,
                        "INVESTIGATION_ID": None,
                        "COMPLETE": None,
                        "DESCRIPTION": None,
                        "DOI": None,
                        "END_DATE": None,
                        "LOCATION": None,
                        "NAME": None,
                        "STARTDATE": None,
                        "SAMPLE_ID": None,
                        "TYPE_ID": None,
                    },
                },
                "DATASET",
                id="Dataset",
            ),
            pytest.param(
                {
                    "ID": 1,
                    "LOCATION": "test location",
                    "NAME": "test name",
                    "MOD_TIME": str(datetime.datetime(2000, 1, 1)),
                    "CHECKSUM": "test checksum",
                    "FILESIZE": 64,
                    "DATAFILEMODTIME": str(datetime.datetime(2000, 1, 1)),
                    "DATAFILECREATETIME": str(datetime.datetime(2000, 1, 1)),
                    "DATASET_ID": 1,
                    "DOI": "test doi",
                    "DESCRIPTION": "test description",
                    "CREATE_ID": "test create id",
                    "MOD_ID": "test mod id",
                    "DATAFILEFORMAT_ID": 1,
                    "CREATE_TIME": str(datetime.datetime(2000, 1, 1)),
                    "DATASET": {
                        "ID": None,
                        "CREATE_TIME": None,
                        "MOD_TIME": None,
                        "CREATE_ID": None,
                        "MOD_ID": None,
                        "INVESTIGATION_ID": None,
                        "COMPLETE": None,
                        "DESCRIPTION": None,
                        "DOI": None,
                        "END_DATE": None,
                        "LOCATION": None,
                        "NAME": None,
                        "STARTDATE": None,
                        "SAMPLE_ID": None,
                        "TYPE_ID": None,
                        "INVESTIGATION": {
                            "ID": None,
                            "CREATE_ID": None,
                            "CREATE_TIME": None,
                            "DOI": None,
                            "ENDDATE": None,
                            "MOD_ID": None,
                            "MOD_TIME": None,
                            "NAME": None,
                            "RELEASEDATE": None,
                            "STARTDATE": None,
                            "SUMMARY": None,
                            "TITLE": None,
                            "VISIT_ID": None,
                            "FACILITY_ID": None,
                            "TYPE_ID": None,
                        },
                    },
                },
                {"DATASET": "INVESTIGATION"},
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
            "ID": 1,
            "LOCATION": "test location",
            "NAME": "test name",
            "MOD_TIME": str(datetime.datetime(2000, 1, 1)),
            "CHECKSUM": "test checksum",
            "FILESIZE": 64,
            "DATAFILEMODTIME": str(datetime.datetime(2000, 1, 1)),
            "DATAFILECREATETIME": str(datetime.datetime(2000, 1, 1)),
            "DATASET_ID": 1,
            "DOI": "test doi",
            "DESCRIPTION": "test description",
            "CREATE_ID": "test create id",
            "MOD_ID": "test mod id",
            "DATAFILEFORMAT_ID": 1,
            "CREATE_TIME": str(datetime.datetime(2000, 1, 1)),
        }

        datafile.update_from_dict(test_dict_data)

        expected_datafile_dict = datafile_entity.to_dict()

        assert test_dict_data == expected_datafile_dict
