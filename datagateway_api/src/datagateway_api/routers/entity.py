from typing import Annotated, Any, List

from fastapi import APIRouter, Path, Query, Request
from pydantic import BaseModel, Json

from datagateway_api.src.common.helpers import get_filters_from_query_string, get_session_id_from_auth_header
from datagateway_api.src.datagateway_api.icat import models as datagateway_models

WhereQuery = Query(
    default=None,
    title="WHERE_FILTER",
    description=(
        "Apply where filters to the query. The possible operators"
        " are: ne, like, lt, lte, gt, gte, in and eq. Please modify the examples"
        " before executing a request if you are having issues with the example"
        " values."
    ),
    json_schema_extra={
        "type": "array",
        "items": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "minProperties": 1,
                "maxProperties": 1,
                "title": "Column",
                "description": "Name of the column to apply the filter on",
                "oneOf": [
                    {
                        "title": "Equality",
                        "properties": {
                            "eq": {
                                "oneOf": [
                                    {"type": "string"},
                                    {"type": "number"},
                                    {"type": "integer"},
                                    {"type": "boolean"},
                                ],
                            },
                        },
                    },
                    {
                        "title": "Inequality",
                        "properties": {
                            "ne": {
                                "oneOf": [
                                    {"type": "string"},
                                    {"type": "number"},
                                    {"type": "integer"},
                                    {"type": "boolean"},
                                ],
                            },
                        },
                    },
                    {
                        "title": "Substring equality",
                        "properties": {"like": {"type": "string"}},
                    },
                    {
                        "title": "Less than",
                        "properties": {"lt": {"oneOf": [{"type": "number"}, {"type": "integer"}]}},
                    },
                    {
                        "title": "Less than or equal",
                        "properties": {"lte": {"oneOf": [{"type": "number"}, {"type": "integer"}]}},
                    },
                    {
                        "title": "Greater than",
                        "properties": {"gt": {"oneOf": [{"type": "number"}, {"type": "integer"}]}},
                    },
                    {
                        "title": "Greater than or equal",
                        "properties": {"gte": {"oneOf": [{"type": "number"}, {"type": "integer"}]}},
                    },
                    {
                        "title": "Equality from a list of values",
                        "properties": {
                            "in": {
                                "type": "array",
                                "items": {
                                    "oneOf": [
                                        {"type": "string"},
                                        {"type": "number"},
                                        {"type": "integer"},
                                    ],
                                },
                            },
                        },
                    },
                ],
            },
            "default": "",
        },
    },
    openapi_examples={
        "eq": {"value": [{"id": {"eq": 1}}]},
        "ne": {"value": [{"id": {"ne": 1}}]},
        "like": {"value": [{"name": {"like": "dog"}}]},
        "lt": {"value": [{"id": {"lt": 10}}]},
        "lte": {"value": [{"id": {"lte": 50}}]},
        "gt": {"value": [{"id": {"gt": 10}}]},
        "gte": {"value": [{"id": {"gte": 50}}]},
        "in": {"value": [{"id": {"in": [1, 2, 3]}}]},
    },
)
OrderQuery = Query(
    default=None,
    title="ORDER_FILTER",
    description=("Apply order filters to the query. Given a field and direction, order the returned entities."),
    json_schema_extra={"type": "array", "items": {"type": "string", "default": ""}},
    openapi_examples={"asc": {"value": ["id asc"]}, "desc": {"value": ["id desc"]}},
)
LimitQuery = Query(
    default=None,
    title="LIMIT_FILTER",
    description="Apply limit filter to the query. Limit the number of" " entities returned.",
    json_schema_extra={"type": "integer", "default": ""},
)
SkipQuery = Query(
    default=None,
    title="SKIP_FILTER",
    description="Apply skip filter to the query. Offset the returned" " entities by a given number.",
    json_schema_extra={"type": "integer", "default": ""},
)
DistinctQuery = Query(
    default=None,
    title="DISTINCT_FILTER",
    description="Apply distinct filter to the query. Return unique values" " for the fields requested.",
    json_schema_extra={"type": "array", "items": {"type": "string", "default": ""}},
)
IncludeQuery = Query(
    default=None,
    title="INCLUDE_FILTER",
    description="Apply include filter to the query. Given the names of"
    " related entities, include them in the results. Only one include parameter"
    " is allowed.",
    json_schema_extra={
        "oneOf": [
            {"type": "string"},
            {
                "type": "array",
                "items": {
                    "oneOf": [
                        {"type": "string"},
                        {
                            "type": "object",
                            "additionalProperties": {
                                "oneOf": [
                                    {"type": "string"},
                                    {
                                        "type": "array",
                                        "items": [{"type": "string"}],
                                    },
                                ],
                            },
                        },
                    ],
                },
            },
            {
                "type": "object",
                "additionalProperties": {
                    "oneOf": [
                        {"type": "string"},
                        {"type": "array", "items": [{"type": "string"}]},
                    ],
                },
            },
        ],
    },
    openapi_examples={
        "single": {"value": "RELATED_COLUMN"},
        "array": {"value": ["RELATED_COLUMN_1", "RELATED_COLUMN_2"]},
        "multi-level": {
            "value": {"RELATED_COLUMN": "RELATED_COLUMN_RELATED_COLUMN"},
        },
        "multi-level array": {
            "value": {
                "RELATED_COLUMN": [
                    "RELATED_COLUMN_RELATED_COLUMN_1",
                    "RELATED_COLUMN_RELATED_COLUMN_2",
                ],
            },
        },
        "array of multi-level": {
            "value": [
                "RELATED_COLUMN_1",
                {"RELATED_COLUMN_2": "RELATED_COLUMN_2_RELATED_COLUMN_1"},
                {
                    "RELATED_COLUMN_3": [
                        "RELATED_COLUMN_3_RELATED_COLUMN_1",
                        "RELATED_COLUMN_3_RELATED_COLUMN_2",
                    ],
                },
            ],
        },
    },
)


