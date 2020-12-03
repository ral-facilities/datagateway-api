import logging

from datagateway_api.common.config import config
from datagateway_api.common.exceptions import (
    ApiError,
    FilterError,
)

log = logging.getLogger()


class QueryFilterFactory(object):
    @staticmethod
    def get_query_filter(request_filter):
        """
        Given a filter return a matching Query filter object

        This factory is not in common.filters so the created filter can be for the
        correct backend. Moving the factory into that file would mean the filters would
        be based off the abstract classes (because they're in the same file) which won't
        enable filters to be unique to the backend

        :param request_filter: dict - The filter to create the QueryFilter for
        :return: The QueryFilter object created
        """

        backend_type = config.get_backend_type()
        if backend_type == "db":
            from datagateway_api.common.database.filters import (
                DatabaseDistinctFieldFilter as DistinctFieldFilter,
                DatabaseIncludeFilter as IncludeFilter,
                DatabaseLimitFilter as LimitFilter,
                DatabaseOrderFilter as OrderFilter,
                DatabaseSkipFilter as SkipFilter,
                DatabaseWhereFilter as WhereFilter,
            )
        elif backend_type == "python_icat":
            from datagateway_api.common.icat.filters import (
                PythonICATDistinctFieldFilter as DistinctFieldFilter,
                PythonICATIncludeFilter as IncludeFilter,
                PythonICATLimitFilter as LimitFilter,
                PythonICATOrderFilter as OrderFilter,
                PythonICATSkipFilter as SkipFilter,
                PythonICATWhereFilter as WhereFilter,
            )
        else:
            raise ApiError(
                "Cannot select which implementation of filters to import, check the"
                " config file has a valid backend type",
            )

        filter_name = list(request_filter)[0].lower()
        if filter_name == "where":
            field = list(request_filter[filter_name].keys())[0]
            operation = list(request_filter[filter_name][field].keys())[0]
            value = request_filter[filter_name][field][operation]
            return WhereFilter(field, value, operation)
        elif filter_name == "order":
            field = request_filter["order"].split(" ")[0]
            direction = request_filter["order"].split(" ")[1]
            return OrderFilter(field, direction)
        elif filter_name == "skip":
            return SkipFilter(request_filter["skip"])
        elif filter_name == "limit":
            return LimitFilter(request_filter["limit"])
        elif filter_name == "include":
            return IncludeFilter(request_filter["include"])
        elif filter_name == "distinct":
            return DistinctFieldFilter(request_filter["distinct"])
        else:
            raise FilterError(f" Bad filter: {request_filter}")
