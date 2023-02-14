from unittest.mock import patch

import pytest
from requests import RequestException

from datagateway_api.src.common.config import Config
from datagateway_api.src.common.exceptions import ScoringAPIError
from datagateway_api.src.search_api.search_scoring import SearchScoring

SEARCH_SCORING_API_SCORES_DATA = {
    "request": {
        "query": "My test query",
        "itemIds": [],
        "group": "Documents",
        "limit": 1000,
    },
    "query": {"query": "My test query", "terms": ["test", "queri"]},
    "scores": [
        {"itemId": "Test doi", "score": 0.7071067811865475, "group": ""},
        {"itemId": "pid:987654321", "score": 0.53843041, "group": ""},
    ],
    "dimension": 3,
    "computeInProgress": False,
    "started": "2023-02-13T12:23:56.280659",
    "ended": "2023-02-13T12:23:56.784180",
}

SEARCH_API_DOCUMENT_RESULTS = [
    {
        "pid": "Test doi",
        "isPublic": True,
        "type": "Test name",
        "title": "Test name",
        "summary": "Test",
        "doi": "Test doi",
        "startDate": "2000-12-31T00:00:00.000Z",
        "endDate": "2000-12-31T00:00:00.000Z",
        "releaseDate": "2000-12-31T00:00:00.000Z",
        "license": None,
        "keywords": ["Test name"],
        "datasets": [],
        "members": [],
        "parameters": [],
    },
    {
        "pid": "pid:12345",
        "isPublic": True,
        "type": "Test name",
        "title": "Test name",
        "summary": "Test",
        "doi": "Test doi",
        "startDate": "2000-12-31T00:00:00.000Z",
        "endDate": "2000-12-31T00:00:00.000Z",
        "releaseDate": "2000-12-31T00:00:00.000Z",
        "license": None,
        "keywords": ["Test name"],
        "datasets": [],
        "members": [],
        "parameters": [],
    },
    {
        "pid": "pid:987654321",
        "isPublic": True,
        "type": "Test name",
        "title": "Test name",
        "summary": "Test summary",
        "doi": "Test doi",
        "startDate": "2000-12-31T00:00:00.000Z",
        "endDate": "2000-12-31T00:00:00.000Z",
        "releaseDate": "2000-12-31T00:00:00.000Z",
        "license": None,
        "keywords": ["Test name"],
        "datasets": [],
        "members": [],
        "parameters": [],
    },
]


class TestHelpers:
    @patch("requests.post")
    def test_get_score(self, post_mock):
        scoring_query_filter_value = "My test query"
        post_request_data = {
            "query": scoring_query_filter_value,
            "group": Config.config.search_api.search_scoring.group,
            "limit": Config.config.search_api.search_scoring.limit,
        }
        post_mock.return_value.status_code = 200
        post_mock.return_value.json.return_value = SEARCH_SCORING_API_SCORES_DATA

        scores = SearchScoring.get_score(scoring_query_filter_value)

        post_mock.assert_called_once_with(
            Config.config.search_api.search_scoring.api_url,
            json=post_request_data,
            timeout=Config.config.search_api.search_scoring.api_request_timeout,
        )
        assert scores == SEARCH_SCORING_API_SCORES_DATA["scores"]

    @patch("requests.post")
    def test_get_score_raises_scoring_api_error(self, post_mock):
        post_mock.side_effect = RequestException
        with pytest.raises(ScoringAPIError):
            SearchScoring.get_score("My test query")

    def test_add_score_to_results(self):
        expected_results_with_scores = []
        # Add scores to document results
        scores = [0.7071067811865475, -1, 0.53843041]
        for i, result in enumerate(SEARCH_API_DOCUMENT_RESULTS):
            expected_results_with_scores.append(result.copy())
            expected_results_with_scores[i]["score"] = scores[i]

        actual_results_with_scores = SearchScoring.add_scores_to_results(
            SEARCH_API_DOCUMENT_RESULTS, SEARCH_SCORING_API_SCORES_DATA["scores"],
        )

        assert actual_results_with_scores == expected_results_with_scores
