from datagateway_api.src.datagateway_api.icat.query import ICATQuery
from datagateway_api.src.search_api.panosc_mappings import mappings
from datagateway_api.src.search_api.session_handler import SessionHandler


class SearchAPIQuery:
    def __init__(self, panosc_entity_name, **kwargs):
        self.panosc_entity_name = panosc_entity_name
        self.icat_entity_name = mappings.mappings[panosc_entity_name][
            "base_icat_entity"
        ]

        self.icat_query = ICATQuery(
            SessionHandler.client, self.icat_entity_name, **kwargs,
        )

    def __repr__(self):
        return (
            f"PaNOSC Entity Name: {self.panosc_entity_name}, ICAT Entity Name:"
            f" {self.icat_entity_name}, ICAT Query: {str(self.icat_query.query)}"
        )
