from datetime import datetime, timezone

import datagateway_api.src.search_api.models as models


AFFILIATION_ICAT_DATA = {
    "id": 1,
    "name": "Test name",
    "fullReference": "Test fullReference",
}

DATASET_ICAT_DATA = {
    "endDate": "2000-12-31 00:00:00+00:00",
    "complete": True,
    "name": "Test name",
    "id": 1,
    "modTime": "2000-12-31 00:00:00+00:00",
    "location": "Test location",
    "modId": "Test modId",
    "description": "Test description",
    "createId": "Test createId",
    "createTime": "2000-12-31 00:00:00+00:00",
    "doi": "Test doi",
    "startDate": "2000-12-31 00:00:00+00:00",
}

DATASET_PARAMETER_ICAT_DATA = {
    "error": 1.0,
    "stringValue": "Test stringValue",
    "id": 1,
    "numericValue": None,
    "modTime": "2000-12-31 00:00:00+00:00",
    "rangeTop": 1.0,
    "modId": "Test modId",
    "createId": "Test createId",
    "createTime": "2000-12-31 00:00:00+00:00",
    "rangeBottom": 1.0,
    "dateTimeValue": None,
}

DATAFILE_ICAT_DATA = {
    "name": "Test name",
    "id": 1,
    "datafileModTime": "2000-12-31 00:00:00+00:00",
    "modTime": "2000-12-31 00:00:00+00:00",
    "fileSize": 1234,
    "location": "Test location",
    "modId": "Test modId",
    "description": "Test description",
    "createId": "Test createId",
    "createTime": "2000-12-31 00:00:00+00:00",
    "doi": "Test doi",
    "datafileCreateTime": "2000-12-31 00:00:00+00:00",
    "checksum": "Test checksum",
}

FACILITY_ICAT_DATA = {
    "daysUntilRelease": 1,
    "name": "Test name",
    "id": 1,
    "modTime": "2000-12-31 00:00:00+00:00",
    "url": None,
    "fullName": None,
    "modId": "Test modId",
    "description": "Test description",
    "createId": "Test createId",
    "createTime": "2000-12-31 00:00:00+00:00",
}

INSTRUMENT_ICAT_DATA = {
    "type": "Test type",
    "pid": None,
    "name": "Test name",
    "id": 1,
    "modTime": "2000-12-31 00:00:00+00:00",
    "url": "Test url",
    "fullName": "Test fullName",
    "modId": "Test modId",
    "description": "Test description",
    "createId": "Test createId",
    "createTime": "2000-12-31 00:00:00+00:00",
}

INVESTIGATION_ICAT_DATA = {
    "endDate": "2000-12-31 00:00:00+00:00",
    "name": "Test name",
    "releaseDate": str(datetime.now(timezone.utc)),
    "id": 1,
    "modTime": "2000-12-31 00:00:00+00:00",
    "modId": "Test modId",
    "createId": "Test createId",
    "summary": "Test summary",
    "visitId": "Test visitId",
    "createTime": "2000-12-31 00:00:00+00:00",
    "doi": "Test doi",
    "startDate": "2000-12-31 00:00:00+00:00",
    "title": "Test title",
}

INVESTIGATION_PARAMETER_ICAT_DATA = DATASET_PARAMETER_ICAT_DATA.copy()
INVESTIGATION_PARAMETER_ICAT_DATA["stringValue"] = None
INVESTIGATION_PARAMETER_ICAT_DATA["dateTimeValue"] = "2000-12-31 00:00:00+00:00"

INVESTIGATION_TYPE_ICAT_DATA = {
    "modId": "Test modId",
    "description": "Test description",
    "createId": "Test createId",
    "name": "Test name",
    "createTime": "2000-12-31 00:00:00+00:00",
    "id": 1,
    "modTime": "2000-12-31 00:00:00+00:00",
}

INVESTIGATION_USER_ICAT_DATA = {
    "id": 1,
    "modId": "Test modId",
    "createId": "Test createId",
    "createTime": "2000-12-31 00:00:00+00:00",
    "role": "Test role",
    "modTime": "2000-12-31 00:00:00+00:00",
}

KEYWORD_ICAT_DATA = {
    "modId": "Test modId",
    "createId": "Test createId",
    "name": "Test name",
    "createTime": "2000-12-31 00:00:00+00:00",
    "id": 1,
    "modTime": "2000-12-31 00:00:00+00:00",
}

