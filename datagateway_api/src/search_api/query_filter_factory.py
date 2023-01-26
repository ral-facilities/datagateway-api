import logging


from datagateway_api.src.common.base_query_filter_factory import QueryFilterFactory
from datagateway_api.src.common.exceptions import FilterError, SearchAPIError
from datagateway_api.src.search_api.filters import (
    SearchAPIIncludeFilter,
    SearchAPILimitFilter,
    SearchAPIScoringFilter,
    SearchAPISkipFilter,
    SearchAPIWhereFilter,
)
import datagateway_api.src.search_api.models as search_api_models
from datagateway_api.src.search_api.nested_where_filters import NestedWhereFilters
from datagateway_api.src.search_api.panosc_mappings import mappings
from datagateway_api.src.search_api.query import SearchAPIQuery

log = logging.getLogger()


class SearchAPIQueryFilterFactory(QueryFilterFactory):
    @staticmethod
    def get_query_filter(request_filter, entity_name=None, related_entity_name=None):
        """
        Given a filter, return a list of matching query filter objects

        :param request_filter: The filter from which to create a list of query filter
            objects
        :type request_filter: :class:`dict`
        :param entity_name: Entity name of the endpoint or the name of the included
            entity - this is needed for when there is a text operator inside a where
            filter
        :type entity_name: :class:`str`
        :param related_entity_name: Entity name used when calling `get_where_filter()`
            and `get_include_filter()`
        :type related_entity_name: :class:`str`
        :return: The list of query filter objects created
        :raises FilterError: If the filter name is not recognised
        """
        query_param_name = list(request_filter)[0].lower()
        query_filters = []

        if query_param_name == "filter":
            log.debug("Filter: %s", request_filter["filter"])
            for filter_name, filter_input in request_filter["filter"].items():
                if filter_name == "where":
                    log.info("where JSON object found")
                    query_filters.extend(
                        SearchAPIQueryFilterFactory.get_where_filter(
                            filter_input, entity_name, related_entity_name,
                        ),
                    )
                elif filter_name == "include":
                    log.info("include JSON object found")
                    query_filters.extend(
                        SearchAPIQueryFilterFactory.get_include_filter(
                            filter_input, entity_name, related_entity_name,
                        ),
                    )
                elif filter_name == "limit":
                    log.info("limit JSON object found")
                    query_filters.append(SearchAPILimitFilter(filter_input))
                elif filter_name == "skip":
                    log.info("skip JSON object found")
                    query_filters.append(SearchAPISkipFilter(filter_input))
                elif filter_name == "query":
                    log.info("query JSON object found")
                    query_filters.append(SearchAPIScoringFilter(filter_input))
                else:
                    raise FilterError(
                        "No valid filter name given within filter query param:"
                        f" {filter_name}",
                    )
        elif query_param_name == "where":
            # For the count endpoints
            log.info("where query param found, likely for count endpoint")
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
    def get_where_filter(where_filter_input, entity_name, related_entity_name=None):
        """
        Given a where filter input, return a list of `NestedWhereFilters` and/ or
        `SearchAPIWhereFilter` objects

        `NestedWhereFilters` objects are created when there is an AND or OR inside the
        where filter input, otherwise `SearchAPIWhereFilter` objects are created. If
        there is a text operator inside the where filter input then the number of
        `SearchAPIWhereFilter` objects that will be created depends on the number of
        text operator fields that will be matched for the provided entity.

        :param where_filter_input: The filter from which to create a list of
            `NestedWhereFilters` and/ or `SearchAPIWhereFilter` objects
        :type where_filter_input: :class:`dict`
        :param entity_name: Entity name of the endpoint or the name of the included
            entity - this is needed for when there is a text operator inside a where
            filter so that the value provided can be matched with the relevant text
            operator fields for the entity.
        :type entity_name: :class:`str`
        :param related_entity_name: Entity name of a related entity, used for getting
            text operator fields for said related entity
        :type related_entity_name: :class:`str`
        :return: The list of `NestedWhereFilters` and/ or `SearchAPIWhereFilter` objects
            created
        :raises SearchAPIError: If there are no text operator fields on the entity
        """

        where_filters = []
        if (
            list(where_filter_input.keys())[0] == "and"
            or list(where_filter_input.keys())[0] == "or"
        ):
            log.debug("and/or operators found: %s", list(where_filter_input.keys())[0])
            boolean_operator = list(where_filter_input.keys())[0]
            conditions = list(where_filter_input.values())[0]
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
                SearchAPIQuery(entity_name),
            )
            where_filters.append(nested)
        elif list(where_filter_input.keys())[0] == "text":
            log.debug("Text operator found within JSON where object")
            try:
                # If there's a related entity name, fetch the text operator fields for
                # that entity. This serves in use cases where there's a WHERE filter
                # with a text operator on an included/related entity
                entity_class_name = (
                    related_entity_name if related_entity_name else entity_name
                )
                entity_class = getattr(search_api_models, entity_class_name)
            except AttributeError as e:
                raise SearchAPIError(
                    f"No text operator fields have been defined for {entity_class_name}"
                    f", {e.args}",
                )

            or_conditional_filters = []
            field_names = entity_class._text_operator_fields
            log.debug(
                "Text operators found for PaNOSC %s: %s", entity_name, field_names,
            )
            if not field_names:
                # No text operator fields present, simply log and move on, we should
                # ignore text operator queries on entities where `_text_operator_fields`
                # is empty (meaning they are not present in the origina PaNOSC data
                # model)
                log.info(
                    "No text operator fields found for PaNOSC entity %s, will"
                    " ignore",
                    entity_name,
                )
            else:
                for field_name in field_names:
                    or_conditional_filters.append(
                        {field_name: {"like": where_filter_input["text"]}},
                    )

                where_filter = {
                    "filter": {"where": {"or": or_conditional_filters}},
                }
                where_filters.extend(
                    SearchAPIQueryFilterFactory.get_query_filter(
                        where_filter, entity_name,
                    ),
                )
        else:
            log.info("Basic where filter found, extracting field, value and operation")
            field, value, operation = SearchAPIQueryFilterFactory.get_condition_values(
                where_filter_input,
            )

            # Ignore filters on `isPublic`` fields as data is always public. Ensure that
            # empty list is returned when filtering for non-public data.
            if field == "isPublic":
                value = not value if operation == "neq" else value
                if not value:
                    where_filters.append(SearchAPISkipFilter(1))
                    where_filters.append(SearchAPILimitFilter(0))
            else:
                where_filters.append(SearchAPIWhereFilter(field, value, operation))

        return where_filters

    @staticmethod
    def get_include_filter(include_filter_input, entity_name, related_entity_name=None):
        """
        Given an include filter input, return a list of `SearchAPIIncludeFilter` and any
        `NestedWhereFilters` and/ or `SearchAPIWhereFilter` objects if there is a scope
        filter inside the filter input

        Currently, we do not support limit and skip filters inside scope filters that
        are part of include filters.

        :param include_filter_input: The filter from which to create a list of
            `SearchAPIIncludeFilter` and any `NestedWhereFilters` and/or
            `SearchAPIWhereFilter` objects
        :type include_filter_input: :class:`list`
        :param entity_name: Entity name of the endpoint or the name of the included
            entity - this is needed for when there is a text operator inside a where
            filter so that the value provided can be matched with the relevant text
            operator fields for the entity.
        :type entity_name: :class:`str`
        :param related_entity_name: Entity name of a related entity
        :type related_entity_name: :class:`str`
        :return: The list of `SearchAPIIncludeFilter` and any `NestedWhereFilters` and/
            or `SearchAPIWhereFilter` objects created
        :raises FilterError: If scope filter has a limit or skip filter
        """

        query_filters = []
        included_entities = []

        for related_model in include_filter_input:
            log.debug("Related model: %s", related_model)
            nested_include = False
            included_entity = related_model["relation"]
            # List of included entities made so they can put into a single include
            # filter instead of having a new filter object for each related entity
            included_entities.append(related_model["relation"])

            if "scope" in related_model:
                log.info("Scope found in include JSON object")
                if "limit" in related_model["scope"]:
                    raise FilterError(
                        "Bad Include filter: Scope filter cannot have a limit filter",
                    )
                if "skip" in related_model["scope"]:
                    raise FilterError(
                        "Bad Include filter: Scope filter cannot have a skip filter",
                    )

                try:
                    entity_class_name = (
                        related_entity_name if related_entity_name else entity_name
                    )
                    # Get related field name in entity name format for recursive call
                    related_entity_name = mappings.get_panosc_related_entity_name(
                        entity_class_name, included_entity,
                    )
                except SearchAPIError as e:
                    # If the function call errors, it's a client issue at this point
                    raise FilterError(e)
                scope_query_filters = SearchAPIQueryFilterFactory.get_query_filter(
                    {"filter": related_model["scope"]},
                    entity_name,
                    related_entity_name,
                )

                for scope_query_filter in scope_query_filters:
                    if isinstance(
                        scope_query_filter, (NestedWhereFilters, SearchAPIWhereFilter),
                    ):
                        SearchAPIQueryFilterFactory.prefix_where_filter_field_with_entity_name(  # noqa: B950
                            scope_query_filter, included_entity,
                        )
                    if isinstance(scope_query_filter, SearchAPIIncludeFilter):
                        for i, included_filter in enumerate(
                            scope_query_filter.included_filters,
                        ):
                            nested_include = True
                            scope_query_filter.panosc_entity_name = entity_name
                            scope_query_filter.included_filters[
                                i
                            ] = f"{included_entity}.{included_filter}"

                query_filters.extend(scope_query_filters)
                # Flush related entity name so a bug doesn't occur with multiple related
                # models
                related_entity_name = None

        if not nested_include:
            query_filters.append(
                SearchAPIIncludeFilter(included_entities, entity_name),
            )

        return query_filters

    @staticmethod
    def get_condition_values(conditions_dict):
        """
        Given a simplified where filter input, return a field name, value and operation
        as a tuple

        :param conditions_dict: The filter from which to return a field name, value and
            operation
        :type conditions_dict: :class:`dict`
        :return: The tuple that includes field name, value and operation
        """
        field = list(conditions_dict.keys())[0]
        filter_data = list(conditions_dict.values())[0]

        if isinstance(filter_data, (bool, int, str)):
            # Format: {"where": {"property": "value"}}
            log.debug("Format of WHERE filter: {'where': {'property': 'value'}}")
            value = conditions_dict[field]
            operation = "eq"
        elif isinstance(filter_data, dict):
            # Format: {"where": {"property": {"operator": "value"}}}
            log.debug(
                "Format of WHERE filter:"
                " {'where': {'property': {'operator': 'value'}}}",
            )
            value = list(conditions_dict[field].values())[0]
            operation = list(conditions_dict[field].keys())[0]

            if isinstance(value, bool) and operation not in ["eq", "neq"]:
                raise FilterError(
                    "Bad Where filter: Invalid operator used with boolean value",
                )

        return field, value, operation

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
