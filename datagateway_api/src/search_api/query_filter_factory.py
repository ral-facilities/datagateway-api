import logging

from datagateway_api.src.common.base_query_filter_factory import QueryFilterFactory
from datagateway_api.src.common.exceptions import FilterError
from datagateway_api.src.search_api.filters import (
    SearchAPIIncludeFilter,
    SearchAPILimitFilter,
    SearchAPISkipFilter,
    SearchAPIWhereFilter,
)
from datagateway_api.src.search_api.nested_where_filters import NestedWhereFilters

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
            conditional_where_filters = []

            for condition in conditions:
                # Could be nested AND/OR
                where_filter = {
                    "filter": {"where": condition},
                }
                conditional_where_filters.extend(
                    SearchAPIQueryFilterFactory.get_query_filter(
                        where_filter, entity_name,
                    ),
                )

            nested = NestedWhereFilters(
                conditional_where_filters[:-1],
                conditional_where_filters[-1],
                boolean_operator,
            )
            where_filters.append(nested)
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
                or_conditional_filters = []
                field_names = text_operator_fields[entity_name]
                for field_name in field_names:
                    or_conditional_filters.append(
                        {field_name: {"like": filter_input["text"]}},
                    )

                where_filter = {
                    "filter": {"where": {"or": or_conditional_filters}},
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

            nested_include = False
            if "scope" in related_model:
                if "limit" in related_model["scope"]:
                    raise FilterError(
                        "Bad Include filter: Scope filter cannot have a limit filter",
                    )
                if "skip" in related_model["scope"]:
                    raise FilterError(
                        "Bad Include filter: Scope filter cannot have a skip filter",
                    )

                # Scope filter can have WHERE and/ or INCLUDE filters
                scope_query_filters = SearchAPIQueryFilterFactory.get_query_filter(
                    {"filter": related_model["scope"]}, included_entity,
                )

                for scope_query_filter in scope_query_filters:
                    if isinstance(
                        scope_query_filter, (NestedWhereFilters, SearchAPIWhereFilter),
                    ):
                        SearchAPIQueryFilterFactory.prefix_where_filter_field_with_entity_name(  # noqa: B950
                            scope_query_filter, included_entity,
                        )
                    if isinstance(scope_query_filter, SearchAPIIncludeFilter):
                        nested_include = True
                        included_filter = scope_query_filter.included_filters[0]

                        scope_query_filter.included_filters[
                            0
                        ] = f"{included_entity}.{included_filter}"

                query_filters.extend(scope_query_filters)

            if not nested_include:
                query_filters.append(SearchAPIIncludeFilter(included_entity))

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

    @staticmethod
    def prefix_where_filter_field_with_entity_name(where_filters, entity_name):
        """
        Given a `NestedWhereFilters` or `SearchAPIWhereFilter` object, or a list of
        these objects, prefix the field attribute of the `SearchAPIWhereFilter` object
        with the provided entity name

        When dealing with `NestedWhereFilters`, this function is called recursively in
        order to drill down and get hold of the `SearchAPIWhereFilter` objects so that
        their field attributes can be prefixed. The field attributes of are prefixed
        only if the where filters are part of a scope filter that is inside an include
        filter. This is done to make it clear that the where filter is related to the
        included entity rather than the endpoint entity.

        :param where_filters: The filter(s) whose field attribute(s) require(s)
            prefixing
        :type where_filters: :class:`NestedWhereFilters` or `SearchAPIWhereFilter`, or a
            :class:`list` of :class:`NestedWhereFilters` and/ or `SearchAPIWhereFilter`
        :param entity_name: The name of the included entity to prefix the where filter
            field with
        :type entity_name: :class:`str`
        """
        if not isinstance(where_filters, list):
            where_filters = [where_filters]

        for where_filter in where_filters:
            if isinstance(where_filter, NestedWhereFilters):
                nested_where_filters = where_filter.lhs + where_filter.rhs
                for nested_where_filter in nested_where_filters:
                    SearchAPIQueryFilterFactory.prefix_where_filter_field_with_entity_name(  # noqa: B950
                        nested_where_filter, entity_name,
                    )
            if isinstance(where_filter, SearchAPIWhereFilter):
                where_filter.field = f"{entity_name}.{where_filter.field}"
