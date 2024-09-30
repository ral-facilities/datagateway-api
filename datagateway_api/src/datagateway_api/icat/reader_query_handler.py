import logging
from typing import List, Optional

from icat.exception import ICATSessionError

from datagateway_api.src.common.config import Config
from datagateway_api.src.common.exceptions import PythonICATError
from datagateway_api.src.common.filter_order_handler import FilterOrderHandler
from datagateway_api.src.common.filters import QueryFilter
from datagateway_api.src.datagateway_api.icat.filters import PythonICATWhereFilter
from datagateway_api.src.datagateway_api.icat.icat_client_pool import ICATClient
from datagateway_api.src.datagateway_api.icat.query import ICATQuery

log = logging.getLogger()


class ReaderQueryHandler:
    """
    This class handles the mechanism that allows 'performance queries' to occur on
    particular endpoints. These queries are to improve performance on requests that have
    a WHERE filter on the ID of the parent entity where passing the query directly to
    ICAT can cause performance issues. This is due to the complexity of the ICAT rules,
    meaning a relatively simple SQL query is a long paragraph of SQL. The rules are
    bypassed by performing an equivalent check to see if the user can see the parent
    entity by querying for it directly. Once permissions have been verified, the user's
    original query is executed using a configurable reader account.

    On a production instance where this functionality is needed, the reader account will
    have been setup with appropriate ICAT rules to view the entities.

    Example workflow:
    - User sends request to /datafiles with a WHERE filter of dataset.id = 4
    - Query is determined as eligble
    - Dataset query is sent to ICAT with a WHERE filter of id = 4
    - If the appropriate dataset is returned, the user's original query is executed, but
      as the reader account, not the user's account
    - If no dataset is found (i.e. the user doesn't have permission is view the dataset)
      the API responds with a 403
    """

    # Lookup to determine which field to search whether a user has permission to view
    entity_filter_check = {"Datafile": "dataset.id", "Dataset": "investigation.id"}
    parent_entity_lookup = {"Datafile": "Dataset", "Dataset": "Investigation"}
    # Keep a cached reader_client for faster queries. A reader client is created when
    # the first instance of this class is created and is refreshed when a login attempt
    # fails (due to an expired session ID)
    reader_client = None

    def __init__(self, entity_type: str, filters: List[QueryFilter]) -> None:
        self.entity_type = entity_type
        self.filters = filters
        log.debug(
            "Instance of ReaderQueryHandler created for a '%s' request",
            self.entity_type,
        )
        self.reader_query_eligible = self.check_eligibility()
        if not ReaderQueryHandler.reader_client:
            self.create_reader_client()

    def create_reader_client(self) -> ICATClient:
        """
        Create a new client (assigning it as a class variable) and login using the
        reader's credentials. If the credentials aren't valid, a PythonICATError is
        raised (resulting in a 500). The client object is returned
        """

        log.info("Creating reader_client")
        ReaderQueryHandler.reader_client = ICATClient("datagateway_api")
        reader_config = Config.config.datagateway_api.use_reader_for_performance
        login_credentals = {
            "username": reader_config.reader_username,
            "password": reader_config.reader_password,
        }
        try:
            ReaderQueryHandler.reader_client.login(
                reader_config.reader_mechanism, login_credentals,
            )
        except ICATSessionError:
            log.error("User credentials for reader account aren't valid")
            raise PythonICATError("Internal error with reader account configuration")
        return ReaderQueryHandler.reader_client

    def check_eligibility(self) -> bool:
        """
        This function checks whether the input query can be executed as a 'reader
        performance query'. The entity of the query needs to be in `entity_filter_check`
        and an appropriate WHERE filter needs to be sought
        (using `get_where_filter_for_entity_id_check()`)
        """
        log.info("Checking whether query is eligible to go via reader account")
        if self.entity_type in ReaderQueryHandler.entity_filter_check.keys():
            if self.get_where_filter_for_entity_id_check():
                return True

        return False

    def is_query_eligible_for_reader_performance(self) -> bool:
        """
        Getter that returns a boolean regarding query eligibility
        """
        return self.reader_query_eligible

    def get_where_filter_for_entity_id_check(self) -> Optional[PythonICATWhereFilter]:
        """
        Iterate through the instance's query filters and return a WHERE filter for a
        relevant parent entity (e.g. dataset.id or datafile.id). The WHERE filter must
        use the 'eq' operator
        """

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

    def is_user_authorised_to_see_entity_id(self, client) -> bool:
        """
        This function checks whether the user is authorised to see a parent entity (e.g.
        if they query /datafiles, whether they can see a particular dataset). A query is
        created and sent to ICAT for execution - the query is performed using the
        session ID provided in the request
        """

        log.info(
            "Checking to see if user '%s' can see '%s' = %s",
            client.getUserName(),
            ReaderQueryHandler.entity_filter_check[self.entity_type],
            self.where_filter_entity_id,
        )
        access_query = ICATQuery(
            client, ReaderQueryHandler.parent_entity_lookup[self.entity_type],
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
