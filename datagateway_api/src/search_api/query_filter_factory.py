import logging

from datagateway_api.src.common.base_query_filter_factory import QueryFilterFactory
from datagateway_api.src.common.exceptions import FilterError
from datagateway_api.src.search_api.filters import (
    SearchAPIIncludeFilter,
    SearchAPILimitFilter,
    SearchAPISkipFilter,
    SearchAPIWhereFilter,
)

log = logging.getLogger()


class SearchAPIQueryFilterFactory(QueryFilterFactory):
    @staticmethod
    def get_query_filter(request_filter, entity_name=None):
        query_param_name = list(request_filter)[0].lower()
        query_filters = []

        if query_param_name == "filter":
            log.debug("Filter: %s", request_filter["filter"])
            for filter_name, filter_input in request_filter["filter"].items():
                if filter_name == "where":
                    query_filters.extend(
                        SearchAPIQueryFilterFactory.get_where_filter(
                            filter_input, entity_name,
                        ),
                    )
                elif filter_name == "include":
                    query_filters.extend(
                        SearchAPIQueryFilterFactory.get_include_filter(filter_input),
                    )
                elif filter_name == "limit":
                    query_filters.append(SearchAPILimitFilter(filter_input))
                elif filter_name == "skip":
                    query_filters.append(SearchAPISkipFilter(filter_input))
                else:
                    raise FilterError(
                        "No valid filter name given within filter query param",
                    )
        elif query_param_name == "where":
            # For the count endpoints
            query_filters.extend(
                SearchAPIQueryFilterFactory.get_query_filter(
                    {"filter": request_filter}, entity_name,
                ),
            )
        else:
            raise FilterError(
                f"Bad filter, please check query parameters: {request_filter}",
            )

        return query_filters

    @staticmethod
    def get_where_filter(filter_input, entity_name):
        where_filters = []
        if (
            list(filter_input.keys())[0] == "and"
            or list(filter_input.keys())[0] == "or"
        ):
            boolean_operator = list(filter_input.keys())[0]
            conditions = list(filter_input.values())[0]
            for condition in conditions:
                # Could be nested AND/OR
                where_filter = {
                    "filter": {"where": condition},
                }
                conditional_where_filters = SearchAPIQueryFilterFactory.get_query_filter(
                    where_filter, entity_name,
                )

                for conditional_where_filter in conditional_where_filters:
                    conditional_where_filter.boolean_operator = boolean_operator
                where_filters.extend(conditional_where_filters)
        elif list(filter_input.keys())[0] == "text":
            # TODO - we might want to move this to the data
            # definitions at a later point
            text_operator_fields = {
                "datasets": ["title"],
                "documents": ["title", "summary"],
                "files": ["name"],
                "instrument": ["name", "facility"],
                "samples": ["name", "description"],
                "techniques": ["name"],
            }

            try:
                field_names = text_operator_fields[entity_name]
                for field_name in field_names:
                    where_filter = {
                        "filter": {"where": {field_name: filter_input["text"]}},
                    }
                    where_filters.extend(
                        SearchAPIQueryFilterFactory.get_query_filter(
                            where_filter, entity_name,
                        ),
                    )
            except KeyError:
                # Do not raise FilterError nor attempt to create filters. Simply
                # ignore text operator queries on fields that are not part of the
                # text_operator_fields dict.
                pass
        else:
            filter_data = SearchAPIQueryFilterFactory.get_condition_values(
                filter_input,
            )
            for condition in filter_data:
                where_filters.append(
                    SearchAPIWhereFilter(
                        field=condition[0], value=condition[1], operation=condition[2],
                    ),
                )
        return where_filters

    @staticmethod
    def get_include_filter(filter_input):
        query_filters = []
        for related_model in filter_input:
            included_entity = related_model["relation"]
            query_filters.append(SearchAPIIncludeFilter(included_entity))

            if "scope" in related_model:
                # Scope filter can have WHERE, INCLUDE, LIMIT and SKIP filters
                scope_query_filters = SearchAPIQueryFilterFactory.get_query_filter(
                    {"filter": related_model["scope"]}, included_entity,
                )

                for scope_query_filter in scope_query_filters:
                    if isinstance(scope_query_filter, SearchAPIWhereFilter):
                        scope_query_filter.field = (
                            f"{included_entity}.{scope_query_filter.field}"
                        )
                query_filters.extend(scope_query_filters)

        return query_filters

    @staticmethod
    def get_condition_values(filter_input):
        where_filter_data = []
        field = list(filter_input.keys())[0]
        filter_data = list(filter_input.values())[0]

        if isinstance(filter_data, str):
            # Format: {"where": {"property": "value"}}
            value = filter_input[field]
            operation = "eq"
        elif isinstance(filter_data, dict):
            # Format: {"where": {"property": {"operator": "value"}}}
            value = list(filter_input[field].values())[0]
            operation = list(filter_input[field].keys())[0]

        where_filter_data.append((field, value, operation))

        return where_filter_data
