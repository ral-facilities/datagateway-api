from src.resources.entities.entity_map import create_entity_models


def initialise_spec(spec):
    """
    Given a apispec spec object, will initialise it with the security scheme, models and
    parameters we use

    :spec: ApiSpec: spec object to initialise
    :return: void
    """

    spec.components.security_scheme(
        "session_id", {"type": "http", "scheme": "bearer", "bearerFormat": "uuid"}
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
            "description": "Apply where filters to the query. The possible operators are like, gte, lte, in and eq",
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
                                        ]
                                    }
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
                                        ]
                                    }
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
                                        ]
                                    }
                                },
                            },
                            {
                                "type": "object",
                                "title": "Substring equality",
                                "properties": {"like": {"type": "string"}},
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
                                            ]
                                        },
                                    }
                                },
                            },
                        ],
                    },
                },
            },
            "examples": {
                "eq": {"value": [{"ID": {"eq": 1}}]},
                "like": {"value": [{"NAME": {"like": "dog"}}]},
                "gte": {"value": [{"ID": {"gte": 50}}]},
                "lte": {"value": [{"ID": {"lte": 50}}]},
                "in": {"value": [{"ID": {"in": [1, 2, 3]}}]},
            },
        },
    )

    spec.components.parameter(
        "ORDER_FILTER",
        "query",
        {
            "in": "query",
            "name": "order",
            "description": "Apply order filters to the query. Given a field and direction, order the returned entities.",
            "schema": {"type": "array", "items": {"type": "string"}},
            "examples": {"asc": {"value": ["ID asc"]}, "desc": {"value": ["ID desc"]}},
        },
    )

    spec.components.parameter(
        "LIMIT_FILTER",
        "query",
        {
            "in": "query",
            "name": "limit",
            "description": "Apply limit filter to the query. Limit the number of entities returned.",
            "schema": {"type": "integer"},
        },
    )

    spec.components.parameter(
        "SKIP_FILTER",
        "query",
        {
            "in": "query",
            "name": "skip",
            "description": "Apply skip filter to the query. Offset the returned entities by a given number.",
            "schema": {"type": "integer"},
        },
    )
    spec.components.parameter(
        "DISTINCT_FILTER",
        "query",
        {
            "in": "query",
            "name": "distinct",
            "description": "Apply distinct filter to the query. Return unique values for the fields requested.",
            "schema": {"type": "array", "items": {"type": "string"}},
        },
    )
    spec.components.parameter(
        "INCLUDE_FILTER",
        "query",
        {
            "in": "query",
            "name": "include",
            "description": "Apply include filter to the query. Given the names of related entities, include them in the results. Only one include parameter is allowed.",
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
                                        ]
                                    },
                                },
                            ]
                        },
                    },
                    {
                        "type": "object",
                        "additionalProperties": {
                            "oneOf": [
                                {"type": "string"},
                                {"type": "array", "items": [{"type": "string"}]},
                            ]
                        },
                    },
                ]
            },
            "examples": {
                "single": {"value": "RELATED_COLUMN"},
                "array": {"value": ["RELATED_COLUMN_1", "RELATED_COLUMN_2"]},
                "multi-level": {
                    "value": {"RELATED_COLUMN": "RELATED_COLUMN_RELATED_COLUMN"}
                },
                "multi-level array": {
                    "value": {
                        "RELATED_COLUMN": [
                            "RELATED_COLUMN_RELATED_COLUMN_1",
                            "RELATED_COLUMN_RELATED_COLUMN_2",
                        ]
                    }
                },
                "array of multi-level": {
                    "value": [
                        "RELATED_COLUMN_1",
                        {"RELATED_COLUMN_2": "RELATED_COLUMN_2_RELATED_COLUMN_1"},
                        {
                            "RELATED_COLUMN_3": [
                                "RELATED_COLUMN_3_RELATED_COLUMN_1",
                                "RELATED_COLUMN_3_RELATED_COLUMN_2",
                            ]
                        },
                    ]
                },
            },
        },
    )
