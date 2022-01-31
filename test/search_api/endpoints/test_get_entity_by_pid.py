import pytest

from datagateway_api.src.common.config import Config


class TestSearchAPIGetByPIDEndpoint:
    @pytest.mark.parametrize(
        "endpoint_name, pid, request_filter, expected_json",
        [
            pytest.param(
                "datasets",
                "0-8401-1070-7",
                "{}",
                {
                    "description": "Beat professional blue clear style have. Light"
                    " final summer. Or hour color maybe word side much team.\nMessage"
                    " weight official learn especially nature. Himself tax west.",
                    "modTime": "2006-08-24 01:28:06+00:00",
                    "modId": "user",
                    "startDate": "2000-10-13 00:00:00+00:00",
                    "endDate": "2000-02-10 00:00:00+00:00",
                    "createId": "user",
                    "complete": True,
                    "id": 2,
                    "name": "DATASET 2",
                    "doi": "0-8401-1070-7",
                    "createTime": "2013-04-01 10:56:52+00:00",
                    "location": "/subject/break.jpeg",
                },
                id="Basic /datasets/{pid} request",
            ),
            pytest.param(
                "documents",
                "0-449-78690-0",
                "{}",
                {
                    "visitId": "42",
                    "modId": "user",
                    "name": "INVESTIGATION 1",
                    "createId": "user",
                    "createTime": "2002-11-27 06:20:36+00:00",
                    "doi": "0-449-78690-0",
                    "id": 1,
                    "summary": "Season identify professor happen third. Beat"
                    " professional blue clear style have. Light final summer.",
                    "endDate": "2000-07-09 00:00:00+00:00",
                    "modTime": "2005-04-30 19:41:49+00:00",
                    "releaseDate": "2000-07-05 00:00:00+00:00",
                    "startDate": "2000-04-03 00:00:00+00:00",
                    "title": "Including spend increase ability music skill former."
                    " Agreement director concern once technology sometimes someone"
                    " staff.\nSuccess pull bar. Laugh senior example.",
                },
                id="Basic /documents/{pid} request",
            ),
            pytest.param(
                "instruments",
                "2",
                "{}",
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
                    " International scene call deep answer audience baby true.\n"
                    "Indicate education across these. Opportunity design too.",
                    "url": "https://moore.org/",
                },
                id="Basic /instruments/{pid} request",
            ),
            pytest.param(
                "datasets",
                "0-8401-1070-7",
                '{"include": [{"relation": "documents"}]}',
                {
                    "createId": "user",
                    "startDate": "2000-10-13 00:00:00+00:00",
                    "doi": "0-8401-1070-7",
                    "modTime": "2006-08-24 01:28:06+00:00",
                    "createTime": "2013-04-01 10:56:52+00:00",
                    "location": "/subject/break.jpeg",
                    "endDate": "2000-02-10 00:00:00+00:00",
                    "complete": True,
                    "modId": "user",
                    "documents": [
                        {
                            "createId": "user",
                            "doi": "0-9729806-3-6",
                            "startDate": "2000-06-04 00:00:00+00:00",
                            "modTime": "2016-11-16 19:42:34+00:00",
                            "createTime": "2004-08-23 02:41:19+00:00",
                            "endDate": "2000-09-14 00:00:00+00:00",
                            "modId": "user",
                            "title": "Show fly image herself yard challenge by. Past"
                            " site her number. Not weight half far move. Leader"
                            " everyone skin still.\nProve begin boy those always"
                            " dream write inside.",
                            "summary": "Day purpose item create. Visit hope mean admit."
                            " The tonight adult cut foreign would situation fund.\n"
                            "Purpose study usually gas think. Machine world doctor"
                            " rise be college treat.",
                            "visitId": "4",
                            "name": "INVESTIGATION 2",
                            "releaseDate": "2000-02-10 00:00:00+00:00",
                            "id": 2,
                        },
                    ],
                    "description": "Beat professional blue clear style have. Light"
                    " final summer. Or hour color maybe word side much team."
                    "\nMessage weight official learn especially nature. Himself"
                    " tax west.",
                    "name": "DATASET 2",
                    "id": 2,
                },
                id="Get dataset by pid with include filter",
                # Skipped because of incorrect document JSON format
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "documents",
                "0-449-78690-0",
                '{"include": [{"relation": "datasets"}]}',
                {
                    "datasets": [
                        {
                            "createId": "user",
                            "startDate": "2000-05-07 00:00:00+00:00",
                            "doi": "0-449-78690-0",
                            "modTime": "2005-04-30 19:41:49+00:00",
                            "createTime": "2002-11-27 06:20:36+00:00",
                            "location": "/international/subject.tiff",
                            "endDate": "2000-07-05 00:00:00+00:00",
                            "complete": True,
                            "modId": "user",
                            "description": "Many last prepare small. Maintain throw"
                            " hope parent.\nEntire soon option bill fish against power."
                            "\nRather why rise month shake voice.",
                            "name": "DATASET 1",
                            "id": 1,
                        },
                        {
                            "createId": "user",
                            "startDate": "2060-01-07 00:00:00+00:00",
                            "doi": "0-353-84629-5",
                            "modTime": "2002-09-30 13:03:32+00:00",
                            "createTime": "2006-11-21 17:10:42+00:00",
                            "location": "/gun/special.jpeg",
                            "endDate": "2060-01-17 00:00:00+00:00",
                            "complete": True,
                            "modId": "user",
                            "description": "Single many hope organization reach process"
                            " I. Health hit total federal describe. Bill firm rate"
                            " democratic outside.\nLate while our either worry.",
                            "name": "DATASET 241",
                            "id": 241,
                        },
                    ],
                    "visitId": "42",
                    "modId": "user",
                    "name": "INVESTIGATION 1",
                    "createId": "user",
                    "createTime": "2002-11-27 06:20:36+00:00",
                    "doi": "0-449-78690-0",
                    "id": 1,
                    "summary": "Season identify professor happen third. Beat"
                    " professional blue clear style have. Light final summer.",
                    "endDate": "2000-07-09 00:00:00+00:00",
                    "modTime": "2005-04-30 19:41:49+00:00",
                    "releaseDate": "2000-07-05 00:00:00+00:00",
                    "startDate": "2000-04-03 00:00:00+00:00",
                    "title": "Including spend increase ability music skill former."
                    " Agreement director concern once technology sometimes someone"
                    " staff.\nSuccess pull bar. Laugh senior example.",
                },
                id="Get document by pid with include filter",
            ),
            pytest.param(
                "instruments",
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
                    " International scene call deep answer audience baby true.\n"
                    "Indicate education across these. Opportunity design too.",
                    "url": "https://moore.org/",
                },
                id="Get instrument by pid with include filter",
                # Skipped due to ICAT 5 mapping
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "datasets",
                "0-8401-1070-7",
                '{"include": [{"relation": "documents"}, {"relation": "techniques"},'
                ' {"relation": "instrument"}, {"relation": "files"},'
                ' {"relation": "parameters"}, {"relation": "samples"}]}',
                {
                    "createId": "user",
                    "startDate": "2000-10-13 00:00:00+00:00",
                    "doi": "0-8401-1070-7",
                    "modTime": "2006-08-24 01:28:06+00:00",
                    "createTime": "2013-04-01 10:56:52+00:00",
                    "location": "/subject/break.jpeg",
                    "endDate": "2000-02-10 00:00:00+00:00",
                    "complete": True,
                    "modId": "user",
                    "documents": [
                        {
                            "createId": "user",
                            "doi": "0-9729806-3-6",
                            "startDate": "2000-06-04 00:00:00+00:00",
                            "modTime": "2016-11-16 19:42:34+00:00",
                            "createTime": "2004-08-23 02:41:19+00:00",
                            "endDate": "2000-09-14 00:00:00+00:00",
                            "modId": "user",
                            "title": "Show fly image herself yard challenge by. Past"
                            " site her number. Not weight half far move. Leader"
                            " everyone skin still.\nProve begin boy those always"
                            " dream write inside.",
                            "summary": "Day purpose item create. Visit hope mean admit."
                            " The tonight adult cut foreign would situation fund.\n"
                            "Purpose study usually gas think. Machine world doctor"
                            " rise be college treat.",
                            "visitId": "4",
                            "name": "INVESTIGATION 2",
                            "releaseDate": "2000-02-10 00:00:00+00:00",
                            "id": 2,
                        },
                    ],
                    "description": "Beat professional blue clear style have. Light"
                    " final summer. Or hour color maybe word side much team."
                    "\nMessage weight official learn especially nature. Himself"
                    " tax west.",
                    "name": "DATASET 2",
                    "id": 2,
                },
                id="Get dataset by pid including all possible related entities",
                # Skipped because of incorrect document JSON format and ICAT 5 mapping
                # on techniques and instrument
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "documents",
                "0-449-78690-0",
                '{"include": [{"relation": "datasets"}, {"relation": "members"},'
                ' {"relation": "parameters"}]}',
                {
                    "datasets": [
                        {
                            "createId": "user",
                            "startDate": "2000-05-07 00:00:00+00:00",
                            "doi": "0-449-78690-0",
                            "modTime": "2005-04-30 19:41:49+00:00",
                            "createTime": "2002-11-27 06:20:36+00:00",
                            "location": "/international/subject.tiff",
                            "endDate": "2000-07-05 00:00:00+00:00",
                            "complete": True,
                            "modId": "user",
                            "description": "Many last prepare small. Maintain throw"
                            " hope parent.\nEntire soon option bill fish against power."
                            "\nRather why rise month shake voice.",
                            "parameters": [],
                            "name": "DATASET 1",
                            "id": 1,
                        },
                        {
                            "createId": "user",
                            "startDate": "2060-01-07 00:00:00+00:00",
                            "doi": "0-353-84629-5",
                            "modTime": "2002-09-30 13:03:32+00:00",
                            "createTime": "2006-11-21 17:10:42+00:00",
                            "location": "/gun/special.jpeg",
                            "endDate": "2060-01-17 00:00:00+00:00",
                            "complete": True,
                            "modId": "user",
                            "description": "Single many hope organization reach process"
                            " I. Health hit total federal describe. Bill firm rate"
                            " democratic outside.\nLate while our either worry.",
                            "parameters": [],
                            "name": "DATASET 241",
                            "id": 241,
                        },
                    ],
                    "createId": "user",
                    "doi": "0-449-78690-0",
                    "startDate": "2000-04-03 00:00:00+00:00",
                    "modTime": "2005-04-30 19:41:49+00:00",
                    "createTime": "2002-11-27 06:20:36+00:00",
                    "members": [
                        {
                            "createId": "user",
                            "modId": "user",
                            "modTime": "2005-04-30 19:41:49+00:00",
                            "role": "CI",
                            "createTime": "2002-11-27 06:20:36+00:00",
                            "id": 1,
                        },
                    ],
                    "endDate": "2000-07-09 00:00:00+00:00",
                    "modId": "user",
                    "title": "Including spend increase ability music skill former."
                    " Agreement director concern once technology sometimes someone"
                    " staff.\nSuccess pull bar. Laugh senior example.",
                    "summary": "Season identify professor happen third. Beat"
                    " professional blue clear style have. Light final summer.",
                    "visitId": "42",
                    "parameters": [
                        {
                            "dateTimeValue": "2000-05-07 00:00:00+00:00",
                            "rangeBottom": 48.0,
                            "createId": "user",
                            "numericValue": 127265.0,
                            "modTime": "2005-04-30 19:41:49+00:00",
                            "createTime": "2002-11-27 06:20:36+00:00",
                            "id": 1,
                            "stringValue": "international1",
                            "modId": "user",
                            "rangeTop": 101.0,
                            "error": 31472.0,
                        },
                    ],
                    "name": "INVESTIGATION 1",
                    "releaseDate": "2000-07-05 00:00:00+00:00",
                    "id": 1,
                },
                id="Get document by pid including all possible related entities",
                # Skipped because of incorrect members JSON naming
                # (investigationUsers key used instead). It's in ICAT fields too,
                # not converted into PaNOSC format
                marks=pytest.mark.skip,
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

        assert test_response.status_code == 200
        assert test_response.json == expected_json

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
            f"{Config.config.search_api.extension}/datasets/{pid}"
            f"?filter={request_filter}",
        )

        assert test_response.status_code == expected_status_code