PARAMETER_TYPE_ICAT_DATA = {
    "pid": None,
    "verified": True,
    "unitsFullName": "Test unitsFullName",
    "enforced": False,
    "maximumNumericValue": 1.0,
    "name": "Test name",
    "modId": "Test modId",
    "minimumNumericValue": 1.0,
    "createId": "Test createId",
    "applicableToDataCollection": False,
    "applicableToInvestigation": False,
    "applicableToDatafile": True,
    "units": "Test units",
    "id": 1,
    "modTime": "2000-12-31 00:00:00+00:00",
    "applicableToDataset": True,
    "description": "Test description",
    "valueType": "Test valueType",
    "createTime": "2000-12-31 00:00:00+00:00",
    "applicableToSample": False,
}

SAMPLE_ICAT_DATA = {
    "pid": "None",
    "modId": "Test modId",
    "createId": "Test createId",
    "name": "Test name",
    "createTime": "2000-12-31 00:00:00+00:00",
    "id": 1,
    "modTime": "2000-12-31 00:00:00+00:00",
}

TECHNIQUE_ICAT_DATA = {
    "name": "Test name",
    "pid": "Test pid",
    "description": "Test description",
}

USER_ICAT_DATA = {
    "email": "Test email",
    "name": "Test name",
    "id": 1,
    "modTime": "2000-12-31 00:00:00+00:00",
    "familyName": None,
    "modId": "Test modId",
    "fullName": "Test fullName",
    "orcidId": "Test orcidId",
    "createId": "Test createId",
    "createTime": "2000-12-31 00:00:00+00:00",
    "affiliation": None,
    "givenName": None,
}


AFFILIATION_PANOSC_DATA = {
    "name": AFFILIATION_ICAT_DATA["name"],
    "id": str(AFFILIATION_ICAT_DATA["id"]),
    "address": AFFILIATION_ICAT_DATA["fullReference"],
    "city": None,
    "country": None,
    "members": [],
}

DATASET_PANOSC_DATA = {
    "pid": DATASET_ICAT_DATA["doi"],
    "title": DATASET_ICAT_DATA["name"],
    "creationDate": datetime.fromisoformat(DATASET_ICAT_DATA["createTime"]),
    "isPublic": True,
    "size": None,
    "documents": [],
    "techniques": [],
    "instrument": None,
    "files": [],
    "parameters": [],
    "samples": [],
}

DOCUMENT_PANOSC_DATA = {
    "pid": INVESTIGATION_ICAT_DATA["doi"],
    "isPublic": False,
    "type": INVESTIGATION_TYPE_ICAT_DATA["name"],
    "title": INVESTIGATION_ICAT_DATA["name"],
    "summary": INVESTIGATION_ICAT_DATA["summary"],
    "doi": INVESTIGATION_ICAT_DATA["doi"],
    "startDate": datetime.fromisoformat(INVESTIGATION_ICAT_DATA["startDate"]),
    "endDate": datetime.fromisoformat(INVESTIGATION_ICAT_DATA["endDate"]),
    "releaseDate": datetime.fromisoformat(INVESTIGATION_ICAT_DATA["releaseDate"]),
    "license": None,
    "keywords": [KEYWORD_ICAT_DATA["name"]],
    "datasets": [],
    "members": [],
    "parameters": [],
}

FILE_PANOSC_DATA = {
    "id": str(DATAFILE_ICAT_DATA["id"]),
    "name": DATAFILE_ICAT_DATA["name"],
    "path": DATAFILE_ICAT_DATA["location"],
    "size": DATAFILE_ICAT_DATA["fileSize"],
    "dataset": None,
}

INSTRUMENT_PANOSC_DATA = {
    "pid": str(INSTRUMENT_ICAT_DATA["id"]),
    "name": INSTRUMENT_ICAT_DATA["name"],
    "facility": FACILITY_ICAT_DATA["name"],
    "datasets": [],
}

MEMBER_PANOSC_DATA = {
    "id": str(INVESTIGATION_USER_ICAT_DATA["id"]),
    "role": INVESTIGATION_USER_ICAT_DATA["role"],
    "document": None,
    "person": None,
    "affiliation": None,
}

