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

    def test_invalid_get_by_pid_endpoint(self):
        # TODO - test for bad filter and bad/unknown PID
        pass
