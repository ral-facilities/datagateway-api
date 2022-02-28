from datagateway_api.src.resources.entities.entity_map import create_entity_models
from datagateway_api.src.search_api.models import (
    Affiliation,
    Dataset,
    Document,
    File,
    Instrument,
    Member,
    Parameter,
    Person,
    Sample,
    Technique,
)


def initialise_datagateway_api_spec(spec):
    """
    Given a apispec spec object, will initialise it with the security scheme, models and
    parameters we use

    :spec: ApiSpec: spec object to initialise
    :return: void
    """

    spec.components.security_scheme(
        "session_id", {"type": "http", "scheme": "bearer", "bearerFormat": "uuid"},
    )

    entity_schemas = create_entity_models()

    for (schema_name, schema) in entity_schemas.items():
        spec.components.schema(schema_name, schema)

    spec.components.parameter(
        "WHERE_FILTER",
        "query",
        {
            "in": "query",
            "name": "where",
            "description": "Apply where filters to the query. The possible operators"
            " are: ne, like, lt, lte, gt, gte, in and eq. Please modify the examples"
            " before executing a request if you are having issues with the example"
            " values.",
            "schema": {
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
                                "type": "object",
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
                                "type": "object",
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
                                "type": "object",
                                "title": "Substring equality",
                                "properties": {"like": {"type": "string"}},
                            },
                            {
                                "type": "object",
                                "title": "Less than",
                                "properties": {
                                    "lt": {
                                        "oneOf": [
                                            {"type": "number"},
                                            {"type": "integer"},
                                        ],
                                    },
                                },
                            },
                            {
                                "type": "object",
                                "title": "Less than or equal",
                                "properties": {
                                    "lte": {
                                        "oneOf": [
                                            {"type": "number"},
                                            {"type": "integer"},
                                        ],
                                    },
                                },
                            },
                            {
                                "type": "object",
                                "title": "Greater than",
                                "properties": {
                                    "gt": {
                                        "oneOf": [
                                            {"type": "number"},
                                            {"type": "integer"},
                                        ],
                                    },
                                },
                            },
                            {
                                "type": "object",
                                "title": "Greater than or equal",
                                "properties": {
                                    "gte": {
                                        "oneOf": [
                                            {"type": "number"},
                                            {"type": "integer"},
                                        ],
                                    },
                                },
                            },
                            {
                                "type": "object",
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
                },
            },
            "examples": {
                "eq": {"value": [{"id": {"eq": 1}}]},
                "ne": {"value": [{"id": {"ne": 1}}]},
                "like": {"value": [{"name": {"like": "dog"}}]},
                "lt": {"value": [{"id": {"lt": 10}}]},
                "lte": {"value": [{"id": {"lte": 50}}]},
                "gt": {"value": [{"id": {"gt": 10}}]},
                "gte": {"value": [{"id": {"gte": 50}}]},
                "in": {"value": [{"id": {"in": [1, 2, 3]}}]},
            },
        },
    )

    spec.components.parameter(
        "ORDER_FILTER",
        "query",
        {
            "in": "query",
            "name": "order",
            "description": "Apply order filters to the query. Given a field and"
            " direction, order the returned entities.",
            "schema": {"type": "array", "items": {"type": "string"}},
            "examples": {"asc": {"value": ["id asc"]}, "desc": {"value": ["id desc"]}},
        },
    )

    spec.components.parameter(
        "LIMIT_FILTER",
        "query",
        {
            "in": "query",
            "name": "limit",
            "description": "Apply limit filter to the query. Limit the number of"
            " entities returned.",
            "schema": {"type": "integer"},
        },
    )

    spec.components.parameter(
        "SKIP_FILTER",
        "query",
        {
            "in": "query",
            "name": "skip",
            "description": "Apply skip filter to the query. Offset the returned"
            " entities by a given number.",
            "schema": {"type": "integer"},
        },
    )
    spec.components.parameter(
        "DISTINCT_FILTER",
        "query",
        {
            "in": "query",
            "name": "distinct",
            "description": "Apply distinct filter to the query. Return unique values"
            " for the fields requested.",
            "schema": {"type": "array", "items": {"type": "string"}},
        },
    )
    spec.components.parameter(
        "INCLUDE_FILTER",
        "query",
        {
            "in": "query",
            "name": "include",
            "description": "Apply include filter to the query. Given the names of"
            " related entities, include them in the results. Only one include parameter"
            " is allowed.",
            "schema": {
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
            "examples": {
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
        },
    )


def initialise_search_api_spec(spec):
    """
    Given a apispec spec object, will initialise it with the models and parameters we
    use

    :spec: ApiSpec: spec object to initialise
    :return: void
    """
    panosc_models = [
        Affiliation,
        Dataset,
        Document,
        File,
        Instrument,
        Member,
        Parameter,
        Person,
        Sample,
        Technique,
    ]
    for panosc_model in panosc_models:
        schema = panosc_model.schema(ref_template="#/components/schemas/{model}")[
            "definitions"
        ][panosc_model.__name__]

        schema_name = panosc_model.__name__
        spec.components.schema(schema_name, schema)

    spec.components.parameter(
        "FILTER",
        "query",
        {
            "in": "query",
            "name": "filter",
            "description": "Apply filters to the query. The possible filters are:"
            " where, include, limit and skip. Please modify the examples before"
            " executing a request if you are having issues with the example values."
            ' must be a JSON-encoded string (`{"where":{"something":"value"}}`).'
            " See more details"
            ' <a href="https://loopback.io/doc/en/lb3/Querying-data.html#using'
            '-stringified-json-in-rest-queries">here</a>.',
            "schema": {"type": "string"},
            "examples": {
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
        },
    )
    spec.components.parameter(
        "WHERE_FILTER",
        "query",
        {
            "in": "query",
            "name": "where",
            "description": "Apply where filter to the query. The possible operators"
            " are: eq, neq, and, or, gt, gte, lt, lte, between, inq, nin, like, nlike,"
            " ilike, nilike and regexp. Please modify the examples before executing a "
            "request if you are having issues with the example values. See more details"
            ' <a href="https://loopback.io/doc/en/lb3/Where-filter.html">here</a>.',
            "schema": {"type": "string"},
            "examples": {
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
        },
    )
