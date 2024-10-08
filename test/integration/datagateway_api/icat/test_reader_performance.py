from unittest.mock import patch

import pytest

from datagateway_api.src.common.config import Config
from datagateway_api.src.datagateway_api.icat.filters import (
    PythonICATLimitFilter,
    PythonICATOrderFilter,
    PythonICATWhereFilter,
)
from datagateway_api.src.datagateway_api.icat.helpers import (
    get_data_with_filters,
    is_use_reader_for_performance_enabled,
)
from datagateway_api.src.datagateway_api.icat.icat_client_pool import ICATClient
from datagateway_api.src.datagateway_api.icat.reader_query_handler import (
    ReaderQueryHandler,
)


class TestReaderPerformance:
    @pytest.mark.parametrize(
        "test_entity_type, test_query_filters, expected_eligbility",
        [
            pytest.param(
                "Dataset",
                [PythonICATWhereFilter("investigation.id", 3, "eq")],
                True,
                id="Typical use case for dataset",
            ),
            pytest.param(
                "Datafile",
                [PythonICATWhereFilter("dataset.id", 3, "eq")],
                True,
                id="Typical use case for datafile",
            ),
            pytest.param(
                "Datafile",
                [
                    PythonICATLimitFilter(50),
                    PythonICATOrderFilter("id", "asc"),
                    PythonICATWhereFilter("dataset.id", 3, "eq"),
                ],
                True,
                id="Typical use case with multiple query filters",
            ),
            pytest.param(
                "Datafile",
                [PythonICATLimitFilter(25)],
                False,
                id="Query with no relevant filters",
            ),
            pytest.param(
                "User",
                [PythonICATWhereFilter("studies.id", 3, "eq")],
                False,
                id="Query on an entity type that isn't relevant for reader performance",
            ),
        ],
    )
    @patch(
        "datagateway_api.src.common.config.Config.config.datagateway_api"
        ".use_reader_for_performance.enabled",
        return_value=True,
    )
    def test_eligbility(
        self, _, test_entity_type, test_query_filters, expected_eligbility,
    ):
        reader_performance_enabled = is_use_reader_for_performance_enabled()
        assert reader_performance_enabled

        # Check eligbility method is executed in init
        test_handler = ReaderQueryHandler(test_entity_type, test_query_filters)
        query_eligbility = test_handler.is_query_eligible_for_reader_performance()
        assert query_eligbility == expected_eligbility

    def test_reader_client(self):
        ReaderQueryHandler("Datafile", [])
        reader_client = ReaderQueryHandler.reader_client
        assert isinstance(reader_client, ICATClient)

        reader_config = Config.config.datagateway_api.use_reader_for_performance
        assert (
            reader_client.getUserName()
            == f"{reader_config.reader_mechanism}/{reader_config.reader_username}"
        )

    @pytest.mark.parametrize(
        "test_entity_type, test_query_filters, expected_authorisation",
        [
            pytest.param(
                "Datafile",
                [PythonICATWhereFilter("dataset.id", 3, "eq")],
                True,
                id="Typical positive use case",
            ),
            pytest.param(
                "Datafile",
                [PythonICATWhereFilter("dataset.id", 99999, "eq")],
                False,
                id="Typical negative use case",
            ),
        ],
    )
    def test_is_user_authorised(
        self, icat_client, test_entity_type, test_query_filters, expected_authorisation,
    ):
        test_handler = ReaderQueryHandler(test_entity_type, test_query_filters)
        is_authorised = test_handler.is_user_authorised_to_see_entity_id(icat_client)
        assert is_authorised == expected_authorisation

    @patch("datagateway_api.src.datagateway_api.icat.helpers.execute_entity_query")
    @patch(
        "datagateway_api.src.common.config.Config.config.datagateway_api"
        ".use_reader_for_performance.enabled",
        return_value=True,
    )
    def test_execute_query_as_reader(self, _, mock_execute_entity_query, icat_client):
        get_data_with_filters(
            icat_client, "Datafile", [PythonICATWhereFilter("dataset.id", 3, "eq")],
        )
        assert mock_execute_entity_query.call_count == 1

        client = mock_execute_entity_query.call_args_list[0][0][0]
        assert client.getUserName() == "simple/reader"
