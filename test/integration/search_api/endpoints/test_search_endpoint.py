import pytest

from datagateway_api.src.common.config import Config
from test.integration.search_api.endpoints.test_get_dataset_files import (
    prepare_data_for_assertion,
)


class TestSearchAPISearchEndpoint:
    @pytest.mark.parametrize(
        "endpoint_name, request_filter, expected_json",
        [
            pytest.param(
                "datasets",
                '{"limit": 2}',
                [
                    {
                        "pid": "1-4978-6907-2",
                        "title": "DATASET 1",
                        "isPublic": True,
                        "size": None,
                        "documents": [],
                        "techniques": [],
                        "instrument": None,
                        "files": [],
                        "parameters": [],
                        "samples": [],
                    },
                    {
                        "pid": "1-01-107043-X",
                        "title": "DATASET 2",
                        "isPublic": True,
                        "size": None,
                        "documents": [],
                        "techniques": [],
                        "instrument": None,
                        "files": [],
                        "parameters": [],
                        "samples": [],
                    },
                ],
                id="Basic /datasets request",
            ),
            pytest.param(
                "documents",
                '{"limit": 1}',
                [
                    {
                        "pid": "0-417-77631-4",
                        "isPublic": True,
                        "type": "INVESTIGATIONTYPE 3",
                        "title": "INVESTIGATION 1",
                        "summary": "Throw hope parent. Receive entire soon."
                        " War top air agent must voice high describe.\nMonth "
                        "shake voice. Do discuss despite least face again study"
                        ". Two beyond picture rich fast sea time.",
                        "doi": "0-417-77631-4",
                        "startDate": "2000-04-03T00:00:00.000Z",
                        "endDate": "2000-07-09T00:00:00.000Z",
                        "releaseDate": "2000-07-05T00:00:00.000Z",
                        "license": None,
                        "keywords": [
                            "number22",
                            "shoulder85",
                            "local117",
                            "religious242",
                            "agreement263",
                            "mention362",
                            "game469",
                            "onto480",
                            "never495",
                        ],
                        "datasets": [],
                        "members": [],
                        "parameters": [],
                    },
                ],
                id="Basic /instruments request",
            ),
            pytest.param(
                "datasets",
                '{"limit": 1, "skip": 5}',
                [
                    {
                        "pid": "1-77218-518-3",
                        "title": "DATASET 6",
                        "isPublic": True,
                        "size": None,
                        "documents": [],
                        "techniques": [],
                        "instrument": None,
                        "files": [],
                        "parameters": [],
                        "samples": [],
                    },
                ],
                id="Search datasets with skip filter",
            ),
            pytest.param(
                "instruments",
                '{"limit": 2, "where": {"name": "INSTRUMENT 10"}}',
                [
                    {
                        "datasets": [],
                        "facility": "LILS",
                        "name": "INSTRUMENT 10",
                        "pid": "pid:10",
                    },
                ],
                id="Search instruments with name condition",
            ),
            pytest.param(
                "datasets",
                '{"limit": 1, "where": {"creationDate": {"gt":'
                ' "2007-06-30T08:30:58.000Z"}}}',
                [
                    {
                        "pid": "1-4978-6907-2",
                        "title": "DATASET 1",
                        "isPublic": True,
                        "size": None,
                        "documents": [],
                        "techniques": [],
                        "instrument": None,
                        "files": [],
                        "parameters": [],
                        "samples": [],
                    },
                ],
                id="Search datasets with creation date filter (operator specified)",
            ),
            pytest.param(
                "datasets",
                '{"include": [{"relation": "documents"}, {"relation": "techniques"},'
                ' {"relation": "instrument"}, {"relation": "files"},'
                ' {"relation": "parameters"}, {"relation": "samples"}], "limit": 1}',
                [{}],
                id="Search datasets including all possible related entities",
                # Skipped because ICAT 5 mapping on techniques and instrument
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "documents",
                '{"include": [{"relation": "datasets"}, {"relation": "members"},'
                ' {"relation": "parameters"}], "limit": 1}',
                [
                    {
                        "pid": "0-417-77631-4",
                        "isPublic": True,
                        "type": "INVESTIGATIONTYPE 3",
                        "title": "INVESTIGATION 1",
                        "summary": "Throw hope parent. Receive entire soon."
                        " War top air agent must voice high describe.\nMonth"
                        " shake voice. Do discuss despite least face again "
                        "study. Two beyond picture rich fast sea time.",
                        "doi": "0-417-77631-4",
                        "startDate": "2000-04-03T00:00:00.000Z",
                        "endDate": "2000-07-09T00:00:00.000Z",
                        "releaseDate": "2000-07-05T00:00:00.000Z",
                        "license": None,
                        "keywords": [
                            "number22",
                            "shoulder85",
                            "local117",
                            "religious242",
                            "agreement263",
                            "mention362",
                            "game469",
                            "onto480",
                            "never495",
                        ],
                        "datasets": [
                            {
                                "pid": "1-4978-6907-2",
                                "title": "DATASET 1",
                                "isPublic": True,
                                "size": None,
                                "documents": [],
                                "techniques": [],
                                "instrument": None,
                                "files": [],
                                "parameters": [],
                                "samples": [],
                            },
                            {
                                "pid": "0-557-36716-6",
                                "title": "DATASET 61",
                                "isPublic": True,
                                "size": None,
                                "documents": [],
                                "techniques": [],
                                "instrument": None,
                                "files": [],
                                "parameters": [],
                                "samples": [],
                            },
                        ],
                        "members": [
                            {
                                "id": "1",
                                "role": "PI",
                                "document": None,
                                "person": None,
                                "affiliation": None,
                            },
                        ],
                        "parameters": [
                            {
                                "id": "1",
                                "name": "PARAMETERTYPE 9",
                                "value": 38,
                                "unit": "unit 9",
                                "dataset": None,
                                "document": None,
                            },
                        ],
                    },
                ],
                id="Search documents including all possible related entities",
            ),
            pytest.param(
                "instruments",
                '{"include": [{"relation": "datasets"}], "limit": 1}',
                {
                    "description": "Former outside source play nearly Congress before"
                    " necessary. Allow want audience test laugh. Economic body person"
                    " general attorney. Effort weight prevent possible.",
                    "modId": "user",
                    "createTime": "2019-02-19 05:57:03.000Z",
                    "pid": None,
                    "createId": "user",
                    "type": "2",
                    "name": "INSTRUMENT 2",
                    "modTime": "2019-01-29 23:33:20.000Z",
                    "id": 2,
                    "fullName": "With piece reason late model. House office fly."
                    " International scene call deep answer audience baby True.\n"
                    "Indicate education across these. Opportunity design too.",
                    "url": "https://moore.org/",
                },
                id="Search instruments including all possible related entities",
                # Skipped due to ICAT 5 mapping
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "datasets",
                '{"where":{"isPublic": {"eq": "True"}}, "limit": 1}',
                [
                    {
                        "pid": "1-4978-6907-2",
                        "title": "DATASET 1",
                        "isPublic": True,
                        "size": None,
                        "documents": [],
                        "techniques": [],
                        "instrument": None,
                        "files": [],
                        "parameters": [],
                        "samples": [],
                    },
                ],
                id="Search datasets with isPublic condition (True)",
            ),
            pytest.param(
                "datasets",
                '{"where": {"isPublic": false}}',
                [],
                id="Search datasets with isPublic condition (False)",
            ),
            pytest.param(
                "datasets",
                '{"include": [{"relation": "techniques", "scope": {"where": {"name":'
                '"TODO"}}}]}',
                [],
                # Skipped because this test relies on ICAT 5 entities
                # TODO - edit the WHERE filter when we know the techniques test data
                marks=pytest.mark.skip,
                id="Search datasets with condition on techniques name (ICAT 5)",
            ),
            pytest.param(
                "datasets",
                '{"include": [{"relation": "parameters", "scope": {"where": {"and": [{'
                '"name": "PARAMETERTYPE 1"}, {"value": {"between": [0, 20]}},'
                '{"unit": "unit 1"}]}}}]}',
                [
                    {
                        "pid": "1-85271-859-5",
                        "title": "DATASET 33",
                        "isPublic": True,
                        "size": None,
                        "documents": [],
                        "techniques": [],
                        "instrument": None,
                        "files": [],
                        "parameters": [
                            {
                                "id": "1",
                                "name": "PARAMETERTYPE 1",
                                "value": 20,
                                "unit": "unit 1",
                                "dataset": None,
                                "document": None,
                            },
                            {
                                "id": "44",
                                "name": "PARAMETERTYPE 44",
                                "value": "value 44",
                                "unit": "unit 44",
                                "dataset": None,
                                "document": None,
                            },
                            {
                                "id": "49",
                                "name": "PARAMETERTYPE 49",
                                "value": "value 49",
                                "unit": "unit 49",
                                "dataset": None,
                                "document": None,
                            },
                        ],
                        "samples": [],
                    },
                ],
                id="Search datasets with parameters include and conditions (between"
                " operator, A AND B AND C)",
            ),
            pytest.param(
                "datasets",
                '{"include": [{"relation": "parameters", "scope": {"where": {"and": [{'
                '"name": "PARAMETERTYPE 39"}, {"value": {"lt": 800000}}, {"unit":'
                ' "unit 39"}]}}}]}',
                [
                    {
                        "pid": "1-71395-013-8",
                        "title": "DATASET 71",
                        "isPublic": True,
                        "size": None,
                        "documents": [],
                        "techniques": [],
                        "instrument": None,
                        "files": [],
                        "parameters": [
                            {
                                "id": "38",
                                "name": "PARAMETERTYPE 38",
                                "value": "value 38",
                                "unit": "unit 38",
                                "dataset": None,
                                "document": None,
                            },
                            {
                                "id": "39",
                                "name": "PARAMETERTYPE 39",
                                "value": 44,
                                "unit": "unit 39",
                                "dataset": None,
                                "document": None,
                            },
                        ],
                        "samples": [],
                    },
                ],
                id="Search datasets with parameters include and conditions (lt operator"
                ", A AND B AND C)",
            ),
            pytest.param(
                "datasets",
                '{"include": [{"relation": "parameters", "scope": {"where": {"or": [{'
                '"and": [{"name": "sample_state"}, {"value": "solid"}]}, {"and": [{'
                '"name": "PARAMETERTYPE 39"}, {"value": 44}]}]}}}]}',
                [
                    {
                        "pid": "1-71395-013-8",
                        "title": "DATASET 71",
                        "isPublic": True,
                        "size": None,
                        "documents": [],
                        "techniques": [],
                        "instrument": None,
                        "files": [],
                        "parameters": [
                            {
                                "id": "38",
                                "name": "PARAMETERTYPE 38",
                                "value": "value 38",
                                "unit": "unit 38",
                                "dataset": None,
                                "document": None,
                            },
                            {
                                "id": "39",
                                "name": "PARAMETERTYPE 39",
                                "value": 44,
                                "unit": "unit 39",
                                "dataset": None,
                                "document": None,
                            },
                        ],
                        "samples": [],
                    },
                ],
                id="Search datasets with parameters include and conditions ((A AND B)"
                " OR (C AND D)",
            ),
            pytest.param(
                "datasets",
                '{"include": [{"relation": "files", "scope": {"where": {"text":'
                ' "Datafile 25"}}}], "limit": 1}',
                [
                    {
                        "pid": "1-85150-280-7",
                        "title": "DATASET 13",
                        "isPublic": True,
                        "size": None,
                        "documents": [],
                        "techniques": [],
                        "instrument": None,
                        "files": [
                            {
                                "id": "1083",
                                "name": "Datafile 1083",
                                "path": "/thousand/hour/most.gif",
                                "size": 8025793,
                                "dataset": None,
                            },
                            {
                                "id": "12",
                                "name": "Datafile 12",
                                "path": "/ask/not/also.bmp",
                                "size": 124256016,
                                "dataset": None,
                            },
                            {
                                "id": "1202",
                                "name": "Datafile 1202",
                                "path": "/second/free/reach.png",
                                "size": 3628023,
                                "dataset": None,
                            },
                            {
                                "id": "131",
                                "name": "Datafile 131",
                                "path": "/although/partner/include.png",
                                "size": 71810603,
                                "dataset": None,
                            },
                            {
                                "id": "1321",
                                "name": "Datafile 1321",
                                "path": "/simple/game/loss.png",
                                "size": 134622872,
                                "dataset": None,
                            },
                            {
                                "id": "1440",
                                "name": "Datafile 1440",
                                "path": "/student/in/wide.tiff",
                                "size": 13715483,
                                "dataset": None,
                            },
                            {
                                "id": "1559",
                                "name": "Datafile 1559",
                                "path": "/start/change/prepare.jpeg",
                                "size": 66656703,
                                "dataset": None,
                            },
                            {
                                "id": "1678",
                                "name": "Datafile 1678",
                                "path": "/amount/building/least.gif",
                                "size": 16593025,
                                "dataset": None,
                            },
                            {
                                "id": "1797",
                                "name": "Datafile 1797",
                                "path": "/talk/attention/nature.bmp",
                                "size": 32738241,
                                "dataset": None,
                            },
                            {
                                "id": "250",
                                "name": "Datafile 250",
                                "path": "/call/vote/and.bmp",
                                "size": 107218026,
                                "dataset": None,
                            },
                            {
                                "id": "369",
                                "name": "Datafile 369",
                                "path": "/party/recent/ever.jpeg",
                                "size": 123486563,
                                "dataset": None,
                            },
                            {
                                "id": "488",
                                "name": "Datafile 488",
                                "path": "/method/arrive/body.bmp",
                                "size": 58049109,
                                "dataset": None,
                            },
                            {
                                "id": "607",
                                "name": "Datafile 607",
                                "path": "/several/message/simply.tiff",
                                "size": 179118921,
                                "dataset": None,
                            },
                            {
                                "id": "726",
                                "name": "Datafile 726",
                                "path": "/stand/expert/federal.jpg",
                                "size": 171349673,
                                "dataset": None,
                            },
                            {
                                "id": "845",
                                "name": "Datafile 845",
                                "path": "/present/want/baby.bmp",
                                "size": 204579388,
                                "dataset": None,
                            },
                            {
                                "id": "964",
                                "name": "Datafile 964",
                                "path": "/international/wish/air.jpg",
                                "size": 53688522,
                                "dataset": None,
                            },
                        ],
                        "parameters": [],
                        "samples": [],
                    },
                ],
                id="Search datasets' files using full text search",
            ),
            pytest.param(
                "documents",
                '{"where": {"type": "INVESTIGATIONTYPE 2"}, "include": [{"relation":'
                '"datasets"}, {"relation": "members", "scope": {"where": {"role": "PI"'
                '}, "include": [{"relation": "person", "scope": {"where": {"fullName":'
                '"Sarah Griffin"}}}]}}]}',
                [
                    {
                        "pid": "1-903289-21-1",
                        "isPublic": True,
                        "type": "INVESTIGATIONTYPE 2",
                        "title": "INVESTIGATION 2",
                        "summary": "Allow want audience test laugh."
                        " Economic body person general attorney. Effort"
                        " weight prevent possible.\nReflect market box "
                        "find gas someone election. Tonight member decide"
                        " paper stage.",
                        "doi": "1-903289-21-1",
                        "startDate": "2000-06-04T00:00:00.000Z",
                        "endDate": "2000-09-14T00:00:00.000Z",
                        "releaseDate": "2000-02-10T00:00:00.000Z",
                        "license": None,
                        "keywords": [
                            "allow20",
                            "she26",
                            "figure34",
                            "significant67",
                            "plan104",
                            "trip116",
                            "technology140",
                            "down141",
                            "range152",
                            "father189",
                            "discussion299",
                            "mention349",
                            "own352",
                            "particular435",
                        ],
                        "datasets": [],
                        "members": [
                            {
                                "id": "2",
                                "role": "PI",
                                "document": None,
                                "person": {
                                    "id": "131",
                                    "fullName": "Sarah Griffin",
                                    "orcid": "18718",
                                    "researcherId": None,
                                    "firstName": None,
                                    "lastName": None,
                                    "members": [],
                                },
                                "affiliation": None,
                            },
                        ],
                        "parameters": [],
                    },
                ],
                id="Search documents with document condition, multiple includes"
                " (nested) and conditions on those with parameters include and"
                " conditions",
            ),
            pytest.param(
                "documents",
                '{"include": [{"relation": "parameters", "scope": {"where": {"and": [{'
                '"name": "PARAMETERTYPE 2"}, {"value": {"between": [23, 55]}},'
                '{"unit": "unit 2"}]}}}]}',
                [
                    {
                        "pid": "0-525-94351-X",
                        "isPublic": True,
                        "type": "INVESTIGATIONTYPE 2",
                        "title": "INVESTIGATION 4",
                        "summary": "Often other each after during authority"
                        " necessary audience. Again act seek grow. Television"
                        " child may some baby we community.\nStart floor blood"
                        " method. Fall throw center treat all firm total"
                        " sound.",
                        "doi": "0-525-94351-X",
                        "startDate": "2001-02-02T00:00:00.000Z",
                        "endDate": "2001-05-04T00:00:00.000Z",
                        "releaseDate": "2001-09-26T00:00:00.000Z",
                        "license": None,
                        "keywords": ["coach336", "discuss378", "stay400"],
                        "datasets": [],
                        "members": [],
                        "parameters": [
                            {
                                "id": "4",
                                "name": "PARAMETERTYPE 2",
                                "value": 55,
                                "unit": "unit 2",
                                "dataset": None,
                                "document": None,
                            },
                        ],
                    },
                ],
                id="Search documents with parameters include and conditions (between"
                " operator, A AND B AND C)",
            ),
            pytest.param(
                "documents",
                '{"include": [{"relation": "datasets", "scope": {"include": [{'
                '"relation": "parameters", "scope": {"where": {"and": [{"name":'
                ' "PARAMETERTYPE 2"}, {"value": {"between": [15, 22]}}, {'
                '"unit": "unit 2"}]}}}]}}]}',
                [
                    {
                        "pid": "0-417-77631-4",
                        "isPublic": True,
                        "type": "INVESTIGATIONTYPE 3",
                        "title": "INVESTIGATION 1",
                        "summary": "Throw hope parent. Receive entire soon."
                        " War top air agent must voice high describe.\nMonth "
                        "shake voice. Do discuss despite least face "
                        "again study. Two beyond picture rich fast sea time.",
                        "doi": "0-417-77631-4",
                        "startDate": "2000-04-03T00:00:00.000Z",
                        "endDate": "2000-07-09T00:00:00.000Z",
                        "releaseDate": "2000-07-05T00:00:00.000Z",
                        "license": None,
                        "keywords": [
                            "number22",
                            "shoulder85",
                            "local117",
                            "religious242",
                            "agreement263",
                            "mention362",
                            "game469",
                            "onto480",
                            "never495",
                        ],
                        "datasets": [
                            {
                                "pid": "1-4978-6907-2",
                                "title": "DATASET 1",
                                "isPublic": True,
                                "size": None,
                                "documents": [],
                                "techniques": [],
                                "instrument": None,
                                "files": [],
                                "parameters": [
                                    {
                                        "id": "30",
                                        "name": "PARAMETERTYPE 30",
                                        "value": 23,
                                        "unit": "unit 30",
                                        "dataset": None,
                                        "document": None,
                                    },
                                ],
                                "samples": [],
                            },
                            {
                                "pid": "0-557-36716-6",
                                "title": "DATASET 61",
                                "isPublic": True,
                                "size": None,
                                "documents": [],
                                "techniques": [],
                                "instrument": None,
                                "files": [],
                                "parameters": [
                                    {
                                        "id": "2",
                                        "name": "PARAMETERTYPE 2",
                                        "value": 21,
                                        "unit": "unit 2",
                                        "dataset": None,
                                        "document": None,
                                    },
                                ],
                                "samples": [],
                            },
                        ],
                        "members": [],
                        "parameters": [],
                    },
                ],
                id="Search documents with datasets.parameters include and conditions"
                " (between operator, A AND B AND C)",
            ),
            pytest.param(
                "datasets",
                '{"include": [{"relation": "datasets", "scope": {"include": [{'
                '"relation": "samples", "scope": {"where": {"name": "SAMPLE 4"}}}, {'
                '"relation": "techniques", "scope": {"where": {"name": "TODO"}}}]}}]}',
                [
                    {
                        "pid": "0-9634101-9-9",
                        "isPublic": True,
                        "type": "INVESTIGATIONTYPE 3",
                        "title": "INVESTIGATION 4",
                        "summary": "Fast purpose right power away health south.\n"
                        "Quality serve food buy responsibility go much. Situation raise"
                        " manage positive help daughter. Yes player reveal.",
                        "doi": "0-9634101-9-9",
                        "startDate": "2001-02-02T00:00:00.000Z",
                        "endDate": "2001-05-04T00:00:00.000Z",
                        "releaseDate": "2001-09-26T00:00:00.000Z",
                        "license": None,
                        "keywords": [
                            "pressure133",
                            "property392",
                            "development707",
                            "field849",
                            "very1485",
                            "ready1552",
                            "laugh1693",
                            "explain1835",
                            "every2547",
                            "answer2893",
                            "relationship3108",
                            "lot3281",
                            "start3507",
                            "later3670",
                            "around3919",
                            "new4134",
                            "cut4496",
                            "seem4587",
                            "four5078",
                            "wind5584",
                            "year5683",
                            "church5824",
                            "toward6051",
                            "door6313",
                            "involve6542",
                            "message6681",
                            "day7103",
                            "in8803",
                            "between8933",
                            "lead8947",
                            "same8992",
                            "establish9806",
                            "lay10219",
                            "institution10406",
                            "artist10468",
                            "analysis10524",
                            "education10886",
                            "score10895",
                            "price10909",
                            "risk11637",
                            "economy12679",
                            "mouth12746",
                            "control13332",
                            "join13453",
                            "visit13664",
                            "middle13751",
                            "quickly14383",
                            "receive14492",
                            "hour14512",
                            "include14664",
                            "likely14872",
                        ],
                        "datasets": [
                            {
                                "pid": "1-937941-39-6",
                                "title": "DATASET 244",
                                "isPublic": True,
                                "size": None,
                                "documents": [],
                                "techniques": [],
                                "instrument": None,
                                "files": [],
                                "parameters": [],
                                "samples": [
                                    {
                                        "name": "SAMPLE 4",
                                        "pid": "pid:4",
                                        "description": "I read painting decade. Down"
                                        " free attention recognize travel.",
                                        "datasets": [],
                                    },
                                ],
                            },
                            {
                                "pid": "1-397-29815-4",
                                "title": "DATASET 4",
                                "isPublic": True,
                                "size": None,
                                "documents": [],
                                "techniques": [],
                                "instrument": None,
                                "files": [],
                                "parameters": [],
                                "samples": [
                                    {
                                        "name": "SAMPLE 4",
                                        "pid": "pid:4",
                                        "description": "I read painting decade. Down"
                                        " free attention recognize travel.",
                                        "datasets": [],
                                    },
                                ],
                            },
                        ],
                        "members": [],
                        "parameters": [],
                    },
                ],
                # Skipped because this relies on ICAT 5 mappings
                # TODO - techniques WHERE filter needs finishing when we know what the
                # test data will be
                marks=pytest.mark.skip,
                id="Search documents with multiple include and scopes (ICAT 5)",
            ),
        ],
    )
    def test_valid_search_endpoint(
        self, flask_test_app_search_api, endpoint_name, request_filter, expected_json,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/{endpoint_name}?filter="
            f"{request_filter}",
        )

        response_data = prepare_data_for_assertion(test_response.json)

        assert response_data == expected_json

    @pytest.mark.parametrize(
        "request_filter, expected_status_code",
        [
            pytest.param('{"where": []}', 400, id="Bad where filter"),
            pytest.param('{"limit": -1}', 400, id="Bad limit filter"),
            pytest.param('{"skip": -100}', 400, id="Bad skip filter"),
            pytest.param('{"include": ""}', 400, id="Bad include filter"),
        ],
    )
    def test_invalid_search_endpoint(
        self, flask_test_app_search_api, request_filter, expected_status_code,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/instruments?filter={request_filter}",
        )

        assert test_response.status_code == expected_status_code
