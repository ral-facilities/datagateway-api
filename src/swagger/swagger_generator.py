import os
import re


class SwaggerGenerator(object):
    FILE_PATH = os.getcwd() + "\\swagger\\openapi.yaml"

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
            self.endpoints.append(cls.__name__)
            return cls

        return decorate
