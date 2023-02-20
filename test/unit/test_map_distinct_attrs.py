from datetime import datetime

from dateutil.tz import tzlocal
import pytest

from datagateway_api.src.common.helpers import map_distinct_attributes_to_results


class TestMapDistinctAttrs:
    @pytest.mark.parametrize(
        "distinct_attrs, result, expected_output",
        [
            pytest.param(
                ["summary"],
                ["Summary 1"],
                {"summary": "Summary 1"},
                id="Single attribute",
            ),
            pytest.param(
                ["startDate"],
                (
                    datetime(
                        year=2020,
                        month=1,
                        day=4,
                        hour=1,
                        minute=1,
                        second=1,
                        tzinfo=tzlocal(),
                    ),
                ),
                {"startDate": "2020-01-04 01:01:01+00:00"},
                id="Single date attribute",
            ),
            pytest.param(
                ["summary", "title"],
                ("Summary 1", "Title 1"),
                {"summary": "Summary 1", "title": "Title 1"},
                id="Multiple attributes",
            ),
            pytest.param(
                ["summary", "investigationUsers.role"],
                ("Summary 1", "PI"),
                {"summary": "Summary 1", "investigationUsers": {"role": "PI"}},
                id="Multiple attributes with related attribute",
            ),
            pytest.param(
                ["summary", "investigationUsers.investigation.name"],
                ("Summary 1", "Investigation Name 1"),
                {
                    "summary": "Summary 1",
                    "investigationUsers": {
                        "investigation": {"name": "Investigation Name 1"},
                    },
                },
                id="Multiple attributes with 2-level nested related attribute",
            ),
        ],
    )
    def test_valid_map_distinct_attributes_to_results(
        self, distinct_attrs, result, expected_output,
    ):
        test_output = map_distinct_attributes_to_results(distinct_attrs, result)

        assert test_output == expected_output
