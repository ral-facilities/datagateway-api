import json
from unittest.mock import ANY

from fastapi.testclient import TestClient
import pytest

INSTRUMENT_1 = {
    "id": 1,
    "name": "INSTRUMENT 1",
    "fullName": (
        "Stop prove field onto think suffer measure. Table lose season identify professor happen third simply. "
        "Beat professional blue clear style have.\nAnalysis reflect work or hour color maybe."
    ),
    "type": "1",
    "url": "https://hopkins-lynch.com/",
    "description": (
        "Suggest shake effort many last prepare small. Maintain throw hope parent.\n"
        "Entire soon option bill fish against power.\nRather why rise month shake voice."
    ),
    "instrumentScientists": [
        {
            "id": 1,
            "user": {
                "email": "wevans@yahoo.com",
                "fullName": "Kathryn Fox",
                "id": 69,
                "name": "Mark69",
                "orcidId": "7206",
            },
        },
    ],
}
DATA_PUBLICATION_1 = {
    "content": {
        "dataCollectionDatafiles": [],
        "dataCollectionDatasets": [],
        "dataCollectionInvestigations": [],
        "doi": "0-285-87335-0",
        "id": 47,
    },
    "dates": [{"date": "2017-09-06", "dateType": "Copyrighted", "id": 1}],
    "description": (
        "Stop prove field onto think suffer measure. Table lose season identify professor happen third simply. "
        "Beat professional blue clear style have.\nAnalysis reflect work or hour color maybe."
    ),
    "facility": {"daysUntilRelease": 10, "description": "Lorem ipsum light source", "id": 1, "name": "LILS"},
    "id": 1,
    "pid": "1-4890-6828-7",
    "publicationDate": "2021-03-23T00:00:00Z",
    "relatedItems": [
        {
            "fullReference": (
                "Consider heavy audience Mrs that must. Focus increase bed. Plan really under everyone size if."
            ),
            "id": 118,
            "identifier": "0-316-07926-X",
            "publication": {
                "description": (
                    "Stop prove field onto think suffer measure. Table lose season identify professor happen third "
                    "simply. Beat professional blue clear style have.\nAnalysis reflect work or hour color maybe."
                ),
                "id": 1,
                "pid": "1-4890-6828-7",
                "publicationDate": "2021-03-23T00:00:00Z",
                "subject": "argue",
                "title": (
                    "Suggest shake effort many last prepare small. Maintain throw hope parent.\n"
                    "Entire soon option bill fish against power.\nRather why rise month shake voice."
                ),
            },
            "relatedItemType": "DataPaper",
            "relationType": "References",
            "title": (
                "Toward nature later camera. Yard team indicate speech wear western traditional. "
                "Paper size maybe experience."
            ),
        },
        {
            "fullReference": (
                "Subject card foreign couple. Prevent dark person somebody response page.\n"
                "Probably couple western through book old. Condition send read stock me."
            ),
            "id": 59,
            "identifier": "0-546-32494-0",
            "publication": {
                "description": (
                    "Stop prove field onto think suffer measure. Table lose season identify professor happen third "
                    "simply. Beat professional blue clear style have.\nAnalysis reflect work or hour color maybe."
                ),
                "id": 1,
                "pid": "1-4890-6828-7",
                "publicationDate": "2021-03-23T00:00:00Z",
                "subject": "argue",
                "title": (
                    "Suggest shake effort many last prepare small. Maintain throw hope parent.\n"
                    "Entire soon option bill fish against power.\nRather why rise month shake voice."
                ),
            },
            "relatedItemType": "ComputationalNotebook",
            "relationType": "IsReviewedBy",
            "title": (
                "Media later look better military later. Arm base your human entire pressure man. "
                "Will heart media both actually major."
            ),
        },
    ],
    "subject": "argue",
    "title": (
        "Suggest shake effort many last prepare small. Maintain throw hope parent.\n"
        "Entire soon option bill fish against power.\nRather why rise month shake voice."
    ),
    "users": [
        {
            "affiliations": [
                {
                    "fullReference": (
                        "Suggest shake effort many last prepare small. Maintain throw hope parent.\n"
                        "Entire soon option bill fish against power.\nRather why rise month shake voice."
                    ),
                    "id": 1,
                    "name": (
                        "Season identify professor happen third. Beat professional blue clear style have. "
                        "Light final summer."
                    ),
                    "pid": "0-449-78690-0",
                },
            ],
            "contributorType": "DataCollector",
            "email": "jenniferadams@hotmail.com",
            "familyName": "Heath",
            "fullName": "Colleen Heath",
            "givenName": "Colleen",
            "id": 1,
            "orderKey": "3",
            "user": {
                "email": "jenniferadams@hotmail.com",
                "fullName": "Colleen Heath",
                "id": 292,
                "name": "Jenny292",
                "orcidId": "19931",
            },
        },
    ],
}
INVESTIGATION_1 = {
    "doi": "0-417-77631-4",
    "endDate": "2000-07-09T00:00:00Z",
    "fileCount": 0,
    "fileSize": 0,
    "id": 1,
    "name": "INVESTIGATION 1",
    "releaseDate": "2000-07-05T00:00:00Z",
    "startDate": "2000-04-03T00:00:00Z",
    "summary": (
        "Throw hope parent. Receive entire soon. War top air agent must voice high describe.\n"
        "Month shake voice. Do discuss despite least face again study. Two beyond picture rich fast sea time."
    ),
    "title": "Analysis reflect work or hour color maybe.\nMuch team discussion message weight.",
    "visitId": "70",
}
INVESTIGATION_1_INVESTIGATION_INSTRUMENTS = {
    "investigationInstruments": [
        {
            "id": 1,
            "instrument": {
                "id": 3,
                "description": (
                    "Financial vote season indicate. Candidate night sure opportunity design.\n"
                    "Commercial test wind region meeting her get. Of to option manage visit. "
                    "Fast matter foot the tonight adult."
                ),
                "fullName": (
                    "Rise be college treat. Environmental forward media effort fund.\n"
                    "Dog want single resource major. Necessary bit always available term small stock game."
                ),
                "name": "INSTRUMENT 3",
                "type": "3",
                "url": "http://www.jackson-allen.com/",
            },
        },
    ],
}
INVESTIGATION_1_INVESTIGATION_USERS = {
    "investigationUsers": [
        {
            "id": 1,
            "role": "PI",
            "user": {
                "id": 292,
                "email": "jenniferadams@hotmail.com",
                "fullName": "Colleen Heath",
                "name": "Jenny292",
                "orcidId": "19931",
            },
        },
    ],
}
INVESTIGATION_1_PARAMETERS = {
    "parameters": [
        {
            "id": 1,
            "error": 4135.0,
            "numericValue": 38.0,
            "rangeBottom": 17.0,
            "rangeTop": 57.0,
            "type": {
                "applicableToDataCollection": True,
                "applicableToDatafile": True,
                "applicableToDataset": True,
                "applicableToInvestigation": True,
                "applicableToSample": True,
                "description": (
                    "Tv shake population. City she third find realize support.\n"
                    "Red say organization task. Whether number computer economy design now serious appear. "
                    "Response girl middle close role American."
                ),
                "enforced": True,
                "id": 9,
                "maximumNumericValue": 60.0,
                "minimumNumericValue": 2.0,
                "name": "PARAMETERTYPE 9",
                "units": "unit 9",
                "unitsFullName": "where",
                "valueType": "NUMERIC",
                "verified": True,
            },
        },
    ],
}
INVESTIGATION_1_PUBLICATIONS = {
    "publications": [
        {
            "id": 59,
            "doi": "1-326-70532-6",
            "fullReference": (
                "Simple notice since view check over through there. "
                "Hotel provide available a air avoid beautiful technology."
            ),
            "repository": "http://www.dillon.info/app/blog/explore/post.htm",
            "repositoryId": "5145083",
            "url": "https://www.roberts.org/",
        },
        {
            "id": 118,
            "doi": "1-5142-4022-X",
            "fullReference": (
                "Him by easy color factor per campaign training. Herself direction big reach high ahead happen hit.\n"
                "Seek describe letter detail Congress either different unit. Buy community doctor."
            ),
            "repository": "https://www.phillips-jones.com/posts/index.php",
            "repositoryId": "4437825",
            "url": "http://www.jackson.com/",
        },
        {
            "id": 177,
            "doi": "0-920183-44-1",
            "fullReference": (
                "Occur how teach. Last fine organization single.\nThose vote possible boy. West thus top right."
            ),
            "repository": "http://ware-peterson.com/category/faq.php",
            "repositoryId": "13298920",
            "url": "http://swanson.com/",
        },
    ],
}
INVESTIGATION_1_SAMPLES = {
    "samples": [
        {
            "id": 1,
            "name": "SAMPLE 1",
            "type": {
                "id": 18,
                "molecularFormula": "13133",
                "name": "SAMPLETYPE 18",
                "safetyInformation": (
                    "Individual five evening see minute across. Chance trial for foreign. Later evidence law hair.\n"
                    "Two soon care model. Table edge early off full wrong someone. I let woman mother cold chance."
                ),
            },
        },
    ],
}
DATASET_1 = {
    "complete": True,
    "description": (
        "Suggest shake effort many last prepare small. Maintain throw hope parent.\n"
        "Entire soon option bill fish against power.\nRather why rise month shake voice."
    ),
    "doi": "0-449-78690-0",
    "endDate": "2000-07-05T00:00:00Z",
    "fileCount": 15,
    "fileSize": 0,
    "id": 1,
    "location": "/international/subject.tiff",
    "name": "DATASET 1",
    "startDate": "2000-05-07T00:00:00Z",
}
DATASET_1_TYPE = {
    "type": {
        "description": (
            "Stop prove field onto think suffer measure. Table lose season identify professor happen third simply. "
            "Beat professional blue clear style have.\nAnalysis reflect work or hour color maybe."
        ),
        "id": 2,
        "name": "DATASETTYPE 2",
    },
}
DATAFILE_1190 = {
    "checksum": "fb4255d735510dbfeca7654ac2f6dff9",
    "datafileCreateTime": ANY,
    "datafileModTime": ANY,
    "description": "Company mother month service message this. Site structure state it itself.",
    "doi": "0-85288-758-2",
    "fileSize": 155061161,
    "id": 1190,
    "location": "/too/lawyer/camera.jpg",
    "name": "Datafile 1190",
}


