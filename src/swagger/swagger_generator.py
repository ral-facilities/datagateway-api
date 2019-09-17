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
            with open(SwaggerGenerator.FILE_PATH, "w+") as target:
                target.write(self.get_yaml_top())
                target.write(self.get_yaml_paths())
            target.close()


swagger_gen = SwaggerGenerator()
