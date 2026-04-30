import logging

from datagateway_api.src.common.base_query_filter_factory import QueryFilterFactory
from datagateway_api.src.common.exceptions import FilterError
from datagateway_api.src.datagateway_api.icat.filters import (
    PythonICATDistinctFieldFilter as DistinctFieldFilter,
    PythonICATIncludeFilter as IncludeFilter,
    PythonICATLimitFilter as LimitFilter,
    PythonICATOrderFilter as OrderFilter,
    PythonICATSkipFilter as SkipFilter,
    PythonICATWhereFilter as WhereFilter,
)

log = logging.getLogger()


class DataGatewayAPIQueryFilterFactory(QueryFilterFactory):
    @staticmethod
    def get_query_filter(request_filter, entity_name=None):
        """
        Given a filter, return a matching Query filter object

        :param request_filter: The filter to create the QueryFilter for
        :type request_filter: :class:`dict`
        :param entity_name: Not utilised in DataGateway API implementation of this
            static function, used in the search API. It is part of the method signature
            as the same function call (called in `get_filters_from_query_string()`) is
            used for both implementations
        :type entity_name: :class:`str`
        :return: The QueryFilter object created
        :raises FilterError: If the filter name is not recognised
        """

        filter_name = list(request_filter)[0].lower()
        if filter_name == "where":
            field = list(request_filter[filter_name].keys())[0]
            operation = list(request_filter[filter_name][field].keys())[0]
            value = request_filter[filter_name][field][operation]
            return [WhereFilter(field, value, operation)]
        elif filter_name == "order":
            field = request_filter["order"].split(" ")[0]
            direction = request_filter["order"].split(" ")[1]
            return [OrderFilter(field, direction)]
        elif filter_name == "skip":
            return [SkipFilter(request_filter["skip"])]
        elif filter_name == "limit":
            return [LimitFilter(request_filter["limit"])]
        elif filter_name == "include":
            return [IncludeFilter(request_filter["include"])]
        elif filter_name == "distinct":
            return [DistinctFieldFilter(request_filter["distinct"])]
        else:
            raise FilterError(f" Bad filter: {request_filter}")
