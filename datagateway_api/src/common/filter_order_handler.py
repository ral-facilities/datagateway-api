import logging

from datagateway_api.src.common.config import Config
from datagateway_api.src.datagateway_api.icat.filters import (
    PythonICATIncludeFilter,
    PythonICATLimitFilter,
    PythonICATOrderFilter,
    PythonICATSkipFilter,
)

if Config.config.search_api:
    from datagateway_api.src.search_api.filters import SearchAPIIncludeFilter
    from datagateway_api.src.search_api.panosc_mappings import mappings
    from datagateway_api.src.search_api.query import SearchAPIQuery


log = logging.getLogger()


class FilterOrderHandler(object):
    """
    The FilterOrderHandler takes in filters, sorts them according to the order of
    operations, then applies them.
    """

    def __init__(self):
        self.filters = []

    def add_filter(self, query_filter):
        self.filters.append(query_filter)

    def add_filters(self, query_filter):
        self.filters.extend(query_filter)

    def remove_filter(self, query_filter):
        self.filters.remove(query_filter)

    def sort_filters(self):
        """
        Sorts the filters according to the order of operations
        """
        self.filters.sort(key=lambda x: x.precedence)

    def apply_filters(self, query):
        """
        Given a query apply the filters the handler has in the correct order.

        :param query: The query to have filters applied to
        """
        self.sort_filters()

        for query_filter in self.filters:
            # Using `type()` because we only want the Python ICAT version, don't want
            # the code to catch objects that inherit from the class e.g.
            # `SearchAPIIncludeFilter`
            if type(query_filter) is PythonICATIncludeFilter and isinstance(
                query, SearchAPIQuery,
            ):
                query = query.icat_query.query
            query_filter.apply_filter(query)

    def add_icat_relations_for_non_related_fields_of_panosc_related_entities(
        self, panosc_entity_name,
    ):
        """
        When there are Search API included filters, get the ICAT relations (if any) for
        the non-related fields of all the entities in the relations. Once retrieved,
        add them to the `included_filters` list of a `PythonICATIncludeFilter` object
        that may already exist in `self.filters`. If such filter does not exist in
        `self.filters` then create a new `PythonICATIncludeFilter` object, passing the
        ICAT relations to it. Doing this will ensure that ICAT related entities that
        map to non-related PaNOSC fields are included in the call made to ICAT.

        A `PythonICATIncludeFilter` object can exist in `self.filters` when one is
        created and added in the `get_search` method. This is done when the the PaNOSC
        entity for which search is been retrieved has non-related fields that have
        ICAT relations. For example, the Document entity has non-related fields that
        map to the `keywords` and `type` ICAT entities that are related to the
        `investigation` entity.

        :param panosc_entity_name: A PaNOSC entity name e.g. "Dataset"
        :type panosc_entity_name: :class:`str`
        """

        python_icat_include_filter = None
        icat_relations = []
        for filter_ in self.filters:
            if type(filter_) == PythonICATIncludeFilter:
                # Using `type` as `isinstance` would return `True` for any class that
                # inherits `PythonICATIncludeFilter` e.g. `SearchAPIIncludeFilter`.`
                python_icat_include_filter = filter_
            elif isinstance(filter_, SearchAPIIncludeFilter):
                included_filters = filter_.included_filters
                for included_filter in included_filters:
                    icat_relations.extend(
                        mappings.get_icat_relations_for_non_related_fields_of_panosc_relation(  # noqa: B950
                            panosc_entity_name, included_filter,
                        ),
                    )

        if icat_relations:
            log.info(
                "Including ICAT relations of non-related fields of related PaNOSC "
                "entities",
            )
            # Remove any duplicate ICAT relations
            icat_relations = list(dict.fromkeys(icat_relations))
            if python_icat_include_filter:
                python_icat_include_filter.included_filters.extend(icat_relations)
            else:
                python_icat_include_filter = PythonICATIncludeFilter(icat_relations)
                self.filters.append(python_icat_include_filter)

    def add_icat_relations_for_panosc_non_related_fields(
        self, panosc_entity_name,
    ):
        """
        Retrieve ICAT relations and create a `PythonICATIncludeFilter` for these ICAT
        relations

        :param panosc_entity_name: A PaNOSC entity name e.g. "Dataset"
        :type panosc_entity_name: :class:`str`
        """

        icat_relations = mappings.get_icat_relations_for_panosc_non_related_fields(
            panosc_entity_name,
        )

        # Remove any duplicate ICAT relations
        icat_relations = list(dict.fromkeys(icat_relations))
        if icat_relations:
            self.filters.append(PythonICATIncludeFilter(icat_relations))

    def merge_python_icat_limit_skip_filters(self):
        """
        When there are both limit and skip filters in a request, merge them into the
        limit filter and remove the skip filter from the instance
        """
        log.info("Merging a PythonICATSkipFilter and PythonICATLimitFilter together")
        skip_filter = None
        limit_filter = None

        for icat_filter in self.filters:
            if isinstance(icat_filter, PythonICATSkipFilter):
                skip_filter = icat_filter

            if isinstance(icat_filter, PythonICATLimitFilter):
                limit_filter = icat_filter

        if skip_filter and limit_filter:
            log.info("Merging skip filter with limit filter")
            limit_filter.skip_value = skip_filter.skip_value
            log.info("Removing skip filter from list of filters")
            self.remove_filter(skip_filter)
            log.debug("Filters: %s", self.filters)

    def clear_python_icat_order_filters(self):
        """
        Checks if any order filters have been added to the request and resets the
        variable used to manage which attribute(s) to use for sorting results.

        A reset is required because Python ICAT overwrites (as opposed to appending to
        it) the query's order list every time one is added to the query.
        """
        log.debug("Resetting result order for the order filter")

        if any(
            isinstance(icat_filter, PythonICATOrderFilter)
            for icat_filter in self.filters
        ):
            PythonICATOrderFilter.result_order = []
            PythonICATOrderFilter.join_specs = {}

    def manage_icat_filters(self, filters, query):
        """
        Utility function to call other functions in this class, used to manage filters
        when using the Python ICAT backend. These steps are the same with the different
        types of requests that utilise filters, therefore this function helps to reduce
        code duplication

        :param filters: The list of filters that will be applied to the query
        :type filters: List of specific implementations :class:`QueryFilter`
        :param query: ICAT query which will fetch the data at a later stage
        :type query: :class:`icat.query.Query`
        """

        self.add_filters(filters)
        self.merge_python_icat_limit_skip_filters()
        self.clear_python_icat_order_filters()
        self.apply_filters(query)
