from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials
from object_pool import ObjectPool
from pydantic import PositiveInt

from datagateway_api.auth.session_bearer import SessionBearer
from datagateway_api.datagateway_api.icat.filters import PythonICATWhereFilter
from datagateway_api.datagateway_api.icat.python_icat import PythonICAT
from datagateway_api.read_only_api.models import (
    DatafileFilters,
    DatasetFilters,
    DatasetIncludeEnum,
    InvestigationFilters,
    InvestigationIncludeEnum,
    Datafile,
    Dataset,
    Investigation,
)
from datagateway_api.read_only_api.models.request.dataset import DATASET_INCLUDE_DESCRIPTION
from datagateway_api.read_only_api.models.request.investigation import INVESTIGATION_INCLUDE_DESCRIPTION

SessionId = Annotated[HTTPAuthorizationCredentials, Depends(SessionBearer())]


def my_data_endpoints(python_icat: PythonICAT, client_pool: ObjectPool) -> APIRouter:
    router = APIRouter(tags=["Entities"])

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
        investigation_filters: Annotated[InvestigationFilters, Query()],
    ) -> list[Investigation]:
        return python_icat.get_with_filters(
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
        include: Annotated[
            list[InvestigationIncludeEnum],
            Query(description=INVESTIGATION_INCLUDE_DESCRIPTION),
        ] = [],  # noqa: B006
    ) -> Investigation:
        return python_icat.get_with_id(
            session_id=session_id,
            entity_type="Investigation",
            id_=investigation_id,
            includes=[i.value for i in include],
            client_pool=client_pool,
        )

    @router.get(
        "/investigations/{investigation_id}/datasets",
        summary="Get Datasets",
        description="Get Datasets and related Entities based on the provided filters.",
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
        investigation_id: PositiveInt,
        dataset_filters: Annotated[DatasetFilters, Query()],
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

    @router.get(
        "/investigations/{investigation_id}/datasets/{dataset_id}",
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
        investigation_id: PositiveInt,
        dataset_id: PositiveInt,
        include: Annotated[list[DatasetIncludeEnum], Query(description=DATASET_INCLUDE_DESCRIPTION)] = [],  # noqa: B006
    ) -> Dataset:
        return python_icat.get_with_id(
            session_id=session_id,
            entity_type="Dataset",
            id_=dataset_id,
            includes=[i.value for i in include],
            client_pool=client_pool,
        )

    @router.get(
        "/investigations/{investigation_id}/datasets/{dataset_id}/datafiles",
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
        investigation_id: PositiveInt,
        dataset_id: PositiveInt,
        datafile_filters: Annotated[DatafileFilters, Query()],
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

    @router.get(
        "/investigations/{investigation_id}/datasets/{dataset_id}/datafiles/{datafile_id}",
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
        investigation_id: PositiveInt,
        dataset_id: PositiveInt,
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
