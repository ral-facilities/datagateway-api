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
    def get_query_filter(request_filter):
        query_param_name = list(request_filter)[0].lower()
        query_filters = []

        if query_param_name == "filter":
            log.debug("Filter: %s", request_filter["filter"])
            for filter_name, filter_input in request_filter["filter"].items():
                # {"where": {"property": "value"}}
                # {"where": {"property": {"operator": "value"}}}
                # {"where": {"text": "value"}}
                # {"where": {"and": [{"property": "value"}, {"property": "value"}]}}
                # {"where": {"or": [{"property": "value"}, {"property": "value"}]}}
                if filter_name == "where":
                    if (
                        list(filter_input.keys())[0] == "and"
                        or list(filter_input.keys())[0] == "or"
                    ):
                        boolean_operator = list(filter_input.keys())[0]
                        conditions = list(filter_input.values())[0]
                        for condition in conditions:
                            # Could be nested AND/OR
                            filter_data = SearchAPIQueryFilterFactory.get_condition_values(  # noqa: B950
                                condition,
                            )
                            for condition in filter_data:
                                query_filters.append(
                                    SearchAPIWhereFilter(
                                        field=condition[0],
                                        value=condition[1],
                                        operation=condition[2],
                                        boolean_operator=boolean_operator,
                                    ),
                                )
                    else:
                        filter_data = SearchAPIQueryFilterFactory.get_condition_values(
                            filter_input,
                        )
                        for condition in filter_data:
                            query_filters.append(
                                SearchAPIWhereFilter(
                                    field=condition[0],
                                    value=condition[1],
                                    operation=condition[2],
                                ),
                            )

                elif filter_name == "include":
                    # {"include": [{"relation": "relatedModel"}]}
                    #
                    # {"include": [{"relation": "relatedModel1"},
                    # {"relation": "relatedModel2"}]}
                    #
                    # {"include": [{"relation": "relatedModel",
                    # "scope": {"where": {"property": "value"}}}]}

                    for related_model in filter_input:
                        included_entity = related_model["relation"]
                        query_filters.append(SearchAPIIncludeFilter(included_entity))

                        if "scope" in related_model:
                            try:
                                where_key = list(
                                    related_model["scope"]["where"].keys(),
                                )[0]

                                if where_key == "text":
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
                                    field_names = text_operator_fields[included_entity]
                                else:
                                    field_names = [where_key]

                                for field_name in field_names:
                                    full_field_path = f"{included_entity}.{field_name}"
                                    where_filter = {
                                        "filter": {
                                            "where": {
                                                full_field_path: related_model["scope"][
                                                    "where"
                                                ][where_key],
                                            },
                                        },
                                    }
                                    query_filters.extend(
                                        SearchAPIQueryFilterFactory.get_query_filter(
                                            where_filter,
                                        ),
                                    )
                            except KeyError:
                                raise FilterError("Error in scope for include filter")
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
                    {"filter": request_filter},
                ),
            )
        else:
            raise FilterError(
                f"Bad filter, please check query parameters: {request_filter}",
            )

        return query_filters

    @staticmethod
    def get_condition_values(filter_input):
        where_filter_data = []
        field = list(filter_input.keys())[0]
        filter_data = list(filter_input.values())[0]

        if isinstance(filter_data, str):
            # {"where": {"property": "value"}}
            value = filter_input[field]
            operation = "eq"
        elif isinstance(filter_data, dict):
            # {"where": {"property": {"operator": "value"}}}
            print(f"filter data: {filter_data}")
            value = list(filter_input[field].values())[0]
            operation = list(filter_input[field].keys())[0]

        where_filter_data.append((field, value, operation))

        return where_filter_data
