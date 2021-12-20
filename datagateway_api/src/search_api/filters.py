import logging

from icat.query import Query

from datagateway_api.src.datagateway_api.icat.filters import (
    PythonICATIncludeFilter,
    PythonICATLimitFilter,
    PythonICATSkipFilter,
    PythonICATWhereFilter,
)
from datagateway_api.src.search_api.panosc_mappings import mappings

log = logging.getLogger()


# TODO - Implement each of these filters for Search API, inheriting from the Python ICAT
# versions


class SearchAPIWhereFilter(PythonICATWhereFilter):
    def __init__(self, field, value, operation):
        super().__init__(field, value, operation)

    def apply_filter(self, query):
        # Convert the field from a PaNOSC field name to an ICAT one
        icat_field_name = mappings.mappings[query.panosc_entity_name][self.field]
        self.field = icat_field_name

        # TODO - `query.query.query` might be confusing, might rename `query` in
        # function signature
        return super().apply_filter(query.query.query)

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
        """

        try:
            icat_mapping = mappings.mappings[panosc_entity_name][field_name]
        except KeyError as e:
            raise FilterError(f"Bad PaNOSC to ICAT mapping: {e.args}")

        print(f"ICAT Mapping: {icat_mapping}, Type: {type(icat_mapping)}")
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

        return (panosc_entity_name, icat_field_name)

    def __str__(self):
        # TODO - can't just hardcode investigation entity. Might need `icat_entity_name`
        # to be passed into init
        query = Query(client, "Investigation")
        query.addConditions(self.create_filter())
        str_conds = query.get_conditions_as_str()

        return str_conds[0]

    def __repr__(self):
        return (
            f"Field: '{self.field}', Value: '{self.value}', Operation:"
            f" '{self.operation}'"
        )


class SearchAPISkipFilter(PythonICATSkipFilter):
    def __init__(self, skip_value):
        super().__init__(skip_value, filter_use="search_api")

    def apply_filter(self, query):
        return super().apply_filter(query.query.query)


class SearchAPILimitFilter(PythonICATLimitFilter):
    def __init__(self, limit_value):
        super().__init__(limit_value)

    def apply_filter(self, query):
        return super().apply_filter(query.query.query)


class SearchAPIIncludeFilter(PythonICATIncludeFilter):
    def __init__(self, included_filters):
        super().__init__(included_filters)

    def apply_filter(self, query):
        return super().apply_filter(query.query.query)
