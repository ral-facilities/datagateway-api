import logging

from datagateway_api.common.config import config
from datagateway_api.common.exceptions import FilterError
from datagateway_api.common.filters import (
    DistinctFieldFilter,
    IncludeFilter,
    LimitFilter,
    OrderFilter,
    SkipFilter,
    WhereFilter,
)


log = logging.getLogger()


class PythonICATWhereFilter(WhereFilter):
    def __init__(self, field, value, operation):
        super().__init__(field, value, operation)
        self.field = field

    def apply_filter(self, query):
        try:
            log.info("Adding ICAT where filter (for %s) to query", self.value)
            query.addConditions(self.create_filter())
        except ValueError:
            raise FilterError(
                "Something went wrong when adding WHERE filter to ICAT query",
            )

    def create_filter(self):
        """
        Create what's needed for a where filter dependent on the operation provided

        The logic in this function has been abstracted away from `apply_filter()` to
        make that function used for its named purpose, and no more.

        :return: A where filter (of type :class:`dict`) ready to be applied to a Query
            object
        :raises FilterError: If the operation provided to the instance isn't valid
        """

        log.info("Creating condition for ICAT where filter")
        if self.operation == "eq":
            where_filter = self.create_condition(self.field, "=", self.value)
        elif self.operation == "ne":
            where_filter = self.create_condition(self.field, "!=", self.value)
        elif self.operation == "like":
            where_filter = self.create_condition(self.field, "like", f"%{self.value}%")
        elif self.operation == "nlike":
            where_filter = self.create_condition(
                self.field, "not like", f"%{self.value}%",
            )
        elif self.operation == "lt":
            where_filter = self.create_condition(self.field, "<", self.value)
        elif self.operation == "lte":
            where_filter = self.create_condition(self.field, "<=", self.value)
        elif self.operation == "gt":
            where_filter = self.create_condition(self.field, ">", self.value)
        elif self.operation == "gte":
            where_filter = self.create_condition(self.field, ">=", self.value)
        elif self.operation == "in":
            # Convert self.value into a string with brackets equivalent to tuple format.
            # Cannot convert straight to tuple as single element tuples contain a
            # trailing comma which Python ICAT/JPQL doesn't accept
            self.value = str(self.value).replace("[", "(").replace("]", ")")

            # DataGateway Search can send requests with blank lists. Adding NULL to the
            # filter prevents the API from returning a 500. An empty list will be
            # returned instead, equivalent to the DB backend
            if self.value == "()":
                self.value = "(NULL)"

            where_filter = self.create_condition(self.field, "in", self.value)
        else:
            raise FilterError(f"Bad operation given to where filter: {self.operation}")

        log.debug("ICAT Where Filter: %s", where_filter)

        return where_filter

    @staticmethod
    def create_condition(attribute_name, operator, value):
        """
        Construct and return a Python dictionary containing conditions to be used in a
        Query object

        :param attribute_name: Attribute name to search
        :type attribute_name: :class:`str`
        :param operator: Operator to use when filtering the data
        :type operator: :class:`str`
        :param value: What ICAT will use to filter the data
        :type value: :class:`str` or :class:`tuple` (when using an IN expression)
        :return: Condition (of type :class:`dict`) ready to be added to a Python ICAT
            Query object
        """

        conditions = {}
        # Removing quote marks when doing conditions with IN expressions or when a
        # distinct filter is used in a request
        jpql_value = (
            f"{value}"
            if operator == "in" or operator == "!=" or "o." in str(value)
            else f"'{value}'"
        )

        conditions[attribute_name] = f"{operator} {jpql_value}"
        log.debug("Conditions in ICAT where filter, %s", conditions)
        return conditions


class PythonICATDistinctFieldFilter(DistinctFieldFilter):
    def __init__(self, fields):
        super().__init__(fields)

    def apply_filter(self, query):
        try:
            log.info("Adding ICAT distinct filter to ICAT query")
            log.debug("Fields for distinct filter: %s", self.fields)

            # These aggregate keywords not currently used in the API, but conditional
            # present in case they're used in the future
            if query.aggregate == "AVG" or query.aggregate == "SUM":
                # Distinct can be combined with other aggregate functions
                query.setAggregate(f"{query.aggregate}:DISTINCT")
            elif query.aggregate == "COUNT":
                # When count and distinct keywords are used together when selecting
                # multiple attributes, Python ICAT will always throw an error on query
                # execution (more info:
                # https://github.com/icatproject/python-icat/issues/76). This appears to
                # be a JPQL limitation, something that cannot be fixed in Python ICAT.
                # As a result, the API will get the distinct results and manually
                # perform `len()` on the list, using `manual_count` as a flag to
                # recognise this situation
                query.setAggregate("DISTINCT")
                log.debug("Manual count flag enabled")
                query.manual_count = True
            else:
                query.setAggregate("DISTINCT")

            query.setAttributes(self.fields)

        except ValueError as e:
            raise FilterError(e)