def get_model_for_entity(entity_name: str) -> BaseModel:
    """
    Dynamically get the Pydantic model for the given entity name.

    :param entity_name: The name of the entity (string)
    :return: Pydantic BaseModel class
    :raises AttributeError: If model does not exist
    """
    try:
        return getattr(datagateway_models, entity_name)
    except AttributeError as exc:
        raise ValueError(f"No model found for entity {entity_name!r}") from exc


def get_endpoint(
    router: APIRouter,
    name: str,
    entity_type: str,
    model: BaseModel,
    python_icat,
    **kwargs,
) -> None:
    """
    Given an entity name, register collection-level FastAPI endpoints on the
    provided APIRouter.

    It registers GET, POST, and PATCH handlers for collection
    access.

    :param router: FastAPI APIRouter to register endpoints on
    :param name: The name of the entity
    :param entity_type: The entity the endpoint will use in queries
    :param model: Pydantic model representing the entity
    :param python_icat: The python ICAT instance used for processing requests
    """

    @router.get(
        "",
        summary=f"Get {name}",
        description=f"Retrieves a list of {entity_type} objects",
        response_model=List[model],
        responses={
            200: {"description": f"Success - returns {entity_type} that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get(
        request: Request,
        where: List[Json] = WhereQuery,
        order: List[str] = OrderQuery,
        limit: int = LimitQuery,
        skip: int = SkipQuery,
        distinct: int = DistinctQuery,
        include: Any = IncludeQuery,
    ):
        return python_icat.get_with_filters(
            get_session_id_from_auth_header(request),
            entity_type,
            get_filters_from_query_string(request, "datagateway_api"),
            **kwargs,
        )

    @router.post(
        "",
        summary=f"Create new {name}",
        description=(f"Creates new {entity_type} object(s) with details provided " "in the request body"),
        response_model=List[model],
        responses={
            200: {"description": "Success - returns the created object"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def post(body: model, request: Request):
        return python_icat.create(
            get_session_id_from_auth_header(request),
            entity_type,
            body.model_dump_json(),
            **kwargs,
        )

    @router.patch(
        "",
        summary=f"Update {name}",
        description=(f"Updates {entity_type} object(s) with details provided " "in the request body"),
        response_model=List[model],
        responses={
            200: {"description": "Success - returns the updated object(s)"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def patch(body: model, request: Request):
        return python_icat.update(
            get_session_id_from_auth_header(request),
            entity_type,
            body.model_dump_json(),
            **kwargs,
        )


def get_id_endpoint(
    router: APIRouter,
    name: str,
    entity_type: str,
    model: BaseModel,
    python_icat,
    **kwargs,
) -> None:
    """
    Given an entity name, register ID-level FastAPI endpoints on the
    provided APIRouter.

    It registers GET, DELETE, and PATCH handlers for single-entity access.

    :param router: FastAPI APIRouter to register endpoints on
    :param name: The name of the entity
    :param entity_type: The entity the endpoint will use in queries
    :param model: Pydantic model representing the entity
    :param python_icat: The python ICAT instance used for processing requests
    """

    @router.get(
        "/{id_}",
        summary=f"Find the {entity_type} matching the given ID",
        description=f"Retrieves a single {entity_type} object",
        response_model=model,
        responses={
            200: {"description": f"Success - the matching {entity_type}"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get(
        request: Request,
        id_: Annotated[int, Path(description="The id of the entity to retrieve")],
    ):
        return python_icat.get_with_id(
            get_session_id_from_auth_header(request),
            entity_type,
            id_,
            **kwargs,
        )

    @router.delete(
        "/{id_}",
        summary=f"Delete {name} by id",
        description=f"Deletes the {entity_type} with the specified ID",
        status_code=204,
        responses={
            204: {"description": "No Content - Object was successfully deleted"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def delete(
        request: Request,
        id_: Annotated[int, Path(description="The id of the entity to delete")],
    ):
        python_icat.delete_with_id(
            get_session_id_from_auth_header(request),
            entity_type,
            id_,
            **kwargs,
        )

    @router.patch(
        "/{id_}",
        summary=f"Update {name} by id",
        description=f"Updates the {entity_type} with the specified ID",
        response_model=model,
        responses={
            200: {"description": "Success - returns the updated object"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def patch(
        body: model,
        request: Request,
        id_: Annotated[int, Path(description="The id of the entity to update")],
    ):
        session_id = get_session_id_from_auth_header(request)

        python_icat.update_with_id(
            session_id,
            entity_type,
            id_,
            body.model_dump_json(),
            **kwargs,
        )

        return python_icat.get_with_id(
            session_id,
            entity_type,
            id_,
            **kwargs,
        )


def get_count_endpoint(
    router: APIRouter,
    name: str,
    entity_type: str,
    python_icat,
    **kwargs,
) -> None:
    """
    Given an entity name, register a count-level FastAPI endpoint on the
    provided APIRouter.

    It registers a GET handler that returns the count of entities matching
    the provided filters.

    :param router: FastAPI APIRouter to register endpoints on
    :param name: The name of the entity
    :param entity_type: The entity the endpoint will use in queries
    :param python_icat: The python ICAT instance used for processing requests
    """

    @router.get(
        "/count",
        summary=f"Count {name}",
        description=(
            f"Return the count of the {entity_type} objects that would be " "retrieved given the filters provided"
        ),
        response_model=int,
        responses={
            200: {"description": f"Success - The count of the {entity_type} objects"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get(
        request: Request,
        where: List[Json] = WhereQuery,
        distinct: int = DistinctQuery,
        include: Any = IncludeQuery,
    ):
        filters = get_filters_from_query_string(request, "datagateway_api")

        return python_icat.count_with_filters(
            get_session_id_from_auth_header(request),
            entity_type,
            filters,
            **kwargs,
        )


def get_find_one_endpoint(
    router: APIRouter,
    entity_type: str,
    model: BaseModel,
    python_icat,
    **kwargs,
) -> None:
    """
    Given an entity name, register a find-one FastAPI endpoint on the
    provided APIRouter.

    It registers a GET handler that returns the first entity matching
    the provided filters.
    """

    @router.get(
        "/findone",
        summary=f"Get single {entity_type}",
        description=(f"Retrieves the first {entity_type} object that satisfies the filters."),
        response_model=model,
        responses={
            200: {"description": (f"Success - a {entity_type} object that satisfies the filters")},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get(
        request: Request,
        where: List[Json] = WhereQuery,
        order: List[str] = OrderQuery,
        limit: int = LimitQuery,
        skip: int = SkipQuery,
        distinct: int = DistinctQuery,
        include: Any = IncludeQuery,
    ):
        filters = get_filters_from_query_string(request, "datagateway_api")

        return python_icat.get_one_with_filters(
            get_session_id_from_auth_header(request),
            entity_type,
            filters,
            **kwargs,
        )


def create_collection_router(
    name: str,
    entity_type: str,
    python_icat,
    **kwargs,
) -> APIRouter:
    """
    Factory function that creates and configures a FastAPI APIRouter
    for a collection-style ICAT entity.

    This function is responsible for:
      - Creating the router with the correct prefix and tags
      - Registering collection-level endpoints (GET, POST, PATCH, etc.)
        via helper functions
      - Returning the fully configured router to be included in the app

    The endpoint implementations themselves are defined in separate
    helper functions.
    """
    router = APIRouter(prefix=f"/{name.lower()}", tags=[name])
    model = get_model_for_entity(entity_type)

    get_endpoint(router, name, entity_type, model, python_icat, **kwargs)
    get_id_endpoint(router, name, entity_type, model, python_icat, **kwargs)
    get_count_endpoint(router, name, entity_type, python_icat, **kwargs)
    get_find_one_endpoint(router, entity_type, model, python_icat, **kwargs)

    return router
