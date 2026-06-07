from datetime import datetime
import time
from typing import Generator

from icat.client import Client
import pytest

from datagateway_api.common.config import APIConfig, Config
from datagateway_api.common.exceptions import MissingRecordError, PythonICATError
from datagateway_api.datagateway_api.icat.filters import (
    PythonICATLimitFilter,
    PythonICATOrderFilter,
    PythonICATWhereFilter,
)
from datagateway_api.datagateway_api.icat.helpers import (
    get_data_with_filters,
    is_use_reader_for_performance_enabled,
)
from datagateway_api.datagateway_api.icat.icat_client_pool import ICATClient
from datagateway_api.datagateway_api.icat.reader_query_handler import (
    ReaderQueryHandler,
)


@pytest.fixture(scope="class")
def enable_reader_permissions(icat_client: Client) -> Generator[None, None, None]:
    entities = []
    try:
        user = icat_client.new(obj="User", name="simple/reader")
        grouping = icat_client.new(obj="Grouping", name="reader")
        user.id, grouping.id = icat_client.createMany(beans=[user, grouping])
        entities = [user, grouping]
        icat_client.createMany(
            beans=[
                icat_client.new("UserGroup", user=user, grouping=grouping),
                icat_client.new(obj="Rule", crudFlags="R", what="User", grouping=grouping),
                icat_client.new(obj="Rule", crudFlags="R", what="InvestigationUser", grouping=grouping),
                icat_client.new(obj="Rule", crudFlags="R", what="InstrumentScientist", grouping=grouping),
                icat_client.new(obj="Rule", crudFlags="R", what="Instrument", grouping=grouping),
                icat_client.new(obj="Rule", crudFlags="R", what="InvestigationInstrument", grouping=grouping),
                icat_client.new(obj="Rule", crudFlags="R", what="Investigation", grouping=grouping),
                icat_client.new(obj="Rule", crudFlags="R", what="Dataset", grouping=grouping),
                icat_client.new(obj="Rule", crudFlags="R", what="Datafile", grouping=grouping),
                icat_client.new(obj="Rule", crudFlags="R", what="DataPublication", grouping=grouping),
                icat_client.new(obj="Rule", crudFlags="R", what="DataCollection", grouping=grouping),
                icat_client.new(obj="Rule", crudFlags="R", what="DataCollectionDataset", grouping=grouping),
            ],
        )
        yield
    finally:
        icat_client.deleteMany(beans=entities)


@pytest.fixture(scope="class")
def associate_icat_user(icat_client: Client) -> Generator[None, None, None]:
    user = None
    try:
        user = icat_client.new(
            obj="User",
            name="simple/icatuser",
            investigationUsers=[
                icat_client.new(obj="InvestigationUser", role="", investigation=icat_client.get("Investigation", 2)),
                icat_client.new(obj="InvestigationUser", role="", investigation=icat_client.get("Investigation", 3)),
            ],
            instrumentScientists=[
                icat_client.new(obj="InstrumentScientist", instrument=icat_client.get("Instrument", 13)),
                icat_client.new(obj="InstrumentScientist", instrument=icat_client.get("Instrument", 14)),
            ],
        )
        user.create()
        yield
    finally:
        if user is not None and user.id is not None:
            icat_client.delete(bean=user)


@pytest.fixture(scope="class")
def associate_data_publication(icat_client: Client) -> Generator[None, None, None]:
    data_collection = None
    try:
        data_collection = icat_client.new(
            obj="DataCollection",
            dataPublications=[
                icat_client.new(
                    obj="DataPublication",
                    title="title",
                    pid="pid",
                    publicationDate=datetime.now(),
                    facility=icat_client.get("Facility", 1),
                    type=icat_client.get("DataPublicationType", 1),
                ),
            ],
            dataCollectionDatasets=[
                icat_client.new(obj="DataCollectionDataset", dataset=icat_client.get("Dataset", 6)),
            ],
        )
        data_collection.create()
        yield
    finally:
        if data_collection is not None and data_collection.id is not None:
            icat_client.delete(bean=data_collection)


@pytest.fixture(scope="class")
def icat_user_client() -> Client:
    client = Client(url=Config.config.datagateway_api.icat_url, checkCert=Config.config.datagateway_api.icat_check_cert)
    client.login(auth="simple", credentials={"username": "icatuser", "password": "icatuserpw"})
    return client


@pytest.fixture(scope="class")
def icat_root_client() -> Client:
    client = Client(url=Config.config.datagateway_api.icat_url, checkCert=Config.config.datagateway_api.icat_check_cert)
    client.login(auth="simple", credentials={"username": "root", "password": "pw"})
    return client


@pytest.fixture(scope="function")
def enable_reader_config() -> Generator[None, None, None]:
    Config.config.datagateway_api.use_reader_for_performance.enabled = True
    yield
    Config.config = APIConfig.load()


