from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials
from object_pool import ObjectPool
from pydantic import PositiveInt

from datagateway_api.auth.session_bearer import SessionBearer
from datagateway_api.datagateway_api.icat.filters import PythonICATWhereFilter
from datagateway_api.datagateway_api.icat.python_icat import PythonICAT
from datagateway_api.read_only_api.models import (
    DataPublication,
    DataPublicationCountFilters,
    DataPublicationGetFilters,
    DataPublicationSearchFilters,
    Datafile,
    DatafileCountFilters,
    DatafileSearchFilters,
    Dataset,
    DatasetCountFilters,
    DatasetGetFilters,
    DatasetSearchFilters,
    FacilityCycle,
    FacilityCycleCountFilters,
    FacilityCycleSearchFilters,
    Instrument,
    InstrumentCountFilters,
    InstrumentGetFilters,
    InstrumentSearchFilters,
    Investigation,
    InvestigationCountFilters,
    InvestigationGetFilters,
    InvestigationSearchFilters,
    InvestigationUser,
    InvestigationUserSearchFilters,
)
from datagateway_api.read_only_api.models.request.datafile import DatafileFindOneFilters
from datagateway_api.read_only_api.models.request.dataset import DatasetFindOneFilters
from datagateway_api.read_only_api.models.request.investigation import InvestigationFindOneFilters

SessionId = Annotated[HTTPAuthorizationCredentials, Depends(SessionBearer())]


