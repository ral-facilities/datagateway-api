from unittest import TestCase

from src.swagger.swagger_generator import SwaggerGenerator


class TestSwaggerGenerator(TestCase):
    def test_pascal_to_normal(self):
        self.assertEqual(SwaggerGenerator.pascal_to_normal("TestCase"), "test case")
        self.assertEqual(SwaggerGenerator.pascal_to_normal("testCase"), "test case")