@pytest.fixture(scope="function")
def enable_reader_bad_config() -> Generator[None, None, None]:
    Config.config.datagateway_api.use_reader_for_performance.enabled = True
    Config.config.datagateway_api.use_reader_for_performance.reader_mechanism = "bad"
    yield
    Config.config = APIConfig.load()


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
    def test_eligbility(
        self,
        enable_reader_config: None,
        test_entity_type,
        test_query_filters,
        expected_eligbility,
    ):
        reader_performance_enabled = is_use_reader_for_performance_enabled()
        assert reader_performance_enabled

        # Check eligbility method is executed in init
        test_handler = ReaderQueryHandler(test_entity_type, test_query_filters)
        query_eligbility = test_handler.is_query_eligible_for_reader_performance()
        assert query_eligbility == expected_eligbility

    def test_reader_client(self, enable_reader_config: None):
        ReaderQueryHandler("Datafile", [])
        reader_client = ReaderQueryHandler.reader_client
        assert isinstance(reader_client, ICATClient)
        assert reader_client.getUserName() == (
            f"{Config.config.datagateway_api.use_reader_for_performance.reader_mechanism}/{Config.config.datagateway_api.use_reader_for_performance.reader_username}"
        )

    @pytest.mark.parametrize(
        ["entity_type", "filters", "results_length"],
        [
            pytest.param("Dataset", [PythonICATWhereFilter("investigation.id", 1, "eq")], 0),
            pytest.param("Datafile", [PythonICATWhereFilter("dataset.id", 1, "eq")], 0),
            pytest.param("Dataset", [PythonICATWhereFilter("investigation.id", 2, "eq")], 2),
            pytest.param("Datafile", [PythonICATWhereFilter("dataset.id", 2, "eq")], 16),
            pytest.param("Dataset", [PythonICATWhereFilter("investigation.id", 3, "eq")], 2),
            pytest.param("Datafile", [PythonICATWhereFilter("dataset.id", 3, "eq")], 16),
            pytest.param("Dataset", [PythonICATWhereFilter("investigation.id", 4, "eq")], 2),
            pytest.param("Datafile", [PythonICATWhereFilter("dataset.id", 4, "eq")], 16),
        ],
    )
    def test_execute_query_as_reader(
        self,
        enable_reader_config: None,
        enable_reader_permissions: None,
        associate_icat_user: None,
        icat_user_client: Client,
        entity_type: str,
        filters: list[PythonICATWhereFilter],
        results_length: int,
    ) -> None:
        results = get_data_with_filters(client=icat_user_client, entity_type=entity_type, filters=filters)
        assert len(results) == results_length

    @pytest.mark.parametrize(
        ["filters", "results_length"],
        [
            pytest.param([PythonICATWhereFilter("dataset.id", 6, "eq")], 16, id="Dataset in a DataPublication"),
            pytest.param([PythonICATWhereFilter("dataset.id", 7, "eq")], 0, id="Dataset not in a DataPublication"),
        ],
    )
    def test_open_data(
        self,
        enable_reader_config: None,
        enable_reader_permissions: None,
        associate_data_publication: None,
        icat_user_client: Client,
        filters: list[PythonICATWhereFilter],
        results_length: int,
    ) -> None:
        results = get_data_with_filters(client=icat_user_client, entity_type="Datafile", filters=filters)
        assert len(results) == results_length

    @pytest.mark.parametrize(
        ["entity_type", "filters", "results_length"],
        [
            pytest.param("Dataset", [PythonICATWhereFilter("investigation.id", 1, "eq")], 2),
            pytest.param("Datafile", [PythonICATWhereFilter("dataset.id", 1, "eq")], 15),
        ],
    )
    def test_root_access(
        self,
        enable_reader_config: None,
        enable_reader_permissions: None,
        associate_data_publication: None,
        icat_root_client: Client,
        entity_type: str,
        filters: list[PythonICATWhereFilter],
        results_length: int,
    ) -> None:
        results = get_data_with_filters(client=icat_root_client, entity_type=entity_type, filters=filters)
        assert len(results) == results_length

    def test_refresh(self, enable_reader_config: None) -> None:
        client = Client(
            url=Config.config.datagateway_api.icat_url,
            checkCert=Config.config.datagateway_api.icat_check_cert,
        )
        client._next_refresh = 0
        ReaderQueryHandler.reader_client = client
        ReaderQueryHandler.refresh()
        current_time = time.time()
        assert current_time + 89 * 60 < ReaderQueryHandler.reader_client._next_refresh < current_time + 90 * 60

    def test_refresh_failure(self, enable_reader_bad_config: None) -> None:
        client = Client(
            url=Config.config.datagateway_api.icat_url,
            checkCert=Config.config.datagateway_api.icat_check_cert,
        )
        client._next_refresh = 0
        ReaderQueryHandler.reader_client = client
        with pytest.raises(PythonICATError, match="Internal error with reader account configuration"):
            ReaderQueryHandler.refresh()

    def test_get_investigation_id_failure(self, enable_reader_config: None) -> None:
        with pytest.raises(expected_exception=MissingRecordError, match="No Dataset found for id=-1"):
            ReaderQueryHandler.get_investigation_id(dataset_id=-1)
