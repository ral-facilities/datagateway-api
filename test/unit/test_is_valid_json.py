import pytest

from datagateway_api.common.helpers import is_valid_json


class TestIsValidJSON:
    @pytest.mark.parametrize(
        "input_json",
        [
            pytest.param("[]", id="empty array"),
            pytest.param("null", id="null"),
            pytest.param('{"test":1}', id="key-value pair"),
            pytest.param('{"test":{"inner_key":"inner_value"}}', id="nested json"),
        ],
    )
    def test_valid_json_input(self, input_json):
        valid_json = is_valid_json(input_json)

        assert valid_json

    @pytest.mark.parametrize(
        "invalid_json",
        [
            pytest.param("{'test':1}", id="single quotes"),
            pytest.param(None, id="none"),
            pytest.param(1, id="integer"),
            pytest.param({"test": 1}, id="dictionary"),
            pytest.param([], id="empty list"),
        ],
    )
    def test_invalid_json_input(self, invalid_json):
        valid_json = is_valid_json(invalid_json)

        assert not valid_json
