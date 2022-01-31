import json
import logging
from pathlib import Path
import sys

from datagateway_api.src.common.config import Config
from datagateway_api.src.common.exceptions import SearchAPIError

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
            # The API shouldn't exit if there's an exception (e.g. file not found) if
            # the user is only using DataGateway API and not the search API
            if Config.config.search_api:
                sys.exit(
                    f"An error occurred while trying to load the PaNOSC mappings: {e}",
                )

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
