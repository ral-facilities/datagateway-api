import logging

from datagateway_api.src.common.config import config
from datagateway_api.src.common.exceptions import (
    ApiError,
    FilterError,
)

log = logging.getLogger()


class QueryFilterFactory(object):
    @staticmethod
    def get_query_filter(request_filter):
        """
        Given a filter, return a matching Query filter object

        The filters are imported inside this method to enable the unit tests to not rely
        on the contents of `config.json`. If they're imported at the top of the file,
        the backend type won't have been updated if the Flask app has been created from
        an automated test (file imports occur before `create_api_endpoints()` executes).

        :param request_filter: The filter to create the QueryFilter for
        :type request_filter: :class:`dict`
        :return: The QueryFilter object created
        :raises ApiError: If the backend type contains an invalid value
        :raises FilterError: If the filter name is not recognised
        """

        backend_type = config.datagateway_api.backend
        if backend_type == "db":
            from datagateway_api.src.datagateway_api.database.filters import (
                DatabaseDistinctFieldFilter as DistinctFieldFilter,
                DatabaseIncludeFilter as IncludeFilter,
                DatabaseLimitFilter as LimitFilter,
                DatabaseOrderFilter as OrderFilter,
                DatabaseSkipFilter as SkipFilter,
                DatabaseWhereFilter as WhereFilter,
            )
        elif backend_type == "python_icat":
            from datagateway_api.src.datagateway_api.icat.filters import (
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
