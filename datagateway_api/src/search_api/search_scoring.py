import requests
from requests import RequestException

from datagateway_api.src.common.config import Config
from datagateway_api.src.common.exceptions import ScoringAPIError


class SearchScoring:
    @staticmethod
    def get_score(query):
        """
        Gets the score for all the items in the scoring API according to the query
        value provided.
        :param query: The term to use in the relevancy scoring
        :type query: :class:`str`
        :return: Returns the scores
        :raises ScoringAPIError: If an error occurs while interacting with the Search
            Scoring API
        """
        try:
            data = {
                "query": query,
                "group": Config.config.search_api.search_scoring.group,
                "limit": Config.config.search_api.search_scoring.limit,
                # With itemIds, scoring server returns a 400 error. No idea why.
                # "itemIds": list(map(lambda entity: (entity["pid"]), entities)),  #
            }
            response = requests.post(
                Config.config.search_api.search_scoring.api_url,
                json=data,
                timeout=Config.config.search_api.search_scoring.api_request_timeout,
            )
            response.raise_for_status()
            return response.json()["scores"]
        except RequestException:
            raise ScoringAPIError("An error occurred while trying to score the results")

    @staticmethod
    def add_scores_to_results(results, scores):
        """
        Add the scores to all the results returned from the metadata catalogue. It only
        adds the score if it finds a match, otherwise the score is set to -1
        (arbitrarily chosen).
        :param results: List of results that have been retrieved from the metadata
            catalogue
        :type results: :class:`list`
        :param scores: List of items retrieved from the scoring application
        :type scores: :class:`list`
        :return: Returns the results with scores
        """
        for result in results:
            result["score"] = next(
                (
                    score["score"]
                    for score in scores
                    if score["itemId"] == result["pid"]
                ),
                -1,
            )

        return results
