import logging
from typing import Annotated, List

from fastapi import APIRouter, Path, Query, Request
from pydantic import BaseModel, Json

from datagateway_api.src.common.helpers import get_filters_from_query_string
from datagateway_api.src.search_api import models as search_api_models
from datagateway_api.src.search_api.filters import SearchAPIScoringFilter
from datagateway_api.src.search_api.helpers import (
    get_count,
    get_files,
    get_files_count,
    get_search,
    get_with_pid,
    search_api_error_handling,
)
from datagateway_api.src.search_api.search_scoring import SearchScoring

log = logging.getLogger()


def get_model_for_entity(entity_name: str) -> BaseModel:
    """
    Dynamically get the Pydantic model for the given entity name.

    :param entity_name: The name of the entity (string)
    :return: Pydantic BaseModel class
    :raises AttributeError: If model does not exist
    """
    try:
        return getattr(search_api_models, entity_name)
    except AttributeError as exc:
        raise ValueError(f"No model found for entity {entity_name!r}") from exc


FilterQuery = Query(
    default=None,
    alias="filter",
    title="FILTER",
    description=(
        "Apply filters to the query. The possible filters are:"
        " where, include, limit and skip. Please modify the examples before"
        " executing a request if you are having issues with the example values."
        ' must be a JSON-encoded string (`{"where":{"something":"value"}}`).'
        " See more details"
        ' <a href="https://loopback.io/doc/en/lb3/Querying-data.html#using'
        '-stringified-json-in-rest-queries">here</a>.'
    ),
    json_schema_extra={"type": "string", "default": ""},
    openapi_examples={
        "where filter": {"value": {"where": {"title": {"eq": "dog"}}}},
        "where filter with text operator": {
            "value": {"where": {"text": "dog"}},
        },
        "where filter with AND": {
            "value": {"where": {"and": [{"title": "dog"}, {"size": 10000}]}},
        },
        "where filter with OR": {
            "value": {"where": {"or": [{"title": "dog"}, {"size": 10000}]}},
        },
        "limit filter": {"value": {"limit": 10}},
        "skip filter": {"value": {"skip": 5}},
        "include filter": {"value": {"include": [{"relation": "datasets"}]}},
        "include filter with scope": {
            "value": {
                "include": [
                    {
                        "relation": "datasets",
                        "scope": {"where": {"title": "dog"}},
                    },
                ],
            },
        },
        "all possible filters": {
            "value": {
                "where": {"title": {"neq": "dog"}},
                "include": [
                    {
                        "relation": "datasets",
                        "scope": {"where": {"title": "dog"}},
                    },
                ],
                "limit": 10,
                "skip": 5,
            },
        },
    },
)
WhereQuery = Query(
    default=None,
    name="WHERE_FILTER",
    description=(
        "Apply where filter to the query. The possible operators"
        " are: eq, neq, and, or, gt, gte, lt, lte, between, inq, nin, like, nlike,"
        " ilike, nilike and regexp. Please modify the examples before executing a "
        "request if you are having issues with the example values. See more details"
        ' <a href="https://loopback.io/doc/en/lb3/Where-filter.html">here</a>.'
    ),
    json_schema_extra={"type": "string", "default": ""},
    openapi_examples={
        "eq": {"value": {"title": {"eq": "dog"}}},
        "ne": {"value": {"title": {"neq": "dog"}}},
        "and": {"value": [{"title": "dog"}, {"size": 10000}]},
        "or": {"value": [{"title": "dog"}, {"size": 10000}]},
        "gt": {"value": {"size": {"gt": 10000}}},
        "gte": {"value": {"size": {"gte": 10000}}},
        "lt": {"value": {"size": {"lt": 10000}}},
        "lte": {"value": {"size": {"lte": 10000}}},
        "between": {"value": {"size": {"between": [5000, 10000]}}},
        "inq": {"value": {"size": {"inq": [5000, 10000, 15000]}}},
        "nin": {"value": {"size": {"inq": [5000, 10000, 15000]}}},
        "like": {"value": {"title": {"like": "dog"}}},
        "nlike": {"value": {"title": {"nlike": "dog"}}},
        "ilike": {"value": {"title": {"ilike": "Dog"}}},
        "nilike": {"value": {"title": {"nilike": "Dog"}}},
    },
)


