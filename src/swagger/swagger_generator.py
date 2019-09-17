import re
from pathlib import Path

import yaml

from common.config import config


class Parameter(object):
    def __init__(self, description, name, param_type, example, location, is_required):
        self.parameter_as_dict = {
            "description": description,
            "in": location,
            "required": is_required,
            "name": name,
            "schema": {
                "type": param_type,
                "example": example
            }
        }


class Entity(object):
    WHERE_PARAMETER = Parameter(
        "Apply a where filter to all entities. The filter can take the form of {\"field\":{<operator>:\"value\"}, "
        "where the possible operators are like, gte, lte and eq",
        "where", "object", {"ID": {"eq": 1}}, "query", False).parameter_as_dict
    LIMIT_PARAMETER = Parameter("Limit the number of entities returned", "limit", "number", 4,
                                "query", False).parameter_as_dict
    SKIP_PARAMETER = Parameter("Offset the returned entities by a given number", "skip", "number", 5,
                               "query", False).parameter_as_dict
    ORDER_PARAMETER = Parameter("Given a field and direction, order the returned entities", "order", "string",
                                "ID DESC", "query", False).parameter_as_dict
    INCLUDE_PARAMETER = Parameter("Given the names of related entities, include them in the results", "include",
                                  "object", {"Relation 1": ["Relation A", "Relation B"]}, "query", False).parameter_as_dict
    DISTINCT_PARAMETER = Parameter("Return unique values for the fields requested", "distinct", "object",
                                   ["FIELD 1", "FIELD 2"], "query", False).parameter_as_dict
    PATH_PARAMETER = Parameter("The id of an entity", "id", "integer", 4, "path", True).parameter_as_dict

    def __init__(self, entity_name):
        self.entity_no_id_endpoint = {
            f"/{entity_name.lower()}": {
                "get": {
                    "summary": f"Get {SwaggerGenerator.pascal_to_normal(entity_name).lower()} based on filters",
                    "tags": ["entities"],
                    "parameters": [self.WHERE_PARAMETER,
                                   self.DISTINCT_PARAMETER,
                                   self.INCLUDE_PARAMETER,
                                   self.LIMIT_PARAMETER,
                                   self.ORDER_PARAMETER,
                                   self.SKIP_PARAMETER],
                    "responses": {
                        "200": {
                            "description": f"The {SwaggerGenerator.pascal_to_normal(entity_name).lower()} found"
                        },
                        "404": {
                            "description": "When no results are found"
                        },
                        "401": {
                            "description": "When no credentials are provided"
                        },
                        "403": {
                            "description": "When bad credentials are provided"
                        }
                    }
                },
                "post": {
                    "summary": f"Add new {SwaggerGenerator.pascal_to_normal(entity_name).lower()}",
                    "tags": ["entities"],
                    "requestBody": {
                        "description": f"Create one or multiple {SwaggerGenerator.pascal_to_normal(entity_name).lower()}",
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object"
                                }
                            }
                        }

                    },
                    "responses": {
                        "200": {
                            "description": f"The created {SwaggerGenerator.pascal_to_normal(entity_name)}"
                        },
                        "401": {
                            "description": "When no credentials are provided"
                        },
                        "403": {
                            "description": "When bad credentials are provided"
                        }
                    }
                },
                "patch": {
                    "summary": f"Update {SwaggerGenerator.pascal_to_normal(entity_name).lower()}",
                    "tags": ["entities"],
                    "requestBody": {
                        "description": f"Update one or multiple {SwaggerGenerator.pascal_to_normal(entity_name).lower()}",
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object"
                                }
                            }
                        }

                    },
                    "responses": {
                        "200": {
                            "description": "The updated entity"
                        },
                        "404": {
                            "description": "When the entity to update could not be found"
                        },
                        "401": {
                            "description": "When no credentials are provided"
                        },
                        "403": {
                            "description": "When bad credentials are provided"
                        }
                    }
                }
            }

        }
        self.entity_count_endpoint = {
            f"/{entity_name.lower()}/count": {
                "get": {
                    "summary": f"Return the count of the {SwaggerGenerator.pascal_to_normal(entity_name).lower()}",
                    "tags": ["entities"],
                    "parameters": [self.WHERE_PARAMETER],
                    "responses": {
                        "200": {
                            "description": f"The count of the {SwaggerGenerator.pascal_to_normal(entity_name).lower()}"
                        },
                        "401": {
                            "description": f"When no credentials are provided"
                        },
                        "403": {
                            "description": "When bad credentials are given"
                        }
                    }

                }

            }
        }
        self.entity_id_endpoint = {
            f"/{entity_name.lower()}/{{id}}": {
                "get": {
                    "summary": f"Find the {SwaggerGenerator.pascal_to_normal(entity_name).lower()} matching the ID",
                    "tags": ["entities"],
                    "parameters": [self.PATH_PARAMETER],
                    "responses": {
                        "200": {
                            "description": f"The matching {SwaggerGenerator.pascal_to_normal(entity_name).lower()}"
                        },
                        "404": {
                            "description": "When no result is found"
                        },
                        "401": {
                            "description": "When no credentials are provided"
                        },
                        "403": {
                            "description": "When bad credentials are provided"
                        }
                    }
                },
                "delete": {
                    "summary": f"Delete the {SwaggerGenerator.pascal_to_normal(entity_name).lower()} matching the ID",
                    "tags": ["entities"],
                    "parameters": [self.PATH_PARAMETER],
                    "responses": {
                        "203": {
                            "description": "Blank response when the entity is deleted"
                        },
                        "404": {
                            "description": "When the entity can't be found"
                        },
                        "401": {
                            "description": "When no credentials are provided"
                        },
                        "403": {
                            "description": "When bad credentials are provided"
                        }
                    }
                }
            }
        }


