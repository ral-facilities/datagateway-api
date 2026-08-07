from datetime import datetime, timezone
import logging
from typing import List, Optional

from cachetools.func import ttl_cache
from icat.exception import ICATSessionError

from datagateway_api.common.config import Config
from datagateway_api.common.exceptions import MissingRecordError, PythonICATError
from datagateway_api.common.filters import QueryFilter
from datagateway_api.datagateway_api.icat.filters import PythonICATWhereFilter
from datagateway_api.datagateway_api.icat.icat_client_pool import ICATClient

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
    maxsize = 128  # cachetools default value
    ttl = 600  # seconds, cachetools default value
    if Config.config.icat.reader is not None:
        maxsize = Config.config.icat.reader.maxsize
        ttl = Config.config.icat.reader.ttl

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

    @classmethod
    def create_reader_client(cls) -> ICATClient:
        """
        Create a new client (assigning it as a class variable) and login using the
        reader's credentials. If the credentials aren't valid, a PythonICATError is
        raised (resulting in a 500). The client object is returned
        """
        log.info("Creating reader_client")
        cls.reader_client = ICATClient()
        try:
            cls.reader_client.login(
                auth=Config.config.icat.reader.mechanism,
                credentials={
                    "username": Config.config.icat.reader.username,
                    "password": Config.config.icat.reader.password.get_secret_value(),
                },
            )
        except ICATSessionError as e:
            log.error("User credentials for reader account aren't valid")
            raise PythonICATError("Internal error with reader account configuration") from e

        return cls.reader_client

    @classmethod
    def refresh(cls) -> None:
        """
        Refresh `cls.reader_client` if it is defined and is close to expiring.
        If it is not defined, or has already expired, create a new one.
        """
        if cls.reader_client is not None and cls.reader_client.sessionId is not None:
            try:
                cls.reader_client.autoRefresh()
                return
            except ICATSessionError:
                log.debug("Reader session expired")

        cls.create_reader_client()

    @classmethod
    @ttl_cache(maxsize=maxsize, ttl=ttl)
    def get_investigation_id(cls, dataset_id: int) -> int:
        """
        Args:
            dataset_id (int): ICAT Dataset.id.

        Raises:
            MissingRecordError: If no Dataset with `dataset_id` is found.

        Returns:
            int: ICAT id of the Dataset's parent Investigation.
        """
        query = f"SELECT d.investigation.id FROM Dataset d WHERE d.id={dataset_id}"  # noqa: S608
        cls.refresh()
        investigation_ids = cls.reader_client.search(query)
        if len(investigation_ids) == 0:
            raise MissingRecordError(f"No Dataset found for id={dataset_id}")

        log.debug("Found investigation.id=%s for dataset.id=%s", investigation_ids[0], dataset_id)
        return investigation_ids[0]

    @classmethod
    @ttl_cache(maxsize=maxsize, ttl=ttl)
    def get_investigation_users(cls, investigation_id: int) -> set[str]:
        """
        Args:
            investigation_id (int): ICAT Investigation.id.

        Returns:
            set[str]:
                ICAT User.name of all InvestigationUsers associated with the Investigation with id `investigation_id`.
        """
        query = (
            f"SELECT iu.user.name FROM InvestigationUser iu WHERE iu.investigation.id={investigation_id}"  # noqa: S608
        )
        cls.refresh()
        user_names = cls.reader_client.search(query=query)
        log.debug("Found %s as InvestigationUsers for investigation.id=%s", user_names, investigation_id)
        return set(user_names)

    @classmethod
    @ttl_cache(maxsize=maxsize, ttl=ttl)
    def get_instrument_scientists(cls, investigation_id: int) -> set[str]:
        """
        Args:
            investigation_id (int): ICAT Investigation.id.

        Returns:
            set[str]:
                ICAT User.name of all InstrumentScientists associated with the Investigation with id `investigation_id`.
        """
        query = (
            "SELECT s.user.name FROM InstrumentScientist s "  # noqa: S608
            f"LEFT JOIN s.instrument.investigationInstruments ii WHERE ii.investigation.id={investigation_id}"
        )
        cls.refresh()
        user_names = cls.reader_client.search(query=query)
        log.debug("Found %s as InstrumentScientists for investigation.id=%s", user_names, investigation_id)
        return set(user_names)

    @classmethod
    def is_user_allowed(cls, user_name: str, investigation_id: int) -> bool:
        """
        Args:
            user_name (str): ICAT User.name.
            investigation_id (int): ICAT Investigation.id.

        Returns:
            bool: If `user_name` has an association with `investigation_id` allowing read access.
        """
        return user_name in cls.get_investigation_users(
            investigation_id=investigation_id,
        ) or user_name in cls.get_instrument_scientists(investigation_id=investigation_id)

    @classmethod
    @ttl_cache(maxsize=maxsize, ttl=ttl)
    def is_dataset_open(cls, dataset_id: int) -> bool:
        """
        Args:
            dataset_id (int): ICAT Dataset.id.

        Returns:
            bool: Whether the Dataset with `dataset_id` has been made open/public.
        """
        query = (
            "SELECT dp.publicationDate FROM DataPublication dp JOIN dp.content c "  # noqa: S608
            f"JOIN c.dataCollectionDatasets dcd WHERE dcd.dataset.id={dataset_id}"
        )
        cls.refresh()
        for publication_date in cls.reader_client.search(query):
            if publication_date < datetime.now(tz=timezone.utc):
                log.debug("dataset.id=%s is open", dataset_id)
                return True

        log.debug("dataset.id=%s is closed", dataset_id)
        return False

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
                and query_filter.field == ReaderQueryHandler.entity_filter_check[self.entity_type]
                and query_filter.operation == "eq"
            ):
                log.debug(
                    "WHERE filter relevant for reader query checking: %s",
                    query_filter,
                )
                self.where_filter_entity_id = int(query_filter.value)
                return query_filter

        return None

    def is_user_authorised_to_see_entity_id(self, client) -> bool:
        """
        This function checks whether the user is authorised to see a parent entity (e.g.
        if they query /datafiles, whether they can see a particular dataset). A query is
        created and sent to ICAT for execution - the query is performed using the
        session ID provided in the request
        """
        user_name = client.getUserName()
        id_field = ReaderQueryHandler.entity_filter_check[self.entity_type]
        log.info("Checking to see if user '%s' can see %s=%s", user_name, id_field, self.where_filter_entity_id)

        if self.entity_type == "Dataset":
            if ReaderQueryHandler.is_user_allowed(user_name=user_name, investigation_id=self.where_filter_entity_id):
                log.debug("User is authorised to see investigation.id=%s", self.where_filter_entity_id)
                return True

        elif self.entity_type == "Datafile":
            investigation_id = ReaderQueryHandler.get_investigation_id(dataset_id=self.where_filter_entity_id)
            if ReaderQueryHandler.is_user_allowed(
                user_name=user_name,
                investigation_id=investigation_id,
            ) or ReaderQueryHandler.is_dataset_open(dataset_id=self.where_filter_entity_id):
                log.debug("User is authorised to see dataset.id=%s", self.where_filter_entity_id)
                return True

        log.debug("User not authorised to see %s=%s", id_field, self.where_filter_entity_id)
        return False
