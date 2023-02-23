import pytest

from datagateway_api.src.common.config import Config
from test.integration.search_api.endpoints.test_get_dataset_files import (
    prepare_data_for_assertion,
)


class TestSearchAPIGetByPIDEndpoint:
    @pytest.mark.parametrize(
        "endpoint_name, pid, request_filter, expected_json",
        [
            pytest.param(
                "Datasets",
                "1-4978-6907-2",
                "{}",
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
                id="Basic /Datasets/{pid} request",
            ),
            pytest.param(
                "Documents",
                "0-417-77631-4",
                "{}",
                {
                    "pid": "0-417-77631-4",
                    "isPublic": True,
                    "type": "INVESTIGATIONTYPE 3",
                    "title": "INVESTIGATION 1",
                    "summary": "Throw hope parent. Receive entire soon. "
                    "War top air agent must voice high describe.\nMonth shake "
                    "voice. Do discuss despite least face again study. Two "
                    "beyond picture rich fast sea time.",
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
                id="Basic /Documents/{pid} request",
            ),
            pytest.param(
                "Instruments",
                "pid:2",
                "{}",
                {
                    "pid": "pid:2",
                    "name": "INSTRUMENT 2",
                    "facility": "LILS",
                    "datasets": [],
                },
                id="Basic /Instruments/{pid} request",
            ),
            pytest.param(
                "Datasets",
                "1-4978-6907-2",
                '{"include": [{"relation": "documents"}]}',
                {
                    "pid": "1-4978-6907-2",
                    "title": "DATASET 1",
                    "isPublic": True,
                    "size": None,
                    "documents": [
                        {
                            "pid": "0-417-77631-4",
                            "isPublic": True,
                            "type": "INVESTIGATIONTYPE 3",
                            "title": "INVESTIGATION 1",
                            "summary": "Throw hope parent. Receive entire "
                            "soon. War top air agent must voice high describe."
                            "\nMonth shake voice. Do discuss despite least "
                            "face again study. Two beyond picture rich "
                            "fast sea time.",
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
                    "techniques": [],
                    "instrument": None,
                    "files": [],
                    "parameters": [],
                    "samples": [],
                },
                id="Get dataset by pid with include filter",
            ),
            pytest.param(
                "Documents",
                "0-417-77631-4",
                '{"include": [{"relation": "datasets"}]}',
                {
                    "pid": "0-417-77631-4",
                    "isPublic": True,
                    "type": "INVESTIGATIONTYPE 3",
                    "title": "INVESTIGATION 1",
                    "summary": "Throw hope parent. Receive entire soon. "
                    "War top air agent must voice high describe.\nMonth "
                    "shake voice. Do discuss despite least face again study. "
                    "Two beyond picture rich fast sea time.",
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
                    "members": [],
                    "parameters": [],
                },
                id="Get document by pid with include filter",
            ),
            pytest.param(
                "Instruments",
                "2",
                '{"include": [{"relation": "datasets"}]}',
                {
                    "description": "Former outside source play nearly Congress before"
                    " necessary. Allow want audience test laugh. Economic body person"
                    " general attorney. Effort weight prevent possible.",
                    "modId": "user",
                    "createTime": "2019-02-19 05:57:03+00:00",
                    "pid": None,
                    "createId": "user",
                    "type": "2",
                    "name": "INSTRUMENT 2",
                    "modTime": "2019-01-29 23:33:20+00:00",
                    "id": 2,
                    "fullName": "With piece reason late model. House office fly."
                    " International scene call deep answer audience baby True.\n"
                    "Indicate education across these. Opportunity design too.",
                    "url": "https://moore.org/",
                },
                id="Get instrument by pid with include filter",
                # Skipped due to ICAT 5 mapping
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "Datasets",
                "1-4978-6907-2",
                '{"include": [{"relation": "documents"},'
                ' {"relation": "files"}, {"relation": "parameters"},'
                ' {"relation": "samples"}]}',
                {
                    "pid": "1-4978-6907-2",
                    "title": "DATASET 1",
                    "isPublic": True,
                    "size": None,
                    "documents": [
                        {
                            "pid": "0-417-77631-4",
                            "isPublic": True,
                            "type": "INVESTIGATIONTYPE 3",
                            "title": "INVESTIGATION 1",
                            "summary": "Throw hope parent. Receive entire "
                            "soon."
                            " War top air agent must voice high describe.\n"
                            "Month shake voice. Do discuss despite least face"
                            " again study. Two beyond picture rich fast "
                            "sea time.",
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
                    "techniques": [],
                    "instrument": None,
                    "files": [
                        {
                            "id": "1071",
                            "name": "Datafile 1071",
                            "path": "/sense/through/candidate.jpeg",
                            "size": 9390543,
                            "dataset": None,
                        },
                        {
                            "id": "119",
                            "name": "Datafile 119",
                            "path": "/five/with/question.bmp",
                            "size": 124185509,
                            "dataset": None,
                        },
                        {
                            "id": "1190",
                            "name": "Datafile 1190",
                            "path": "/too/lawyer/camera.jpg",
                            "size": 155061161,
                            "dataset": None,
                        },
                        {
                            "id": "1309",
                            "name": "Datafile 1309",
                            "path": "/writer/family/pull.bmp",
                            "size": 171717920,
                            "dataset": None,
                        },
                        {
                            "id": "1428",
                            "name": "Datafile 1428",
                            "path": "/I/collection/population.png",
                            "size": 6316615,
                            "dataset": None,
                        },
                        {
                            "id": "1547",
                            "name": "Datafile 1547",
                            "path": "/training/value/share.gif",
                            "size": 80936756,
                            "dataset": None,
                        },
                        {
                            "id": "1666",
                            "name": "Datafile 1666",
                            "path": "/able/leg/policy.gif",
                            "size": 43253880,
                            "dataset": None,
                        },
                        {
                            "id": "1785",
                            "name": "Datafile 1785",
                            "path": "/kind/rest/who.tiff",
                            "size": 113394018,
                            "dataset": None,
                        },
                        {
                            "id": "238",
                            "name": "Datafile 238",
                            "path": "/tough/former/one.tiff",
                            "size": 104571616,
                            "dataset": None,
                        },
                        {
                            "id": "357",
                            "name": "Datafile 357",
                            "path": "/official/yard/father.tiff",
                            "size": 11056319,
                            "dataset": None,
                        },
                        {
                            "id": "476",
                            "name": "Datafile 476",
                            "path": "/now/lose/long.gif",
                            "size": 163877950,
                            "dataset": None,
                        },
                        {
                            "id": "595",
                            "name": "Datafile 595",
                            "path": "/with/through/maintain.jpeg",
                            "size": 95042354,
                            "dataset": None,
                        },
                        {
                            "id": "714",
                            "name": "Datafile 714",
                            "path": "/effort/ten/yeah.png",
                            "size": 80001674,
                            "dataset": None,
                        },
                        {
                            "id": "833",
                            "name": "Datafile 833",
                            "path": "/movie/west/agent.gif",
                            "size": 168730831,
                            "dataset": None,
                        },
                        {
                            "id": "952",
                            "name": "Datafile 952",
                            "path": "/green/building/cost.tiff",
                            "size": 62543055,
                            "dataset": None,
                        },
                    ],
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
                    "samples": [
                        {
                            "name": "SAMPLE 1",
                            "pid": "pid:1",
                            "description": "Tv shake population. City she "
                            "third find realize support.\nRed say organization"
                            " task. Whether number computer economy design now "
                            "serious appear. Response girl middle "
                            "close role American.",
                            "datasets": [],
                        },
                    ],
                },
                id="Get dataset by pid including all ICAT 4 related entities",
            ),
            pytest.param(
                "Datasets",
                "0-8401-1070-7",
                '{"include": [{"relation": "documents"}, {"relation": "techniques"},'
                ' {"relation": "instrument"}, {"relation": "files"},'
                ' {"relation": "parameters"}, {"relation": "samples"}]}',
                {},
                id="Get dataset by pid including all possible related entities",
                # Skipped ICAT 5 mapping on techniques and instrument
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "Documents",
                "0-417-77631-4",
                '{"include": [{"relation": "datasets"}, {"relation": "members"},'
                ' {"relation": "parameters"}]}',
                {
                    "pid": "0-417-77631-4",
                    "isPublic": True,
                    "type": "INVESTIGATIONTYPE 3",
                    "title": "INVESTIGATION 1",
                    "summary": "Throw hope parent. Receive entire soon. "
                    "War top air agent must voice high describe.\nMonth "
                    "shake voice. Do discuss despite least face again study."
                    " Two beyond picture rich fast sea time.",
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
                id="Get document by pid including all possible related entities",
            ),
        ],
    )
    def test_valid_get_by_pid_endpoint(
        self,
        flask_test_app_search_api,
        endpoint_name,
        pid,
        request_filter,
        expected_json,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/{endpoint_name}/{pid}?filter="
            f"{request_filter}",
        )

        response_data = prepare_data_for_assertion(test_response.json)

        assert test_response.status_code == 200
        assert response_data == expected_json

    @pytest.mark.parametrize(
        "pid, request_filter, expected_status_code",
        [
            pytest.param("0-8401-1070-7", '{"where": []}', 400, id="Bad where filter"),
            pytest.param("0-8401-1070-7", '{"limit": -1}', 400, id="Bad limit filter"),
            pytest.param("0-8401-1070-7", '{"skip": -100}', 400, id="Bad skip filter"),
            pytest.param(
                "0-8401-1070-7", '{"include": ""}', 400, id="Bad include filter",
            ),
            pytest.param("my 404 test pid", "{}", 404, id="Non-existent dataset pid"),
        ],
    )
    def test_invalid_get_by_pid_endpoint(
        self, flask_test_app_search_api, pid, request_filter, expected_status_code,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/Datasets/{pid}"
            f"?filter={request_filter}",
        )

        assert test_response.status_code == expected_status_code
