import os
import re
from pathlib import Path


class SwaggerGenerator(object):
    FILE_PATH = Path.cwd() / "swagger" / "openapi.yaml"
    is_generating = False

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
        if SwaggerGenerator.is_generating:
            def decorate(cls):
                self.endpoints.append(cls.__name__)
                return cls

            return decorate

    def write_swagger_spec(self):
        """
        Writes the openapi.yaml file

        """
        if SwaggerGenerator.is_generating:
            with open(SwaggerGenerator.FILE_PATH, "w+") as target:
                target.write(self.get_yaml_top())
                target.write(self.get_yaml_paths())
            target.close()

    @staticmethod
    def get_yaml_top():
        """
        Gets the top part of the openapi spec without the paths

        :return: String containing the top part of the openapi spec
        """
        return (f'''openapi: "3.0.0"
info:
  title: DataGateway API
  description: ICAT API to interface with the Data Gateway
  version: "0"
servers:
  - url: http://localhost:5000

paths:''')

    def get_yaml_paths(self):
        """
        Gets the paths for the openapi spec

        :return: String containing the paths and their methods of the openapi spec
        """
        base = ""
        for endpoint in self.endpoints:
            base += f'''
  /{endpoint.lower()}:
    get:
      summary: Get {SwaggerGenerator.pascal_to_normal(endpoint).lower()}
      tags:
        - Entities
      parameters:
        - name: where
          in: query
          description: Apply a where filter to the {SwaggerGenerator.pascal_to_normal(endpoint).lower()}
          required: false
          schema:
            type: object
        - name: limit
          in: query
          description: Limit the number of {SwaggerGenerator.pascal_to_normal(endpoint).lower()} returned
          required: false
          schema:
            type: object
        - name: skip
          in: query
          description: Skip the number of {SwaggerGenerator.pascal_to_normal(endpoint).lower()} returned
          required: false
          schema:
            type: object
        - name: order
          in: query
          description: order the {SwaggerGenerator.pascal_to_normal(endpoint).lower()} by the given field
          required: false
          schema:
            type: object
        - name: include
          in: query
          description: include the related entities given
          required: false
          schema:
            type: object
      responses:
        '200':
           description: The {SwaggerGenerator.pascal_to_normal(endpoint).lower()} found.
        '404':
          description: When no result is found
    post:
      summary: Create one of more {SwaggerGenerator.pascal_to_normal(endpoint).lower()}
      tags:
        - Entities
      responses:
        '200': 
          description: The created {SwaggerGenerator.pascal_to_normal(endpoint).lower()}
    patch:
      summary: Update one or multiple {SwaggerGenerator.pascal_to_normal(endpoint).lower()}
      tags:
        - Entities
      responses:
        200:
          description: The updated {SwaggerGenerator.pascal_to_normal(endpoint).lower()}
  /{endpoint.lower()}/count:
    get:
      summary: Return the count of the {SwaggerGenerator.pascal_to_normal(endpoint).lower()}
      tags:
        - Entities
      parameters:
        - name: where
          in: query
          description: Apply a where filter to the {SwaggerGenerator.pascal_to_normal(endpoint).lower()}
          required: false
          schema:
            type: object
      responses:
        200:
          description: The count of {SwaggerGenerator.pascal_to_normal(endpoint).lower()}
  /{endpoint.lower()}/findOne:
    get:
      summary: Return the first {SwaggerGenerator.pascal_to_normal(endpoint).lower()} matching a given filter
      tags:
        - Entities
      parameters:
        - name: where
          in: query
          description: Apply a where filter to the {SwaggerGenerator.pascal_to_normal(endpoint).lower()}
          required: false
          schema:
            type: object
        - name: limit
          in: query
          description: Limit the number of {SwaggerGenerator.pascal_to_normal(endpoint).lower()} returned
          required: false
          schema:
            type: object
        - name: skip
          in: query
          description: Skip the number of {SwaggerGenerator.pascal_to_normal(endpoint).lower()} returned
          required: false
          schema:
            type: object
        - name: order
          in: query
          description: order the {SwaggerGenerator.pascal_to_normal(endpoint).lower()} by the given field
          required: false
          schema:
            type: object
        - name: include
          in: query
          description: include the related entities given
          required: false
          schema:
            type: object
      responses:
        200:
          description: The first {SwaggerGenerator.pascal_to_normal(endpoint).lower()} matching
  /{endpoint.lower()}/{{id}}:
    get:
      summary: Find the {SwaggerGenerator.pascal_to_normal(endpoint).lower()} matching the given ID
      tags:
        - Entities
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: integer
          description: The id matching the {SwaggerGenerator.pascal_to_normal(endpoint).lower()}
      responses:
        '200': 
          description: The matching {SwaggerGenerator.pascal_to_normal(endpoint).lower()}
        '404':
          description: When no {SwaggerGenerator.pascal_to_normal(endpoint).lower()} matches the given ID
    delete:
      summary: Delete the {SwaggerGenerator.pascal_to_normal(endpoint).lower()} matching the given ID
      tags:
        - Entities
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: integer
          description: The id matching the {SwaggerGenerator.pascal_to_normal(endpoint).lower()}
      responses:
        '203':
          description: Blank responses, when the {SwaggerGenerator.pascal_to_normal(endpoint).lower()} is deleted
        '404':
          description: When the {SwaggerGenerator.pascal_to_normal(endpoint).lower()} can't be found
    patch:
      summary: Update the {SwaggerGenerator.pascal_to_normal(endpoint).lower()} matching the given ID
      tags:
        - Entities
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: integer
          description: The id matching the {SwaggerGenerator.pascal_to_normal(endpoint).lower()}
      responses:
        '200':
          description: The updated {SwaggerGenerator.pascal_to_normal(endpoint).lower()}
        '404':
          description: When the {SwaggerGenerator.pascal_to_normal(endpoint).lower()} can't be found'''
        return base


swagger_gen = SwaggerGenerator()
