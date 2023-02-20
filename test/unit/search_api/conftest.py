import json
from unittest.mock import mock_open, patch

import pytest

from datagateway_api.src.search_api.panosc_mappings import PaNOSCMappings


@pytest.fixture()
def test_search_api_mappings_data():
    return {
        "Affiliation": {
            "base_icat_entity": "Affiliation",
            "id": "id",
            "name": "name",
            "address": "fullReference",
            "city": "",
            "country": "",
            "members": {"Member": "user.user.investigationUsers"},
        },
        "Dataset": {
            "base_icat_entity": "Dataset",
            "pid": ["doi", "id"],
            "title": "name",
            "isPublic": "",
            "creationDate": "createTime",
            "size": "",
            "documents": {"Document": "investigation"},
            "techniques": {"Technique": "datasetTechniques.technique"},
            "instrument": {"Instrument": "datasetInstruments.instrument"},
            "files": {"File": "datafiles"},
            "parameters": {"Parameter": "parameters"},
            "samples": {"Sample": "sample"},
        },
        "Document": {
            "base_icat_entity": "Investigation",
            "pid": ["doi", "id"],
            "isPublic": "",
            "type": "type.name",
            "title": "name",
            "summary": "summary",
            "doi": "doi",
            "startDate": "startDate",
            "endDate": "endDate",
            "releaseDate": "releaseDate",
            "license": "",
            "keywords": "keywords.name",
            "datasets": {"Dataset": "datasets"},
            "members": {"Member": "investigationUsers"},
            "parameters": {"Parameter": "parameters"},
        },
        "File": {
            "base_icat_entity": "Datafile",
            "id": "id",
            "name": "name",
            "path": "location",
            "size": "fileSize",
            "dataset": {"Dataset": "dataset"},
        },
        "Instrument": {
            "base_icat_entity": "Instrument",
            "pid": ["pid", "id"],
            "name": "name",
            "facility": "facility.name",
            "datasets": {"Dataset": "datasetInstruments.dataset"},
        },
        "Member": {
            "base_icat_entity": "InvestigationUser",
            "id": "id",
            "role": "role",
            "document": {"Document": "investigation"},
            "person": {"Person": "user"},
            "affiliation": {"Affiliation": "user.dataPublicationUsers.affiliations"},
        },
        "Parameter": {
            "base_icat_entity": ["InvestigationParameter", "DatasetParameter"],
            "id": "id",
            "name": "type.name",
            "value": ["numericValue", "stringValue", "dateTimeValue"],
            "unit": "type.units",
            "dataset": {"Dataset": "dataset"},
            "document": {"Document": "investigation"},
        },
        "Person": {
            "base_icat_entity": "User",
            "id": "id",
            "fullName": "fullName",
            "orcid": "orcidId",
            "researcherId": "",
            "firstName": "givenName",
            "lastName": "familyName",
            "members": {"Member": "investigationUsers"},
        },
        "Sample": {
            "base_icat_entity": "Sample",
            "name": "name",
            "pid": ["pid", "id"],
            "description": "parameters.type.description",
            "datasets": {"Dataset": "datasets"},
        },
        "Technique": {
            "base_icat_entity": "Technique",
            "pid": ["pid", "id"],
            "name": "name",
            "datasets": {"Dataset": "datasetTechniques.dataset"},
        },
    }


@pytest.fixture()
def test_panosc_mappings(test_search_api_mappings_data):
    with patch(
        "builtins.open", mock_open(read_data=json.dumps(test_search_api_mappings_data)),
    ):
        return PaNOSCMappings("test/path")
