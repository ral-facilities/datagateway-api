import pytest

from datagateway_api.read_only_api.models.request.investigation import (
    InvestigationOrderEnum,
    InvestigationSearchFilters,
)


class TestCommon:
    def test_validate_order(self) -> None:
        with pytest.raises(ValueError, match="Cannot order on the same field multiple times"):
            InvestigationSearchFilters(order=[InvestigationOrderEnum.TITLE_ASC, InvestigationOrderEnum.TITLE_DESC])
