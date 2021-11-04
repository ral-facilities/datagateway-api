import logging

from datagateway_api.common.base_query_filter_factory import QueryFilterFactory
from datagateway_api.common.exceptions import FilterError

log = logging.getLogger()


class SearchAPIQueryFilterFactory(QueryFilterFactory):
    @staticmethod
    def get_query_filter(request_filter):
        query_param_name = list(request_filter)[0].lower()
        query_filters = []

        if query_param_name == "filter":
            log.debug(
                f"Filter: {request_filter['filter']}, Type: {type(request_filter['filter'])})"
            )
            for filter_name, filter_input in request_filter["filter"].items():
                if filter_name == "where":
                    pass
                elif filter_name == "include":
                    pass
                elif filter_name == "limit":
                    pass
                elif filter_name == "skip":
                    pass
                else:
                    raise FilterError(
                        "No valid filter name given within filter query param"
                    )

            return query_filters
        else:
            raise FilterError(f"Bad filter, please check input: {request_filter}")
