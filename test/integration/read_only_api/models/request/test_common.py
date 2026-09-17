import json

import pytest

from datagateway_api.read_only_api.models.request.common import CommonWhereFilter, validate_order
from datagateway_api.read_only_api.models.request.investigation import InvestigationOrderEnum


class TestCommon:
    @pytest.mark.parametrize(
        ["obj"],
        [pytest.param({"name": {"eq": "name"}}), pytest.param(json.dumps({"name": {"eq": "name"}}))],
    )
    def test_common_where_filter(self, obj: dict[str, dict[str, str]] | str) -> None:
        CommonWhereFilter.model_validate(obj)

    def test_validate_order(self) -> None:
        with pytest.raises(ValueError, match="Cannot order on the same field multiple times"):
            validate_order([InvestigationOrderEnum.TITLE_ASC, InvestigationOrderEnum.TITLE_DESC])
