from datetime import datetime
import logging

from datagateway_api.src.common.date_handler import DateHandler
from datagateway_api.src.common.exceptions import FilterError
from datagateway_api.src.datagateway_api.icat.filters import (
    PythonICATIncludeFilter,
    PythonICATLimitFilter,
    PythonICATSkipFilter,
    PythonICATWhereFilter,
)
from datagateway_api.src.search_api.panosc_mappings import mappings
from datagateway_api.src.search_api.query import SearchAPIQuery

log = logging.getLogger()


# TODO - Implement each of these filters for Search API, inheriting from the Python ICAT
# versions


class SearchAPIWhereFilter(PythonICATWhereFilter):
    def __init__(self, field, value, operation, search_api_query=None):
        self.search_api_query = search_api_query
        super().__init__(field, value, operation)
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
            panosc_mapping_name, icat_field_name = self.get_icat_mapping(
                panosc_mapping_name, field_name,
            )
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

    def get_icat_mapping(self, panosc_entity_name, field_name):
        """
        This function searches the PaNOSC mappings (from `search_api_mapping.json`,
        maintained/stored by :class:`PaNOSCMappings`) and retrieves the ICAT translation
        from the PaNOSC input. Fields in the same entity can be found, as well as fields
        from related entities (e.g. Dataset.files.path) via recursion inside this
        function.

        An edge case for ICAT has been somewhat hardcoded into this function to dea
        with ICAT's different parameter value field names. The following mapping is
        assumed (where order matters):
        {"Parameter": {"value": ["numericValue", "stringValue", "dateTimeValue"]}}

        :param panosc_entity_name: A PaNOSC entity name e.g. "Dataset"
        :type panosc_entity_name: :class:`str`
        :param field_name: PaNOSC field name to fetch the ICAT version of e.g. "name"
        :type field_name: :class:`str`
        :return: Tuple containing the PaNOSC entity name (which will change from the
            input if a related entity is found) and the ICAT field name
            mapping/translation from the PaNOSC data model
        :raises FilterError: If a valid mapping cannot be found
        """

        log.info(
            "Searching mapping file to find ICAT translation for %s",
            f"{panosc_entity_name}.{field_name}",
        )

        try:
            icat_mapping = mappings.mappings[panosc_entity_name][field_name]
            log.debug("ICAT mapping/translation found: %s", icat_mapping)
        except KeyError as e:
            raise FilterError(f"Bad PaNOSC to ICAT mapping: {e.args}")

        if isinstance(icat_mapping, str):
            # Field name
            icat_field_name = icat_mapping
        elif isinstance(icat_mapping, dict):
            # Relation - JSON format: {PaNOSC entity name: ICAT related field name}
            panosc_entity_name = list(icat_mapping.keys())[0]
            icat_field_name = icat_mapping[panosc_entity_name]
        elif isinstance(icat_mapping, list):
            # Edge case for ICAT's different parameter value field names
            if isinstance(self.value, int) or isinstance(self.value, float):
                icat_field_name = icat_mapping[0]
            elif isinstance(self.value, datetime):
                icat_field_name = icat_mapping[2]
            elif isinstance(self.value, str):
                if DateHandler.is_str_a_date(self.value):
                    icat_field_name = icat_mapping[2]
                else:
                    icat_field_name = icat_mapping[1]
            else:
                self.value = str(self.value)
                icat_field_name = icat_mapping[1]

        log.debug(
            "Output of get_icat_mapping(): %s, %s", panosc_entity_name, icat_field_name,
        )

        return panosc_entity_name, icat_field_name

    def __str__(self):
        """
        String representation which is also used to apply WHERE filters that are inside
        a `NestedWhereFilters` object
        """

        if isinstance(self.search_api_query, SearchAPIQuery):
            log.info("__str__ for SearchAPIWhereFilter, SearchAPIQuery found")

            self.apply_filter(self.search_api_query)
            # Replicating the condition in Python ICAT format so it can be searched on
            # the query and return as string representation
            conds_dict = self.create_filter()
            a, jpql_func = self.search_api_query.icat_query.query._split_db_functs(
                self.field,
            )
            conds_dict[self.field] = self.search_api_query.icat_query.query._cond_value(
                conds_dict[self.field], jpql_func,
            )

            str_conds = self.search_api_query.icat_query.query.search_conditions(
                self.field, conds_dict,
            )

            try:
                return str_conds[0]
            except IndexError:
                raise FilterError("Condition could not be found in Python ICAT query")
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


class SearchAPIIncludeFilter(PythonICATIncludeFilter):
    def __init__(self, included_filters):
        super().__init__(included_filters)

    def apply_filter(self, query):
        return super().apply_filter(query.icat_query.query)