PARAMETER_PANOSC_DATA = {
    "id": str(INVESTIGATION_PARAMETER_ICAT_DATA["id"]),
    "name": PARAMETER_TYPE_ICAT_DATA["name"],
    "value": INVESTIGATION_PARAMETER_ICAT_DATA["dateTimeValue"],
    "unit": PARAMETER_TYPE_ICAT_DATA["units"],
    "dataset": None,
    "document": None,
}

PERSON_PANOSC_DATA = {
    "id": str(USER_ICAT_DATA["id"]),
    "fullName": USER_ICAT_DATA["fullName"],
    "orcid": USER_ICAT_DATA["orcidId"],
    "researcherId": None,
    "firstName": USER_ICAT_DATA["givenName"],
    "lastName": USER_ICAT_DATA["familyName"],
    "members": [],
}

SAMPLE_PANOSC_DATA = {
    "name": SAMPLE_ICAT_DATA["name"],
    "pid": SAMPLE_ICAT_DATA["pid"],
    "description": PARAMETER_TYPE_ICAT_DATA["description"],
    "datasets": [],
}

TECHNIQUE_PANOSC_DATA = {
    "pid": TECHNIQUE_ICAT_DATA["pid"],
    "name": TECHNIQUE_ICAT_DATA["name"],
    "datasets": [],
}