class TestInstruments:
    def test_get_instruments(self, test_client: TestClient, valid_icat_credentials_header: dict[str, str]) -> None:
        response = test_client.get(
            url="/read-only-api/instruments",
            params={
                "where": json.dumps(
                    {"name": {"like": "INSTRUMENT"}, "fullName": {"ilike": "analysis"}, "type": {"eq": "1"}},
                ),
                "order": "type asc",
                "include": ["instrumentScientists.user"],
            },
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == [INSTRUMENT_1]

    def test_count_instruments(self, test_client: TestClient, valid_icat_credentials_header: dict[str, str]) -> None:
        response = test_client.get(
            url="/read-only-api/instruments/count",
            params={
                "where": json.dumps(
                    {"name": {"like": "INSTRUMENT"}, "fullName": {"ilike": "analysis"}, "type": {"eq": "1"}},
                ),
            },
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == 1

    def test_get_instrument(self, test_client: TestClient, valid_icat_credentials_header: dict[str, str]) -> None:
        response = test_client.get(
            url="/read-only-api/instruments/1",
            params={"include": ["instrumentScientists.user"]},
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == INSTRUMENT_1


class TestFacilityCycles:
    def test_get_facility_cycles(self, test_client: TestClient, valid_icat_credentials_header: dict[str, str]) -> None:
        response = test_client.get(
            url="/read-only-api/facilitycycles",
            params={
                "distinct": ["id", "name", "startDate", "endDate"],
                "where": json.dumps(
                    {"name": {"like": "2000"}, "startDate": {"isnull": False}, "endDate": {"isnull": False}},
                ),
                "order": "startDate asc",
            },
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == [
            {
                "endDate": "2000-07-10T00:00:00Z",
                "id": 1,
                "name": "2000 cycle 2",
                "startDate": "2000-04-02T00:00:00Z",
            },
            {
                "endDate": "2000-09-15T00:00:00Z",
                "id": 2,
                "name": "2000 cycle 3",
                "startDate": "2000-06-03T00:00:00Z",
            },
            {
                "endDate": "2000-11-20T00:00:00Z",
                "id": 3,
                "name": "2000 cycle 4",
                "startDate": "2000-08-04T00:00:00Z",
            },
        ]

    def test_count_facility_cycles(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
    ) -> None:
        response = test_client.get(
            url="/read-only-api/facilitycycles/count",
            params={
                "distinct": ["id", "name", "startDate", "endDate"],
                "where": json.dumps(
                    {"name": {"like": "2000"}, "startDate": {"isnull": False}, "endDate": {"isnull": False}},
                ),
            },
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == 3

    def test_get_facility_cycle(self, test_client: TestClient, valid_icat_credentials_header: dict[str, str]) -> None:
        response = test_client.get(
            url="/read-only-api/facilitycycles/1",
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == {
            "description": (
                "Suggest shake effort many last prepare small. Maintain throw hope parent.\n"
                "Entire soon option bill fish against power.\nRather why rise month shake voice."
            ),
            "endDate": "2000-07-10T00:00:00Z",
            "id": 1,
            "name": "2000 cycle 2",
            "startDate": "2000-04-02T00:00:00Z",
        }


class TestDataPublications:
    @pytest.mark.parametrize(
        ["include"],
        [
            pytest.param(
                [
                    "facility",
                    "type",
                    "dates",
                    "relatedItems.publication",
                    "users.user",
                    "users.affiliations",
                    "content.dataCollectionInvestigations.investigation.datasets.type",
                    "content.dataCollectionInvestigations.investigation.investigationInstruments.instrument",
                    "content.dataCollectionInvestigations.investigation.investigationUsers.user",
                    "content.dataCollectionDatasets.dataset",
                    "content.dataCollectionDatafiles.datafile",
                ],
                id="strings",
            ),
            pytest.param(
                json.dumps(
                    [
                        "facility",
                        "type",
                        "dates",
                        {"relatedItems": "publication"},
                        {"users": ["user", "affiliations"]},
                        {
                            "content": {
                                "dataCollectionInvestigations": {
                                    "investigation": {
                                        "datasets": "type",
                                        "investigationInstruments": "instrument",
                                        "investigationUsers": "user",
                                    },
                                },
                                "dataCollectionDatasets": "dataset",
                                "dataCollectionDatafiles": "datafile",
                            },
                        },
                    ],
                ),
                id="json.dumps",
            ),
        ],
    )
    def test_get_data_publications(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
        include: list,
    ) -> None:
        response = test_client.get(
            url="/read-only-api/datapublications",
            params={
                "where": json.dumps(
                    {
                        "title": {"like": "Suggest"},
                        "pid": {"like": "6828"},
                        "publicationDate": {"isnull": False},
                        "users.user.name": {"eq": "Jenny292"},
                        "users.orderKey": {"neq": "0"},
                        "relatedItems.relationType": {"eq": "References"},
                        "relatedItems.identifier": {"eq": "0-316-07926-X"},
                    },
                ),
                "order": "publicationDate asc",
                "include": include,
            },
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == [DATA_PUBLICATION_1]

    def test_count_data_publications(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
    ) -> None:
        response = test_client.get(
            url="/read-only-api/datapublications/count",
            params={
                "distinct": ["id", "title", "pid"],
                "where": json.dumps(
                    {
                        "title": {"like": "Suggest"},
                        "pid": {"like": "6828"},
                        "publicationDate": {"isnull": False},
                        "users.user.name": {"eq": "Jenny292"},
                        "users.orderKey": {"neq": "0"},
                        "relatedItems.relationType": {"eq": "References"},
                        "relatedItems.identifier": {"eq": "0-316-07926-X"},
                    },
                ),
            },
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == 1

    def test_get_data_publication(self, test_client: TestClient, valid_icat_credentials_header: dict[str, str]) -> None:
        response = test_client.get(
            url="/read-only-api/datapublications/1",
            params={
                "include": [
                    "facility",
                    "type",
                    "dates",
                    "relatedItems.publication",
                    "users.user",
                    "users.affiliations",
                    "content.dataCollectionInvestigations.investigation.datasets.type",
                    "content.dataCollectionInvestigations.investigation.investigationInstruments.instrument",
                    "content.dataCollectionInvestigations.investigation.investigationUsers.user",
                    "content.dataCollectionDatasets.dataset",
                    "content.dataCollectionDatafiles.datafile",
                ],
            },
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == DATA_PUBLICATION_1


class TestInvestigations:
    @pytest.mark.parametrize(
        ["params", "body"],
        [
            pytest.param(
                {
                    "where": json.dumps(
                        {
                            "name": {"like": "INVESTIGATION"},
                            "title": {"ilike": "analysis"},
                            "visitId": {"between": ["69", "71"]},
                            "startDate": {"gt": "2000-01-01 00:00:00"},
                            "endDate": {"lt": "2001-01-01 00:00:00"},
                            "investigationInstruments.instrument.name": {"nilike": "1"},
                        },
                    ),
                    "order": "name asc",
                    "include": [
                        "investigationInstruments.instrument",
                        "investigationUsers.user",
                        "samples.type",
                        "parameters.type",
                        "publications",
                    ],
                },
                [
                    {
                        **INVESTIGATION_1,
                        **INVESTIGATION_1_INVESTIGATION_INSTRUMENTS,
                        **INVESTIGATION_1_INVESTIGATION_USERS,
                        **INVESTIGATION_1_PARAMETERS,
                        **INVESTIGATION_1_PUBLICATIONS,
                        **INVESTIGATION_1_SAMPLES,
                    },
                ],
            ),
            pytest.param(
                {"distinct": ["name", "title"], "skip": 10, "limit": 3},
                [
                    {
                        "name": "INVESTIGATION 11",
                        "title": (
                            "Quite world game over million. Business get box.\n"
                            "American back right billion first especially anyone. Bad understand head.\n"
                            "Quickly event middle focus. Good sound political successful."
                        ),
                    },
                    {
                        "name": "INVESTIGATION 12",
                        "title": (
                            "Dream none group city since trouble finish they. "
                            "Effect personal together trouble pay increase."
                        ),
                    },
                    {
                        "name": "INVESTIGATION 13",
                        "title": (
                            "Again teacher letter. Coach card no step side PM.\n"
                            "Network recognize recognize space many everything. Else evidence compare return. "
                            "Room from central effort."
                        ),
                    },
                ],
            ),
        ],
    )
    def test_get_investigations(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
        params: dict,
        body: list[dict],
    ) -> None:
        response = test_client.get(
            url="/read-only-api/investigations",
            params=params,
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == body

    def test_count_investigations(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
    ) -> None:
        response = test_client.get(
            url="/read-only-api/investigations/count",
            params={
                "where": json.dumps(
                    {
                        "name": {"like": "INVESTIGATION"},
                        "title": {"ilike": "analysis"},
                        "visitId": {"between": ["69", "71"]},
                        "startDate": {"gt": "2000-01-01 00:00:00"},
                        "endDate": {"lt": "2001-01-01 00:00:00"},
                        "investigationInstruments.instrument.name": {"nilike": "1"},
                    },
                ),
            },
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == 1

    def test_find_one_investigation(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
    ) -> None:
        response = test_client.get(
            url="/read-only-api/investigations/findone",
            params={"where": json.dumps({"name": {"eq": "INVESTIGATION 1"}})},
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == INVESTIGATION_1

    @pytest.mark.parametrize(
        ["includes", "included_body"],
        [
            pytest.param([], {}),
            pytest.param(["investigationInstruments.instrument"], INVESTIGATION_1_INVESTIGATION_INSTRUMENTS),
            pytest.param(["investigationUsers.user"], INVESTIGATION_1_INVESTIGATION_USERS),
            pytest.param(["samples.type"], INVESTIGATION_1_SAMPLES),
            pytest.param(["parameters.type"], INVESTIGATION_1_PARAMETERS),
            pytest.param(["publications"], INVESTIGATION_1_PUBLICATIONS),
        ],
    )
    def test_get_investigation(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
        includes: int,
        included_body: dict,
    ) -> None:
        response = test_client.get(
            url="/read-only-api/investigations/1",
            params={"include": includes},
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == {**INVESTIGATION_1, **included_body}

    @pytest.mark.parametrize(
        ["includes", "included_body"],
        [pytest.param([], {}), pytest.param(["type"], DATASET_1_TYPE)],
    )
    def test_get_datasets(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
        includes: list[str],
        included_body: dict,
    ) -> None:
        response = test_client.get(
            url="/read-only-api/investigations/1/datasets",
            params={
                "where": json.dumps(
                    {"name": {"nlike": "61"}, "createTime": {"isnull": False}, "modTime": {"isnull": False}},
                ),
                "include": includes,
            },
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == [{**DATASET_1, **included_body}]


class TestDatasets:
    def test_get_datasets(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
    ) -> None:
        response = test_client.get(
            url="/read-only-api/datasets",
            params={
                "where": json.dumps(
                    {
                        "id": {"eq": "1"},
                        "investigation.id": {"eq": "1"},
                        "name": {"ilike": "dataset"},
                        "createTime": {"isnull": False},
                        "modTime": {"isnull": False},
                    },
                ),
            },
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == [DATASET_1]

    def test_count_datasets(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
    ) -> None:
        response = test_client.get(
            url="/read-only-api/datasets/count",
            params={
                "where": json.dumps(
                    {
                        "id": {"eq": "1"},
                        "investigation.id": {"eq": "1"},
                        "name": {"ilike": "dataset"},
                        "createTime": {"isnull": False},
                        "modTime": {"isnull": False},
                    },
                ),
            },
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == 1

    def test_find_one_dataset(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
    ) -> None:
        response = test_client.get(
            url="/read-only-api/datasets/findone",
            params={"where": json.dumps({"id": {"eq": "1"}, "investigation.id": {"eq": "1"}})},
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == DATASET_1

    @pytest.mark.parametrize(
        ["includes", "included_body"],
        [pytest.param([], {}), pytest.param(["type"], DATASET_1_TYPE)],
    )
    def test_get_dataset(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
        includes: list[str],
        included_body: dict,
    ) -> None:
        response = test_client.get(
            url="/read-only-api/datasets/1",
            params={"include": includes},
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == {**DATASET_1, **included_body}

    def test_get_datafiles(self, test_client: TestClient, valid_icat_credentials_header: dict[str, str]) -> None:
        response = test_client.get(
            url="/read-only-api/datasets/1/datafiles",
            params={
                "where": json.dumps(
                    {"name": {"like": "1"}, "location": {"ilike": "JPG"}, "datafileCreateTime": {"isnull": False}},
                ),
                "order": "location asc",
            },
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == [DATAFILE_1190]


class TestDatafiles:
    def test_get_datafiles(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
    ) -> None:
        response = test_client.get(
            url="/read-only-api/datafiles",
            params={
                "where": json.dumps(
                    {
                        "id": {"eq": "1190"},
                        "dataset.id": {"eq": "1"},
                        "name": {"ilike": "datafile"},
                        "location": {"like": "jpg"},
                        "datafileCreateTime": {"isnull": False},
                        "datafileModTime": {"isnull": False},
                    },
                ),
            },
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == [DATAFILE_1190]

    def test_count_datafiles(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
    ) -> None:
        response = test_client.get(
            url="/read-only-api/datafiles/count",
            params={
                "where": json.dumps(
                    {
                        "id": {"eq": "1190"},
                        "dataset.id": {"eq": "1"},
                        "name": {"ilike": "datafile"},
                        "location": {"like": "jpg"},
                        "datafileCreateTime": {"isnull": False},
                        "datafileModTime": {"isnull": False},
                    },
                ),
            },
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == 1

    def test_find_one_datafile(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
    ) -> None:
        response = test_client.get(
            url="/read-only-api/datafiles/findone",
            params={"where": json.dumps({"id": {"eq": "1190"}, "dataset.id": {"eq": "1"}})},
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == DATAFILE_1190

    def test_get_datafile(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
    ) -> None:
        response = test_client.get(
            url="/read-only-api/datafiles/1190",
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == DATAFILE_1190


class TestInvestigationUsers:
    def test_get_investigation_users(
        self,
        test_client: TestClient,
        valid_icat_credentials_header: dict[str, str],
    ) -> None:
        response = test_client.get(
            url="/read-only-api/investigationusers",
            params={"distinct": "role", "where": json.dumps({"user.name": {"eq": "Jenny292"}})},
            headers=valid_icat_credentials_header,
        )
        assert response.status_code == 200, response.text
        assert response.json() == [{"role": "PI"}]
