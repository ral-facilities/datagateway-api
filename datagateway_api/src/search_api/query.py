from datagateway_api.src.datagateway_api.icat.query import ICATQuery
from datagateway_api.src.search_api.panosc_mappings import mappings
from datagateway_api.src.search_api.session_handler import SessionHandler


# TODO - Not sure if this should inherit from `ICATQuery`?
class SearchAPIQuery:
    def __init__(self, panosc_entity_name):
        self.panosc_entity_name = panosc_entity_name
        self.icat_entity_name = mappings.mappings[panosc_entity_name][
            "base_icat_entity"
        ]

        self.query = ICATQuery(SessionHandler.client, self.icat_entity_name)
