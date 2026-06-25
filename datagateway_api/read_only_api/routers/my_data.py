from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from object_pool import ObjectPool

from datagateway_api.datagateway_api.icat.python_icat import PythonICAT
from datagateway_api.read_only_api.models.investigation import Investigation


security = HTTPBearer()


def my_data_endpoints(python_icat: PythonICAT, icat_client_pool: ObjectPool) -> APIRouter:
    router = APIRouter(prefix="/my_data", tags="My data")

    @router.get(
        "/investigations",
        summary="Get investigations",
        description="Get investigations",
        response_model=list[Investigation],
        responses={
            200: {"description": f"Success - returns Investigations that satisfy the filters"},
            400: {"description": "Bad request - Something was wrong with the request"},
            401: {"description": "Unauthorized - No session ID found in HTTP Auth. header"},
            403: {"description": "Forbidden - The session ID provided is invalid"},
            404: {"description": "No such record - Unable to find a record in ICAT"},
        },
    )
    def get_investigations(credentials: HTTPAuthorizationCredentials = Depends(security)):
        return python_icat.get_with_filters(
            session_id=credentials.credentials,
            entity_type="Investigaton",
            filters=[],
            icat_client_pool=icat_client_pool,
        )

    return router
