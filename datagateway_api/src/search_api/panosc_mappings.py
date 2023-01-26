import json
import logging
from pathlib import Path
import sys

from datagateway_api.src.common.config import Config
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
            # The API shouldn't exit if there's an exception (e.g. file not found) if
            # the user is only using DataGateway API and not the search API
            if Config.config.search_api:
                sys.exit(
                    f"An error occurred while trying to load the PaNOSC mappings: {e}",
                )

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
            icat_mapping = self.mappings[panosc_entity_name][field_name]
            # Too verbose log.debug("ICAT mapping/translation found: %s", icat_mapping)
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

        return panosc_entity_name, icat_field_name

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

    def get_panosc_non_related_field_names(self, panosc_entity_name):
        """
        This function retrieves the names of the non related fields of a given PaNOSC
        entity.

        :param panosc_entity_name: A PaNOSC entity name e.g. "Dataset"
        :type panosc_entity_name: :class:`str`
        :return: List containing the names of the non related fields of the given
            PaNOSC entity
        :raises FilterError: If mappings for the given entity name cannot be found
        """
        try:
            entity_mappings = self.mappings[panosc_entity_name]
        except KeyError:
            raise FilterError(
                f"Cannot find mappings for {[panosc_entity_name]} PaNOSC entity",
            )

        non_related_field_names = []
        for mapping_key, mapping_value in entity_mappings.items():
            # The mappings for the non-related fields are of type `str` and sometimes
            # `list' whereas for the related fields, they are of type `dict`.
            if mapping_key != "base_icat_entity" and (
                isinstance(mapping_value, str) or isinstance(mapping_value, list)
            ):
                non_related_field_names.append(mapping_key)

        return non_related_field_names

    def get_icat_relations_for_panosc_non_related_fields(self, panosc_entity_name):
        """
        This function retrieves the ICAT relations for the non related fields of a
        given PaNOSC entity.

        :param panosc_entity_name: A PaNOSC entity name e.g. "Dataset"
        :type panosc_entity_name: :class:`str`
        :return: List containing the ICAT relations for the non related fields of the
            given PaNOSC entity
        """
        icat_relations = []

        field_names = self.get_panosc_non_related_field_names(panosc_entity_name)
        for field_name in field_names:
            _, icat_mapping = self.get_icat_mapping(panosc_entity_name, field_name)

            if not isinstance(icat_mapping, list):
                icat_mapping = [icat_mapping]

            for mapping in icat_mapping:
                split_mapping = mapping.split(".")
                if len(split_mapping) > 1:
                    # Remove the last split element because it is an ICAT
                    # field name and is not therefore part of the relation
                    split_mapping = split_mapping[:-1]
                    split_mapping = ".".join(split_mapping)
                    icat_relations.append(split_mapping)

        return icat_relations

    def get_icat_relations_for_non_related_fields_of_panosc_relation(
        self, panosc_entity_name, entity_relation,
    ):
        """
        THis function retrieves the ICAT relations for the non related fields of all the
        PaNOSC entities that form a given PaNOSC entity relation which is applied to a
        given PaNOSC entity. Relations can be non-nested or nested. Those that are
        nested are represented in a dotted format e.g. "documents.members.person". When
        a given relation is nested, this function retrieves the ICAT relations for the
        first PaNOSC entity and then recursively calls itself until the ICAT relations
        for the last PaNOSC entity in the relation are retrieved.

        :param panosc_entity_name: A PaNOSC entity name e.g. "Dataset" to which the
            PaNOSC entity relation is applied
        :type panosc_entity_name: :class:`str`
        :param panosc_entity_name: A PaNOSC entity relation e.g. "documents" or
            "documents.members.person" if nested
        :type panosc_entity_name: :class:`str`
        :return: List containing the ICAT relations for the non related fields of all
            the PaNOSC entitities that form the given PaNOSC entity relation
        """
        icat_relations = []

        split_entity_relation = entity_relation.split(".")
        related_entity_name, icat_field_name = self.get_icat_mapping(
            panosc_entity_name, split_entity_relation[0],
        )
        relations = self.get_icat_relations_for_panosc_non_related_fields(
            related_entity_name,
        )
        icat_relations.extend(relations)

        if len(split_entity_relation) > 1:
            entity_relation = ".".join(split_entity_relation[1:])
            relations = self.get_icat_relations_for_non_related_fields_of_panosc_relation(  # noqa: B950
                related_entity_name, entity_relation,
            )
            icat_relations.extend(relations)

        for i, icat_relation in enumerate(icat_relations):
            icat_relations[i] = f"{icat_field_name}.{icat_relation}"

        return icat_relations


mappings = PaNOSCMappings()
