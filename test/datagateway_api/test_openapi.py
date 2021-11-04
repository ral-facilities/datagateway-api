from datetime import date, datetime

import pytest

from datagateway_api.src.resources.datagateway_api.entities.entity_map import (
    type_conversion,
)


class TestOpenAPI:
    @pytest.mark.parametrize(
        "python_type, expected_type",
        [
            pytest.param(int, {"type": "integer"}, id="integer"),
            pytest.param(float, {"type": "number", "format": "float"}, id="float"),
            pytest.param(bool, {"type": "boolean"}, id="boolean"),
            pytest.param(
                datetime, {"type": "string", "format": "datetime"}, id="datetime",
            ),
            pytest.param(date, {"type": "string", "format": "date"}, id="date"),
            pytest.param(str, {"type": "string"}, id="string"),
        ],
    )
    def test_type_conversion(self, python_type, expected_type):
        openapi_type = type_conversion(python_type)
        assert openapi_type == expected_type