class TestModels:
    def test_from_icat_affiliation_entity_without_data_for_related_entities(self):
        affiliation_entity = models.Affiliation.from_icat(AFFILIATION_ICAT_DATA, [])

        assert affiliation_entity.dict(by_alias=True) == AFFILIATION_PANOSC_DATA

    def test_from_icat_affiliation_entity_with_data_for_all_related_entities(self):
        expected_entity_data = AFFILIATION_PANOSC_DATA.copy()
        expected_entity_data["members"] = [MEMBER_PANOSC_DATA]

        icat_data = AFFILIATION_ICAT_DATA.copy()
        icat_data["user"] = {
            "user": {"investigationUsers": [INVESTIGATION_USER_ICAT_DATA]},
        }

        affiliation_entity = models.Affiliation.from_icat(icat_data, ["members"])

        assert affiliation_entity.dict(by_alias=True) == expected_entity_data

    def test_from_icat_dataset_entity_without_data_for_related_entities(self):
        dataset_entity = models.Dataset.from_icat(DATASET_ICAT_DATA, [])

        assert dataset_entity.dict(by_alias=True) == DATASET_PANOSC_DATA

    def test_from_icat_dataset_entity_with_data_for_mandatory_related_entities(self):
        expected_entity_data = DATASET_PANOSC_DATA.copy()
        expected_entity_data["documents"] = [DOCUMENT_PANOSC_DATA]
        expected_entity_data["techniques"] = [
            TECHNIQUE_PANOSC_DATA,
            TECHNIQUE_PANOSC_DATA,
        ]

        icat_data = DATASET_ICAT_DATA.copy()
        icat_data["investigation"] = INVESTIGATION_ICAT_DATA.copy()
        icat_data["investigation"]["type"] = INVESTIGATION_TYPE_ICAT_DATA
        icat_data["investigation"]["keywords"] = [KEYWORD_ICAT_DATA]
        icat_data["datasetTechniques"] = [
            {"technique": TECHNIQUE_ICAT_DATA},
            {"technique": TECHNIQUE_ICAT_DATA},
        ]

        dataset_entity = models.Dataset.from_icat(
            icat_data, ["documents", "techniques"],
        )

        assert dataset_entity.dict(by_alias=True) == expected_entity_data

    def test_from_icat_dataset_entity_with_data_for_all_related_entities(self):
        expected_entity_data = DATASET_PANOSC_DATA.copy()
        expected_entity_data["documents"] = [DOCUMENT_PANOSC_DATA]
        expected_entity_data["techniques"] = [TECHNIQUE_PANOSC_DATA]
        expected_entity_data["instrument"] = INSTRUMENT_PANOSC_DATA
        expected_entity_data["files"] = [FILE_PANOSC_DATA, FILE_PANOSC_DATA]
        expected_entity_data["parameters"] = [PARAMETER_PANOSC_DATA.copy()]
        expected_entity_data["parameters"][0]["value"] = DATASET_PARAMETER_ICAT_DATA[
            "stringValue"
        ]
        expected_entity_data["samples"] = [SAMPLE_PANOSC_DATA]

        icat_data = DATASET_ICAT_DATA.copy()
        icat_data["investigation"] = INVESTIGATION_ICAT_DATA.copy()
        icat_data["investigation"]["type"] = INVESTIGATION_TYPE_ICAT_DATA
        icat_data["investigation"]["keywords"] = [KEYWORD_ICAT_DATA]
        icat_data["datasetTechniques"] = [{"technique": TECHNIQUE_ICAT_DATA}]
        icat_data["datasetInstruments"] = [
            {"instrument": INSTRUMENT_ICAT_DATA.copy()},
            {"instrument": INSTRUMENT_ICAT_DATA.copy()},
        ]
        icat_data["datasetInstruments"][0]["instrument"][
            "facility"
        ] = FACILITY_ICAT_DATA
        icat_data["datasetInstruments"][1]["instrument"][
            "facility"
        ] = FACILITY_ICAT_DATA
        icat_data["datafiles"] = [DATAFILE_ICAT_DATA, DATAFILE_ICAT_DATA]
        icat_data["parameters"] = [DATASET_PARAMETER_ICAT_DATA.copy()]
        icat_data["parameters"][0]["type"] = PARAMETER_TYPE_ICAT_DATA
        icat_data["sample"] = SAMPLE_ICAT_DATA.copy()
        icat_data["sample"]["parameters"] = [
            {"type": PARAMETER_TYPE_ICAT_DATA},
            {"type": PARAMETER_TYPE_ICAT_DATA},
        ]

        dataset_entity = models.Dataset.from_icat(
            icat_data,
            ["documents", "techniques", "instrument", "files", "parameters", "samples"],
        )

        assert dataset_entity.dict(by_alias=True) == expected_entity_data

    def test_from_icat_document_entity_without_data_for_related_entities(self):
        icat_data = INVESTIGATION_ICAT_DATA.copy()
        icat_data["type"] = INVESTIGATION_TYPE_ICAT_DATA
        icat_data["keywords"] = [KEYWORD_ICAT_DATA]

        document_entity = models.Document.from_icat(icat_data, [])

        assert document_entity.dict(by_alias=True) == DOCUMENT_PANOSC_DATA

    def test_from_icat_document_entity_with_data_for_mandatory_related_entities(self):
        expected_entity_data = DOCUMENT_PANOSC_DATA.copy()
        expected_entity_data["datasets"] = [DATASET_PANOSC_DATA, DATASET_PANOSC_DATA]

        icat_data = INVESTIGATION_ICAT_DATA.copy()
        icat_data["type"] = INVESTIGATION_TYPE_ICAT_DATA
        icat_data["keywords"] = [KEYWORD_ICAT_DATA]
        icat_data["datasets"] = [DATASET_ICAT_DATA, DATASET_ICAT_DATA]

        document_entity = models.Document.from_icat(icat_data, ["datasets"])

        assert document_entity.dict(by_alias=True) == expected_entity_data

    def test_from_icat_document_entity_with_data_for_all_related_entities(self):
        expected_entity_data = DOCUMENT_PANOSC_DATA.copy()
        expected_entity_data["datasets"] = [DATASET_PANOSC_DATA, DATASET_PANOSC_DATA]
        expected_entity_data["members"] = [MEMBER_PANOSC_DATA]
        expected_entity_data["parameters"] = [PARAMETER_PANOSC_DATA]

        icat_data = INVESTIGATION_ICAT_DATA.copy()
        icat_data["type"] = INVESTIGATION_TYPE_ICAT_DATA
        icat_data["keywords"] = [KEYWORD_ICAT_DATA]
        icat_data["datasets"] = [DATASET_ICAT_DATA, DATASET_ICAT_DATA]
        icat_data["investigationUsers"] = [INVESTIGATION_USER_ICAT_DATA]
        icat_data["parameters"] = [INVESTIGATION_PARAMETER_ICAT_DATA.copy()]
        icat_data["parameters"][0]["type"] = PARAMETER_TYPE_ICAT_DATA

        document_entity = models.Document.from_icat(icat_data, ["datasets"])

        assert document_entity.dict(by_alias=True) == expected_entity_data
