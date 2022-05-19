from copy import copy
from datetime import datetime
import logging

from datagateway_api.src.common.date_handler import DateHandler
from datagateway_api.src.datagateway_api.icat.filters import (
    PythonICATIncludeFilter,
    PythonICATLimitFilter,
    PythonICATSkipFilter,
    PythonICATWhereFilter,
    PythonICATQueryFilter
)
from datagateway_api.src.search_api.models import PaNOSCAttribute
from datagateway_api.src.search_api.panosc_mappings import mappings
from datagateway_api.src.search_api.query import SearchAPIQuery

log = logging.getLogger()


class SearchAPIWhereFilter(PythonICATWhereFilter):
    def __init__(self, field, value, operation, search_api_query=None):
        self.search_api_query = search_api_query
        super().__init__(field, value, operation)

        # Detect various datetime formats and convert them into a format that ICAT can
        # understand
        if (
            self.field in PaNOSCAttribute._datetime_field_names
            and isinstance(self.value, str)
            and DateHandler.is_str_a_date(self.value)
        ):
            value_datetime = DateHandler.str_to_datetime_object(value)
            str_datetime = DateHandler.datetime_object_to_str(value_datetime)
            # +/- need to be removed so the format works when querying ICAT
            self.value = str_datetime.replace("+", " ").replace("-", " ")

        log.info("SearchAPIWhereFilter created: %s", repr(self))

    def apply_filter(self, query):
        log.info("Applying SearchAPIWhereFilter to: %s", type(query))
        log.debug("Current WHERE filter data: %s", repr(self))

        panosc_field_names = self.field.split(".")
        icat_field_names = []
        panosc_mapping_name = query.panosc_entity_name

        log.debug(
            "Converting PaNOSC where input to ICAT using: %s (PaNOSC field names) and"
            " %s (PaNOSC mapping name)",
            panosc_field_names,
            panosc_mapping_name,
        )

        # Convert PaNOSC field names to ICAT field names
        for field_name in panosc_field_names:
            panosc_mapping_name, icat_field_name = mappings.get_icat_mapping(
                panosc_mapping_name, field_name,
            )

            # Edge cases for ICAT have been somewhat hardcoded here, to deal with
            # ICAT's different parameter value and sample pid field names.
            if isinstance(icat_field_name, list):
                # The following mapping is assumed for parameter value (where order
                # matters):
                # {"Parameter": {"value": ["numericValue", "stringValue", "dateTimeValue"]}} # noqa: B950
                if field_name == "value":
                    # If the value is a list, extract the first value to determine which
                    # parameter value type should be used
                    if self.operation == "between" and isinstance(self.value, list):
                        filter_value = self.value[0]
                    else:
                        filter_value = self.value

                    if isinstance(filter_value, (int, float)):
                        icat_field_name = icat_field_name[0]
                    elif isinstance(filter_value, datetime):
                        icat_field_name = icat_field_name[2]
                    elif isinstance(filter_value, str):
                        if DateHandler.is_str_a_date(filter_value):
                            icat_field_name = icat_field_name[2]
                        else:
                            icat_field_name = icat_field_name[1]
                    else:
                        self.value = str(self.value)
                        icat_field_name = icat_field_name[1]
                # The following mapping is assumed for sample pid (where order matters):
                # {"Sample": {"pid": ["pid", "id"]}}
                elif field_name == "pid":
                    if "pid:" in self.value:
                        icat_field_name = icat_field_name[1]
                        self.value = self.value.replace("pid:", "")
                    else:
                        icat_field_name = icat_field_name[0]

            icat_field_names.append(icat_field_name)

        log.debug(
            "PaNOSC to ICAT translation for where filter: %s (PaNOSC), %s (ICAT)",
            panosc_field_names,
            icat_field_names,
        )

        # Once we have got ICAT field names we no longer need the PaNOSC versions so
        # overwriting them is all good. ICAT version needs to be in `self.field` due to
        # code written in `PythonICATWhereFilter.apply_filter()`
        self.field = ".".join(icat_field_names)

        return super().apply_filter(query.icat_query.query)

    def __str__(self):
        """
        String representation which is also used to apply WHERE filters that are inside
        a `NestedWhereFilters` object
        """

        if isinstance(self.search_api_query, SearchAPIQuery):
            # Making a copy of the filter because `apply_filter()` can only be executed
            # once per filter successfully
            filter_copy = copy(self)

            # Applying filter to the query so we get the correct JOINs, something not
            # managed by the search API when we build the WHERE clause ourselves
            self.apply_filter(self.search_api_query)

            # Using a blank query to ensure the correct condition is retrieved from the
            # where clause
            blank_query = SearchAPIQuery(self.search_api_query.panosc_entity_name)
            filter_copy.apply_filter(blank_query)
            where_clause = blank_query.icat_query.query.where_clause
            # The WHERE keyword is added by `ConditionSettingQuery`, where the
            # `where_clause` property is overridden to support the search API building
            # its own WHERE clauses to support `NestedWhereFilters`
            str_cond = where_clause.replace("WHERE ", "")

            return str_cond
        else:
            log.info(
                "__str__ for SearchAPIWhereFilter, no query found so repr() will be"
                " returned",
            )
            return repr(self)

    def __repr__(self):
        return (
            f"Field: '{self.field}', Value: '{self.value}', Operation:"
            f" '{self.operation}'"
        )


class SearchAPISkipFilter(PythonICATSkipFilter):
    def __init__(self, skip_value):
        super().__init__(skip_value, filter_use="search_api")

    def apply_filter(self, query):
        return super().apply_filter(query.icat_query.query)


class SearchAPILimitFilter(PythonICATLimitFilter):
    def __init__(self, limit_value):
        super().__init__(limit_value)

    def apply_filter(self, query):
        return super().apply_filter(query.icat_query.query)

class SearchAPIQueryFilter(PythonICATQueryFilter):
    def __init__(self, query_value):
        super().__init__(query_value)

    def apply_filter(self, query):
        return super().apply_filter(query.icat_query.query)

class SearchAPIIncludeFilter(PythonICATIncludeFilter):
    def __init__(self, included_filters, panosc_entity_name):
        self.included_filters = included_filters
        self.panosc_entity_name = panosc_entity_name
        super().__init__(included_filters)

    def apply_filter(self, query):
        icat_field_names = []

        for panosc_field_name in self.included_filters:
            # Need an empty list at start of each iteration to clear field names from
            # previous iterations
            split_icat_field_name = []

            panosc_entity_name = self.panosc_entity_name
            split_panosc_fields = panosc_field_name.split(".")

            for split_field in split_panosc_fields:
                panosc_entity_name, icat_field_name = mappings.get_icat_mapping(
                    panosc_entity_name, split_field,
                )
                split_icat_field_name.append(icat_field_name)

            icat_field_names.append(".".join(split_icat_field_name))

        # All PaNOSC field names translated to ICAT, so we can overwrite the PaNOSC
        # versions with the ICAT mappings so they can be used to apply the filter via
        # `super().apply_filter()`
        self.included_filters = icat_field_names

        return super().apply_filter(query.icat_query.query)
