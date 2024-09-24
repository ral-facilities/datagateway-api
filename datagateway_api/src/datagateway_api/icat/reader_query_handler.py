import logging

from datagateway_api.src.common.config import Config
from datagateway_api.src.common.filter_order_handler import FilterOrderHandler
from datagateway_api.src.datagateway_api.icat.filters import PythonICATWhereFilter
from datagateway_api.src.datagateway_api.icat.query import ICATQuery

log = logging.getLogger()


class ReaderQueryHandler:
    # TODO - better names and comments on dicts to explain what they're for
    # TODO - add docstrings
    entity_filter_check = {"Datafile": "dataset.id", "Dataset": "investigation.id"}
    entity_type_check = {"Datafile": "Dataset", "Dataset": "Investigation"}

    def __init__(self, entity_type, filters):
        self.entity_type = entity_type
        self.filters = filters
        log.debug(
            "Instance of ReaderQueryHandler created for a '%s' request",
            self.entity_type,
        )
        self.reader_query_eligible = self.check_eligibility()

    def check_eligibility(self):
        reader_config = Config.config.datagateway_api.use_reader_for_performance
        if not reader_config:
            return False
        if not reader_config.enabled:
            return False

        log.info("Checking whether query is eligible to go via reader account")
        if self.entity_type in ReaderQueryHandler.entity_filter_check.keys():
            if self.get_where_filter_for_entity_id_check():
                return True

        return False

    def is_query_eligible_for_reader_performance(self):
        return self.reader_query_eligible

    def get_where_filter_for_entity_id_check(self):
        for query_filter in self.filters:
            if (
                isinstance(query_filter, PythonICATWhereFilter)
                and query_filter.field
                == ReaderQueryHandler.entity_filter_check[self.entity_type]
                and query_filter.operation == "eq"
            ):
                log.debug(
                    "WHERE filter relevant for reader query checking: %s", query_filter,
                )
                self.where_filter_entity_id = query_filter.value
                return query_filter

        return None

    def is_user_authorised_to_see_entity_id(self, client):
        log.info(
            "Checking to see if user '%s' can see '%s' = %s",
            client.getUserName(),
            ReaderQueryHandler.entity_filter_check[self.entity_type],
            self.where_filter_entity_id,
        )
        access_query = ICATQuery(
            client,
            ReaderQueryHandler.entity_type_check[self.entity_type],
        )
        id_check = PythonICATWhereFilter("id", self.where_filter_entity_id, "eq")
        access_filter_handler = FilterOrderHandler()
        access_filter_handler.manage_icat_filters([id_check], access_query.query)
        results = access_query.execute_query(client)

        if results:
            log.debug(
                "User is authorised to see '%s' '%s'",
                ReaderQueryHandler.entity_filter_check[self.entity_type],
                self.where_filter_entity_id,
            )
            user_authorised = True
        else:
            log.debug(
                "User is NOT authorised to see '%s' '%s'",
                ReaderQueryHandler.entity_filter_check[self.entity_type],
                self.where_filter_entity_id,
            )
            user_authorised = False

        return user_authorised