class PythonICATOrderFilter(OrderFilter):
    # Used to append the order tuples across all filters in a single request
    result_order = []
    # When 1-many relationships occur, entities should be joined using a LEFT JOIN to
    # prevent disappearing results when sorting on DataGateway's table view
    join_specs = {}

    def __init__(self, field, direction):
        # Python ICAT doesn't automatically uppercase the direction, errors otherwise
        super().__init__(field, direction.upper())

    def apply_filter(self, query):
        PythonICATOrderFilter.result_order.append((self.field, self.direction))
        log.debug("Result Order: %s", PythonICATOrderFilter.result_order)

        try:
            log.info("Adding order filter (for %s)", self.field)
            query.setOrder(PythonICATOrderFilter.result_order)
        except ValueError as e:
            # Typically invalid attribute(s)
            raise FilterError(e)

        split_fields = self.field.split(".")
        for field_pointer in range(len(split_fields)):
            # Looking for plural entities but not field names
            # This is to avoid adding JOINs to field names such as job's argument field
            if (
                split_fields[field_pointer].endswith("s")
                and split_fields[field_pointer] != split_fields[-1]
            ):
                # Length minus 1 is used to omit field names, same reason as above
                for join_field_pointer in range(field_pointer, len(split_fields) - 1):
                    join_field_list = split_fields[
                        field_pointer : join_field_pointer + 1
                    ]
                    join_field_str = ".".join(join_field_list)

                    PythonICATOrderFilter.join_specs[join_field_str] = "LEFT JOIN"

                log.debug(
                    "Setting query join specs: %s", PythonICATOrderFilter.join_specs,
                )
                try:
                    query.setJoinSpecs(PythonICATOrderFilter.join_specs)
                except (TypeError, ValueError) as e:
                    raise FilterError(e)

                break


class PythonICATSkipFilter(SkipFilter):
    def __init__(self, skip_value):
        super().__init__(skip_value)

    def apply_filter(self, query):
        icat_properties = config.get_icat_properties()
        icat_set_limit(query, self.skip_value, icat_properties["maxEntities"])


class PythonICATLimitFilter(LimitFilter):
    def __init__(self, limit_value):
        super().__init__(limit_value)
        self.skip_value = 0

    def apply_filter(self, query):
        icat_set_limit(query, self.skip_value, self.limit_value)


def icat_set_limit(query, skip_number, limit_number):
    """
    Add limit (utilising skip and count) to an ICAT query

    :param query: ICAT Query object to execute within Python ICAT
    :type query: :class:`icat.query.Query`
    :param skip_number: Number of results to skip
    :type skip_number: :class:`int`
    :param limit_number: Number of results to limit in the query
    :type limit_number: :class:`int`
    :raises FilterError: If the tuple is not of two elements, or the elements aren't of
        the valid type
    """
    try:
        query.setLimit((skip_number, limit_number))
        log.debug("Current limit/skip values assigned to query: %s", query.limit)
    except TypeError as e:
        # Not a two element tuple as managed by Python ICAT's setLimit()
        raise FilterError(e)


class PythonICATIncludeFilter(IncludeFilter):
    def __init__(self, included_filters):
        self.included_filters = []
        log.info("Extracting fields for include filter")
        self._extract_filter_fields(included_filters)

    def _extract_filter_fields(self, field):
        """
        Using recursion, go through the fields and add them to the filter's instance.
        This means that lists within dictionaries, dictionaries within dictionaries are
        supported. Where dictionaries are involved, '.' are used to join the fields
        together

        Some (but not all) fields require the plural to be accepted in the include of a
        Python ICAT query - e.g. 'userGroups' is valid (plural required), but 'dataset'
        is also valid (plural not required). The dictionary `substnames` in Python
        ICAT's query.py gives a good overview of which need to be plural.

        :param field: Which field(s) should be included in the ICAT query
        :type field: :class:`str` or :class:`list` or :class:`dict`
        """
        if isinstance(field, str):
            log.debug("Adding %s to include filter", field)
            self.included_filters.append(field)
        elif isinstance(field, dict):
            for key, value in field.items():
                if not isinstance(key, str):
                    raise FilterError(
                        "Include Filter: Dictionary key should only be a string, not"
                        " any other type",
                    )

                if isinstance(value, str):
                    self._extract_filter_fields(".".join((key, value)))
                elif isinstance(value, list):
                    for element in value:
                        if isinstance(element, str):
                            # Will end up as: key.element1, key.element2 etc.
                            self._extract_filter_fields(".".join((key, element)))
                        elif isinstance(element, list):
                            for sub_element in element:
                                self._extract_filter_fields(
                                    ".".join((key, sub_element)),
                                )
                        elif isinstance(element, dict):
                            for (
                                inner_element_key,
                                inner_element_value,
                            ) in element.items():
                                if not isinstance(inner_element_key, str):
                                    raise FilterError(
                                        "Include Filter: Dictionary key should only be"
                                        " a string, not any other type",
                                    )
                                self._extract_filter_fields(
                                    {
                                        ".".join(
                                            (key, inner_element_key),
                                        ): inner_element_value,
                                    },
                                )
                elif isinstance(value, dict):
                    for inner_key, inner_value in value.items():
                        if not isinstance(inner_key, str):
                            raise FilterError(
                                "Include Filter: Dictionary key should only be a"
                                " string, not any other type",
                            )

                        # Will end up as: key.inner_key.inner_value
                        self._extract_filter_fields(
                            {".".join((key, inner_key)): inner_value},
                        )
                else:
                    raise FilterError(
                        "Include Filter: Inner field type (inside dictionary) not"
                        " recognised, cannot interpret input",
                    )
        elif isinstance(field, list):
            for element in field:
                self._extract_filter_fields(element)
        else:
            raise FilterError(
                "Include Filter: Field type not recognised, cannot interpret input",
            )

    def apply_filter(self, query):
        log.info("Applying include filter, adding fields: %s", self.included_filters)

        try:
            query.addIncludes(self.included_filters)
        except ValueError as e:
            raise FilterError(e)
