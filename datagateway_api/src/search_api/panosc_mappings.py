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


# TODO - don't think I'll need this
def load_mappings(path=Path(__file__).parent.parent.parent / "search_api_mapping.json"):
    try:
        with open(path, encoding="utf-8") as target:
            data = json.load(target)
    except IOError as e:
        raise SearchAPIError(e)

    return data


mappings = PaNOSCMappings()