def instrument_endpoints(python_icat: PythonICAT, client_pool: ObjectPool) -> APIRouter:
    router = APIRouter(tags=["Instrument"])

    @router.get(
        "/instruments",
        summary="Get Instruments",
        description="Get Instruments and related Entities based on the provided filters.",
        response_model=list[Instrument],
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns Instruments that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_instruments(
        session_id: SessionId,
        instrument_filters: Annotated[InstrumentSearchFilters, Query()],
    ) -> list[Instrument]:
        return python_icat.get_with_filters(
            session_id=session_id,
            entity_type="Instrument",
            filters=instrument_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/instruments/count",
        summary="Count Instruments",
        description="Count Instruments based on the provided filters.",
        response_model=int,
        responses={
            200: {"description": "Success - The number of Instruments that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def count_instruments(
        session_id: SessionId,
        instrument_filters: Annotated[InstrumentCountFilters, Query()],
    ) -> list[Instrument]:
        return python_icat.count_with_filters(
            session_id=session_id,
            entity_type="Instrument",
            filters=instrument_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/instruments/{instrument_id}",
        summary="Get a single Instrument",
        description="Get a single Instrument and related Entities based on the provided id",
        response_model=Instrument,
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns the requested Instrument"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_instrument(
        session_id: SessionId,
        instrument_id: PositiveInt,
        instrument_filters: Annotated[InstrumentGetFilters, Query()],
    ) -> Instrument:
        return python_icat.get_with_id(
            session_id=session_id,
            entity_type="Instrument",
            id_=instrument_id,
            includes=instrument_filters.model_dump(),
            client_pool=client_pool,
        )

    return router


def facility_cycle_endpoints(python_icat: PythonICAT, client_pool: ObjectPool) -> APIRouter:
    router = APIRouter(tags=["FacilityCycle"])

    @router.get(
        "/facilitycycles",
        summary="Get FacilityCycles",
        description="Get FacilityCycles and related Entities based on the provided filters.",
        response_model=list[FacilityCycle],
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns FacilityCycles that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_facility_cycles(
        session_id: SessionId,
        facility_cycle_filters: Annotated[FacilityCycleSearchFilters, Query()],
    ) -> list[FacilityCycle]:
        return python_icat.get_with_filters(
            session_id=session_id,
            entity_type="FacilityCycle",
            filters=facility_cycle_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/facilitycycles/count",
        summary="Count FacilityCycles",
        description="Count FacilityCycles based on the provided filters.",
        response_model=int,
        responses={
            200: {"description": "Success - The number of FacilityCycles that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def count_facility_cycles(
        session_id: SessionId,
        facility_cycle_filters: Annotated[FacilityCycleCountFilters, Query()],
    ) -> list[FacilityCycle]:
        return python_icat.count_with_filters(
            session_id=session_id,
            entity_type="FacilityCycle",
            filters=facility_cycle_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/facilitycycles/{facility_cycle_id}",
        summary="Get a single FacilityCycle",
        description="Get a single FacilityCycle and related Entities based on the provided id",
        response_model=FacilityCycle,
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns the requested FacilityCycle"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_facility_cycle(session_id: SessionId, facility_cycle_id: PositiveInt) -> FacilityCycle:
        return python_icat.get_with_id(
            session_id=session_id,
            entity_type="FacilityCycle",
            id_=facility_cycle_id,
            client_pool=client_pool,
        )

    return router


def data_publication_endpoints(python_icat: PythonICAT, client_pool: ObjectPool) -> APIRouter:
    router = APIRouter(tags=["DataPublication"])

    @router.get(
        "/datapublications",
        summary="Get DataPublications",
        description="Get DataPublications and related Entities based on the provided filters.",
        response_model=list[DataPublication],
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns DataPublications that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_data_publications(
        session_id: SessionId,
        data_publication_filters: Annotated[DataPublicationSearchFilters, Query()],
    ) -> list[DataPublication]:
        return python_icat.get_with_filters(
            session_id=session_id,
            entity_type="DataPublication",
            filters=data_publication_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/datapublications/count",
        summary="Count DataPublications",
        description="Count DataPublications based on the provided filters.",
        response_model=int,
        responses={
            200: {"description": "Success - The number of DataPublications that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def count_data_publications(
        session_id: SessionId,
        data_publication_filters: Annotated[DataPublicationCountFilters, Query()],
    ) -> list[DataPublication]:
        return python_icat.count_with_filters(
            session_id=session_id,
            entity_type="DataPublication",
            filters=data_publication_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/datapublications/{data_publication_id}",
        summary="Get a single DataPublication",
        description="Get a single DataPublication and related Entities based on the provided id",
        response_model=DataPublication,
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns the requested DataPublication"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_data_publication(
        session_id: SessionId,
        data_publication_id: PositiveInt,
        data_publication_filters: Annotated[DataPublicationGetFilters, Query()],
    ) -> DataPublication:
        return python_icat.get_with_id(
            session_id=session_id,
            entity_type="DataPublication",
            id_=data_publication_id,
            includes=data_publication_filters.model_dump(),
            client_pool=client_pool,
        )

    return router


def investigation_endpoints(python_icat: PythonICAT, client_pool: ObjectPool) -> APIRouter:
    router = APIRouter(tags=["Investigation"])

    @router.get(
        "/investigations",
        summary="Get Investigations",
        description="Get Investigations and related Entities based on the provided filters.",
        response_model=list[Investigation],
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns Investigations that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_investigations(
        session_id: SessionId,
        investigation_filters: Annotated[InvestigationSearchFilters, Query()],
    ) -> list[Investigation]:
        return python_icat.get_with_filters(
            session_id=session_id,
            entity_type="Investigation",
            filters=investigation_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/investigations/count",
        summary="Count Investigations",
        description="Count Investigations based on the provided filters.",
        response_model=int,
        responses={
            200: {"description": "Success - The number of Investigations that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def count_investigations(
        session_id: SessionId,
        investigation_filters: Annotated[InvestigationCountFilters, Query()],
    ) -> list[Investigation]:
        return python_icat.count_with_filters(
            session_id=session_id,
            entity_type="Investigation",
            filters=investigation_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/investigations/findone",
        summary="Get a single Investigation by name",
        description="Get a single Investigation based on its name",
        response_model=Investigation,
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns the requested Investigation"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def find_one_investigation(
        session_id: SessionId,
        investigation_filters: Annotated[InvestigationFindOneFilters, Query()],
    ) -> Investigation:
        return python_icat.get_one_with_filters(
            session_id=session_id,
            entity_type="Investigation",
            filters=investigation_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/investigations/{investigation_id}",
        summary="Get a single Investigation",
        description="Get a single Investigation and related Entities based on the provided id",
        response_model=Investigation,
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns the requested Investigation"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_investigation(
        session_id: SessionId,
        investigation_id: PositiveInt,
        investigation_filters: Annotated[InvestigationGetFilters, Query()],
    ) -> Investigation:
        return python_icat.get_with_id(
            session_id=session_id,
            entity_type="Investigation",
            id_=investigation_id,
            includes=investigation_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/investigations/{investigation_id}/datasets",
        summary="Get Investigation Datasets",
        description="Get Datasets and related Entities from an Investigation based on the provided filters.",
        response_model=list[Dataset],
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns Datasets that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_investigation_datasets(
        session_id: SessionId,
        investigation_id: PositiveInt,
        dataset_filters: Annotated[DatasetSearchFilters, Query()],
    ) -> list[Dataset]:
        return python_icat.get_with_filters(
            session_id=session_id,
            entity_type="Dataset",
            filters=[
                PythonICATWhereFilter(field="investigation.id", operation="eq", value=investigation_id),
                *dataset_filters.model_dump(),
            ],
            client_pool=client_pool,
        )

    return router


def dataset_endpoints(python_icat: PythonICAT, client_pool: ObjectPool) -> APIRouter:
    router = APIRouter(tags=["Dataset"])

    @router.get(
        "/datasets",
        summary="Get Datasets",
        description="Get Datasets based on the provided filters.",
        response_model=list[Dataset],
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns Datasets that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_datasets(
        session_id: SessionId,
        dataset_filters: Annotated[DatasetSearchFilters, Query()],
    ) -> list[Dataset]:
        return python_icat.get_with_filters(
            session_id=session_id,
            entity_type="Dataset",
            filters=dataset_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/datasets/count",
        summary="Count Datasets",
        description="Count Datasets based on the provided filters.",
        response_model=int,
        responses={
            200: {"description": "Success - The number of Datasets that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def count_datasets(
        session_id: SessionId,
        dataset_filters: Annotated[DatasetCountFilters, Query()],
    ) -> list[Dataset]:
        return python_icat.count_with_filters(
            session_id=session_id,
            entity_type="Dataset",
            filters=dataset_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/datasets/findone",
        summary="Get a single Dataset by name",
        description="Get a single Dataset based on its name",
        response_model=Dataset,
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns the requested Dataset"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def find_one_dataset(
        session_id: SessionId,
        dataset_filters: Annotated[DatasetFindOneFilters, Query()],
    ) -> Investigation:
        return python_icat.get_one_with_filters(
            session_id=session_id,
            entity_type="Dataset",
            filters=dataset_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/datasets/{dataset_id}",
        summary="Get a single Dataset",
        description="Get a single Dataset and related Entities based on the provided id.",
        response_model=Dataset,
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns the requested Dataset"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_dataset(
        session_id: SessionId,
        dataset_id: PositiveInt,
        dataset_filters: Annotated[DatasetGetFilters, Query()],
    ) -> Dataset:
        return python_icat.get_with_id(
            session_id=session_id,
            entity_type="Dataset",
            id_=dataset_id,
            includes=dataset_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/datasets/{dataset_id}/datafiles",
        summary="Get Dataset Datafiles",
        description="Get Datafiles from a Dataset based on the provided filters.",
        response_model=list[Datafile],
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns Datafiles that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_dataset_datafiles(
        session_id: SessionId,
        dataset_id: PositiveInt,
        datafile_filters: Annotated[DatafileSearchFilters, Query()],
    ) -> list[Datafile]:
        return python_icat.get_with_filters(
            session_id=session_id,
            entity_type="Datafile",
            filters=[
                PythonICATWhereFilter(field="dataset.id", operation="eq", value=dataset_id),
                *datafile_filters.model_dump(),
            ],
            client_pool=client_pool,
        )

    return router


def datafile_endpoints(python_icat: PythonICAT, client_pool: ObjectPool) -> APIRouter:
    router = APIRouter(tags=["Datafile"])

    @router.get(
        "/datafiles",
        summary="Get Datafiles",
        description="Get Datafiles based on the provided filters.",
        response_model=list[Datafile],
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns Datafiles that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_datafiles(
        session_id: SessionId,
        datafile_filters: Annotated[DatafileSearchFilters, Query()],
    ) -> list[Datafile]:
        return python_icat.get_with_filters(
            session_id=session_id,
            entity_type="Datafile",
            filters=datafile_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/datafiles/count",
        summary="Count Datafiles",
        description="Count Datafiles based on the provided filters.",
        response_model=int,
        responses={
            200: {"description": "Success - The number of Datafiles that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def count_datafiles(
        session_id: SessionId,
        datafile_filters: Annotated[DatafileCountFilters, Query()],
    ) -> list[Datafile]:
        return python_icat.count_with_filters(
            session_id=session_id,
            entity_type="Datafile",
            filters=datafile_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/datafiles/findone",
        summary="Get a single Datafile by name",
        description="Get a single Datafile based on its name",
        response_model=Datafile,
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns the requested Datafile"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def find_one_datafile(
        session_id: SessionId,
        datafile_filters: Annotated[DatafileFindOneFilters, Query()],
    ) -> Investigation:
        return python_icat.get_one_with_filters(
            session_id=session_id,
            entity_type="Datafile",
            filters=datafile_filters.model_dump(),
            client_pool=client_pool,
        )

    @router.get(
        "/datafiles/{datafile_id}",
        summary="Get a single Datafile",
        description="Get a single Datafile based on the provided id.",
        response_model=Datafile,
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns requested Datafile"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_datafile(
        datafile_id: PositiveInt,
        session_id: SessionId,
    ) -> Datafile:
        return python_icat.get_with_id(
            session_id=session_id,
            entity_type="Datafile",
            id_=datafile_id,
            client_pool=client_pool,
        )

    return router


def investigation_user_endpoints(python_icat: PythonICAT, client_pool: ObjectPool) -> APIRouter:
    router = APIRouter(tags=["InvestigationUser"])

    @router.get(
        "/investigationusers",
        summary="Get InvestigationUsers",
        description="Get InvestigationUsers based on the provided filters.",
        response_model=list[InvestigationUser],
        response_model_exclude_none=True,
        responses={
            200: {"description": "Success - returns InvestigationUsers that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_investigation_users(
        session_id: SessionId,
        investigation_user_filters: Annotated[InvestigationUserSearchFilters, Query()],
    ) -> list[InvestigationUser]:
        return python_icat.get_with_filters(
            session_id=session_id,
            entity_type="InvestigationUser",
            filters=investigation_user_filters.model_dump(),
            client_pool=client_pool,
        )

    return router
