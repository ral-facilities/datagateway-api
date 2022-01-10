import json
import logging
from pathlib import Path

from datagateway_api.src.common.exceptions import FilterError, SearchAPIError

log = logging.getLogger()


class PaNOSCMappings:
    def __init__(
        self, path=Path(__file__).parent.parent.parent / "search_api_mapping.json",
    ):
        """Load contents of `search_api_mapping.json` into this class"""
        try:
            with open(path, encoding="utf-8") as target:
                log.info("Loading PaNOSC to ICAT mappings from %s", path)
                self.mappings = json.load(target)
        except IOError as e:
            raise SearchAPIError(e)

    def get_icat_mapping(self, panosc_entity_name, field_name):
        """
        This function searches the PaNOSC mappings and retrieves the ICAT translation
        from the PaNOSC input. Fields in the same entity can be found, as well as fields
        from related entities (e.g. Dataset.files.path) via recursion inside this
        function.

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
            # If a list of ICAT field names are found, this is likely to be a specific
            # need for that entity (e.g. parameter values). Dealing with this should be
            # delegated to other code in this repo so the entire list is returned here
            icat_field_name = icat_mapping

        return (panosc_entity_name, icat_field_name)

    def get_panosc_related_entity_name(
        self, panosc_entity_name, panosc_related_field_name,
    ):
        """
        For a given related field name (e.g. "files"), get the entity name version of
        this (e.g. "File")

        :param panosc_entity_name: Entity name used as an entrypoint into the mapping
        :type panosc_entity_name: :class:`str`
        :param panosc_related_field_name: Related field name which needs to be
            translated to the entity name format
        :type panosc_related_field_name: :class:`str`
        :return: Entity name for the given related field name
        :raises SearchAPIError: If a suitable mapping cannot be found
        """

        panosc_related_entity_name = ""
        try:
            panosc_related_entity_name = list(
                self.mappings[panosc_entity_name][panosc_related_field_name].keys(),
            )[0]
        except KeyError:
            raise SearchAPIError(
                f"Cannot find related entity name from: {panosc_entity_name}"
                f", {panosc_related_field_name}",
            )

        return panosc_related_entity_name


mappings = PaNOSCMappings()
