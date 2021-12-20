import json
from pathlib import Path

from datagateway_api.src.common.exceptions import SearchAPIError


class PaNOSCMappings:
    def __init__(
        self, path=Path(__file__).parent.parent.parent / "search_api_mapping.json",
    ):
        try:
            with open(path, encoding="utf-8") as target:
                self.mappings = json.load(target)
        except IOError as e:
            raise SearchAPIError(e)

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


# TODO - don't think I'll need this
def load_mappings(path=Path(__file__).parent.parent.parent / "search_api_mapping.json"):
    try:
        with open(path, encoding="utf-8") as target:
            data = json.load(target)
    except IOError as e:
        raise SearchAPIError(e)

    return data


mappings = PaNOSCMappings()
