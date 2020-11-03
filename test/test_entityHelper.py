import datetime
from unittest import TestCase

from datagateway_api.common.database.models import (
    DATAFILE,
    DATASET,
    DATAFILEFORMAT,
    INVESTIGATION,
)


class TestEntityHelper(TestCase):
    def setUp(self):
        self.dataset = DATASET()
        self.investigation = INVESTIGATION()
        self.dataset.INVESTIGATION = self.investigation
        self.datafileformat = DATAFILEFORMAT()
        self.datafile = DATAFILE()
        self.datafile.ID = 1
        self.datafile.LOCATION = "test location"
        self.datafile.DATASET = self.dataset
        self.datafile.DATAFILEFORMAT = self.datafileformat
        self.datafile.NAME = "test name"
        self.datafile.MOD_TIME = datetime.datetime(2000, 1, 1)
        self.datafile.CREATE_TIME = datetime.datetime(2000, 1, 1)
        self.datafile.CHECKSUM = "test checksum"
        self.datafile.FILESIZE = 64
        self.datafile.DATAFILEMODTIME = datetime.datetime(2000, 1, 1)
        self.datafile.DATAFILECREATETIME = datetime.datetime(2000, 1, 1)
        self.datafile.DATASET_ID = 1
        self.datafile.DOI = "test doi"
        self.datafile.DESCRIPTION = "test description"
        self.datafile.CREATE_ID = "test create id"
        self.datafile.MOD_ID = "test mod id"
        self.datafile.DATAFILEFORMAT_ID = 1

    def test_to_dict(self):
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
        self.assertEqual(expected_dict, self.datafile.to_dict())

    def test_to_nested_dict(self):
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
        }
        self.assertEqual(expected_dict, self.datafile.to_nested_dict("DATASET"))
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
        }
        self.assertEqual(
            expected_dict, self.datafile.to_nested_dict({"DATASET": "INVESTIGATION"}),
        )

    def test_get_related_entity(self):
        self.assertEqual(self.dataset, self.datafile.get_related_entity("DATASET"))

    def test_update_from_dict(self):
        datafile = DATAFILE()
        dictionary = {
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
        datafile.update_from_dict(dictionary)
        self.assertEqual(dictionary, datafile.to_dict())