class SwaggerSpecification(object):
    def __init__(self):
        self.paths = []
        self.top_part = {
            'openapi': "3.0.0",
            "info": {
                "title": "DataGateway API",
                "description": "ICAT API to interface with the DataGateway",
                "version": "0"
            },
            "servers": [
                {
                    "url": "http://localhost:5000"
                }
            ],
            "paths": {}
        }

    def add_path(self, path):
        self.paths.append(path)

    def get_spec_as_dict(self):
        spec = {}
        for path in self.paths:
            self.top_part["paths"].update(path)
        spec.update(self.top_part)

        return spec


class SwaggerGenerator(object):
    FILE_PATH = Path.cwd() / "swagger" / "openapi.yaml"

    def __init__(self):
        self.endpoints = []

    @staticmethod
    def pascal_to_normal(input):
        """
        Converts PascalCase to words seperated by spaces. All lowercase

        :param input: The PascalCase input to be converted
        :return: The converted string
        """
        words = re.findall(r"[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+", input)
        return " ".join(map(str.lower, words))

    def resource_wrapper(self):
        """
        Wrapper for Resource classes that appends the class name to the endpoints list
        """

        def decorate(cls):
            if config.is_generate_swagger():
                self.endpoints.append(cls.__name__)
            return cls

        return decorate

    def write_swagger_spec(self):
        """
        Writes the openapi.yaml file

        """
        if config.is_generate_swagger():
            swagger_spec = SwaggerSpecification()
            for endpoint in self.endpoints:
                entity = Entity(endpoint)
                swagger_spec.add_path(entity.entity_count_endpoint)
                swagger_spec.add_path(entity.entity_id_endpoint)
                swagger_spec.add_path(entity.entity_no_id_endpoint)
            swagger_dict = swagger_spec.get_spec_as_dict()
            yaml.Dumper.ignore_aliases = lambda *args : True
            with open(SwaggerGenerator.FILE_PATH, "w+") as target:
                target.write(yaml.dump(swagger_dict))
            target.close()


swagger_gen = SwaggerGenerator()
