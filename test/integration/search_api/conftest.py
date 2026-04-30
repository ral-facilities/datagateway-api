import json
from unittest.mock import mock_open, patch

from fastapi.testclient import TestClient
import pytest

from datagateway_api.src.common.config import Config
from datagateway_api.src.main import create_search_api_app
from datagateway_api.src.search_api.panosc_mappings import PaNOSCMappings
from datagateway_api.src.search_api.query import SearchAPIQuery


@pytest.fixture()
def search_api_query_dataset():
    return SearchAPIQuery("Dataset")


@pytest.fixture()
def search_api_query_document():
    return SearchAPIQuery("Document")


@pytest.fixture()
def search_api_query_instrument():
    return SearchAPIQuery("Instrument")


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
        "builtins.open",
        mock_open(read_data=json.dumps(test_search_api_mappings_data)),
    ):
        return PaNOSCMappings("test/path")


@pytest.fixture(name="test_search_api_client")
def fixture_test_client() -> TestClient:
    """
    Fixture for creating a test client for the application.

    :return: The test client.
    """
    app = create_search_api_app()
    app.root_path = f"{Config.config.url_prefix}{Config.config.search_api.extension}"
    return TestClient(app)
