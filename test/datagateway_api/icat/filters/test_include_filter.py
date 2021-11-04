import pytest

from datagateway_api.common.datagateway_api.icat.filters import PythonICATIncludeFilter
from datagateway_api.common.exceptions import FilterError


class TestICATIncludeFilter:
    @pytest.mark.parametrize(
        "filter_input, expected_output",
        [
            pytest.param("investigationUsers", {"investigationUsers"}, id="string"),
            pytest.param(
                {"investigationUsers": "user"},
                {"investigationUsers.user"},
                id="dictionary",
            ),
            pytest.param(
                {"datasets": ["datafiles", "sample"]},
                {"datasets.datafiles", "datasets.sample"},
                id="dictionary with list",
            ),
            pytest.param(
                {"datasets": {"datafiles": "datafileFormat"}},
                {"datasets.datafiles.datafileFormat"},
                id="nested dictionary",
            ),
            pytest.param(
                ["studyInvestigations", "datasets", "facility"],
                {"studyInvestigations", "datasets", "facility"},
                id="list of strings",
            ),
            pytest.param(
                [{"investigationUsers": "user"}, {"datasets": "datafiles"}],
                {"investigationUsers.user", "datasets.datafiles"},
                id="list of dictionaries",
            ),
            pytest.param(
                ["investigationUsers", ["datasets", "facility"]],
                {"investigationUsers", "datasets", "facility"},
                id="nested list",
            ),
            pytest.param(
                {"investigationUsers": [{"user": "userGroups"}, "investigation", []]},
                {
                    "investigationUsers.user.userGroups",
                    "investigationUsers.investigation",
                },
                id="complex use case used similarly in DataGateway",
            ),
            pytest.param(
                {"investigationUsers": [["investigation.datasets"]]},
                {"investigationUsers.investigation.datasets"},
                id="dictionary with nested list value",
            ),
        ],
    )
    def test_valid_input(self, icat_query, filter_input, expected_output):
        test_filter = PythonICATIncludeFilter(filter_input)
        test_filter.apply_filter(icat_query)

        assert icat_query.includes == expected_output

    def test_invalid_type(self, icat_query):
        with pytest.raises(FilterError):
            PythonICATIncludeFilter({"datasets", "facility"})

    def test_invalid_field(self, icat_query):
        test_filter = PythonICATIncludeFilter("invalidField")
        with pytest.raises(FilterError):
            test_filter.apply_filter(icat_query)

    @pytest.mark.parametrize(
        "filter_input",
        [
            pytest.param({2: "datasets"}, id="invalid dictionary key"),
            pytest.param(
                {"datasets": {2: "datafiles"}}, id="invalid inner dictionary key",
            ),
            pytest.param(
                {"datasets": {"datafiles", "sample"}},
                id="invalid inner dictionary value",
            ),
            pytest.param(
                {"investigationUsers": [{2: "userGroups"}, "investigation"]},
                id="Invalid inner key with nested dict and list",
            ),
        ],
    )
    def test_invalid_extract_field(self, filter_input):
        with pytest.raises(FilterError):
            PythonICATIncludeFilter(filter_input)