def get_search_endpoint(
    router: APIRouter,
    entity_name: str,
    model: BaseModel,
) -> None:
    """
    Register a search endpoint for the given entity.
    """

    @router.get(
        "",
        summary=f"Get {entity_name}s",
        description=f"Retrieves a list of {entity_name} objects",
        response_model=List[model],
        responses={
            200: {"description": (f"Success - returns {entity_name}s that satisfy the filter")},
            400: {"description": "Bad request - Something was wrong with the request"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    @search_api_error_handling
    def get(
        request: Request,
        filter_: str = FilterQuery,
    ):
        filters = get_filters_from_query_string(
            request,
            "search_api",
            entity_name,
        )

        results = get_search(entity_name, filters)

        scoring_filter = next(
            (f for f in filters if isinstance(f, SearchAPIScoringFilter)),
            None,
        )

        if scoring_filter:
            scores = SearchScoring.get_score(scoring_filter.value)
            results = SearchScoring.add_scores_to_results(results, scores)

        return results


def get_single_endpoint(
    router: APIRouter,
    entity_name: str,
    model: BaseModel,
) -> None:
    """
    Register a single-entity (PID) search endpoint.
    """

    @router.get(
        "/{pid}",
        summary=f"Find the {entity_name} matching the given pid",
        description=f"Retrieves a {entity_name} object with the matching pid",
        response_model=model,
        responses={
            200: {"description": f"Success - the matching {entity_name}"},
            400: {"description": "Bad request - Something was wrong with the request"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    @search_api_error_handling
    def get(
        request: Request,
        pid: Annotated[str, Path(description="The pid of the entity to retrieve")],
        filter_: str = FilterQuery,
    ):
        filters = get_filters_from_query_string(
            request,
            "search_api",
            entity_name,
        )
        log.debug("Filters: %s", filters)

        return get_with_pid(entity_name, pid, filters)


def get_number_count_endpoint(
    router: APIRouter,
    entity_name: str,
) -> None:
    """
    Register a count endpoint for search entities.
    """

    @router.get(
        "/count",
        summary=f"Count {entity_name}s",
        description=(
            f"Return the count of the {entity_name} objects that would be " "retrieved given the filters provided"
        ),
        response_model=int,
        responses={
            200: {"description": f"The count of the {entity_name} objects"},
            400: {"description": "Bad request - Something was wrong with the request"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    @search_api_error_handling
    def get(
        request: Request,
        where: List[Json] = WhereQuery,
    ):
        filters = get_filters_from_query_string(
            request,
            "search_api",
            entity_name,
        )
        log.debug("Filters: %s", filters)

        return get_count(entity_name, filters)


def get_files_endpoint(
    router: APIRouter,
    entity_name: str,
    model: BaseModel,
) -> None:
    """
    Register a files endpoint for a Dataset PID.
    """

    @router.get(
        "/{pid}/files",
        summary=f"Get {entity_name}s for the given Dataset",
        description=(f"Retrieves a list of {entity_name} objects for a given Dataset object"),
        response_model=List[model],
        responses={
            200: {"description": (f"Success - returns {entity_name}s for the given Dataset")},
            400: {"description": "Bad request - Something was wrong with the request"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    @search_api_error_handling
    def get(
        request: Request,
        pid: Annotated[str, Path(description="The pid of the entity to retrieve")],
        filter_: str = FilterQuery,
    ):
        filters = get_filters_from_query_string(
            request,
            "search_api",
            entity_name,
        )
        log.debug("Filters: %s", filters)

        return get_files(entity_name, pid, filters)


def get_number_count_files_endpoint(
    router: APIRouter,
    entity_name: str,
) -> None:
    """
    Register a count-files endpoint for a Dataset PID.
    """

    @router.get(
        "/{pid}/files/count",
        summary=f"Count {entity_name}s for the given Dataset",
        description=(
            f"Return the count of {entity_name} objects for the given Dataset "
            "object that would be retrieved given the filters provided"
        ),
        response_model=int,
        responses={
            200: {"description": (f"The count of {entity_name} objects for the given Dataset")},
            400: {"description": "Bad request - Something was wrong with the request"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    @search_api_error_handling
    def get(
        request: Request,
        pid: Annotated[str, Path(description="The pid of the entity to retrieve")],
        where: List[Json] = WhereQuery,
    ):
        filters = get_filters_from_query_string(
            request,
            "search_api",
            entity_name,
        )
        log.debug("Filters: %s", filters)

        return get_files_count(entity_name, filters, pid)


def create_search_collection_router(
    entity_name: str,
    endpoint_name: str,
    add_file_endpoints: bool = False,
) -> APIRouter:
    """
    Factory function that creates and configures a FastAPI APIRouter
    for a collection-style search api ICAT entity.

    This function is responsible for:
        - Creating the router with the correct prefix and tags
        - Registering collection-level endpoints (GET etc)
        via helper functions
        - Returning the fully configured router to be included in the app

    The endpoint implementations themselves are defined in separate
    helper functions.
    """
    router = APIRouter(prefix=f"/{endpoint_name}", tags=[entity_name])
    model = get_model_for_entity(entity_name)

    get_search_endpoint(router, entity_name, model)
    get_single_endpoint(router, entity_name, model)
    get_number_count_endpoint(router, entity_name)
    if add_file_endpoints:
        get_files_endpoint(router, "File", model)
        get_number_count_files_endpoint(router, "File")

    return router
