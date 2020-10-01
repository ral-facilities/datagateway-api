import datetime
import logging
from abc import ABC, abstractmethod
from functools import wraps

from sqlalchemy.orm import aliased

from common.exceptions import (
    ApiError,
    AuthenticationError,
    MissingRecordError,
    FilterError,
    BadRequestError,
    MultipleIncludeError,
)
from common.models import db_models
from common.models.db_models import (
    INVESTIGATIONUSER,
    INVESTIGATION,
    INSTRUMENT,
    FACILITYCYCLE,
    INVESTIGATIONINSTRUMENT,
    FACILITY,
    SESSION,
)
from common.session_manager import session_manager
from common.filter_order_handler import FilterOrderHandler
from common.config import config

backend_type = config.get_backend_type()
if backend_type == "db":
    from common.database.filters import (
        DatabaseWhereFilter as WhereFilter,
        DatabaseDistinctFieldFilter as DistinctFieldFilter,
        DatabaseOrderFilter as OrderFilter,
        DatabaseSkipFilter as SkipFilter,
        DatabaseLimitFilter as LimitFilter,
        DatabaseIncludeFilter as IncludeFilter,
    )
elif backend_type == "python_icat":
    from common.icat.filters import (
        PythonICATWhereFilter as WhereFilter,
        PythonICATDistinctFieldFilter as DistinctFieldFilter,
        PythonICATOrderFilter as OrderFilter,
        PythonICATSkipFilter as SkipFilter,
        PythonICATLimitFilter as LimitFilter,
        PythonICATIncludeFilter as IncludeFilter,
    )
else:
    raise ApiError(
        "Cannot select which implementation of filters to import, check the config file"
        " has a valid backend type"
    )

log = logging.getLogger()


def requires_session_id(method):
    """
    Decorator for database backend methods that makes sure a valid session_id is
    provided. It expects that session_id is the second argument supplied to the function

    :param method: The method for the backend operation
    :raises AuthenticationError, if a valid session_id is not provided with the request
    """

    @wraps(method)
    def wrapper_requires_session(*args, **kwargs):
        log.info(" Authenticating consumer")
        session = session_manager.get_icat_db_session()
        query = session.query(SESSION).filter(SESSION.ID == args[1]).first()
        if query is not None:
            log.info(" Closing DB session")
            session.close()
            session.close()
            log.info(" Consumer authenticated")
            return method(*args, **kwargs)
        else:
            log.info(" Could not authenticate consumer, closing DB session")
            session.close()
            raise AuthenticationError("Forbidden")

    return wrapper_requires_session


class Query(ABC):
    """
    The base query class that all other queries extend from. This defines the enter and
    exit methods, used to handle sessions. It is expected that all queries would be used
    with the 'with' keyword in most cases for this reason.
    """

    @abstractmethod
    def __init__(self, table):
        self.session = session_manager.get_icat_db_session()
        self.table = table
        self.base_query = self.session.query(table)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        log.info("Closing DB session")
        self.session.close()

    @abstractmethod
    def execute_query(self):
        pass

    def commit_changes(self):
        """
        Commits all changes to the database and closes the session
        """
        log.info(" Committing changes to %s", self.table)
        self.session.commit()


class CountQuery(Query):
    def __init__(self, table):
        super().__init__(table)
        self.include_related_entities = False

    def execute_query(self):
        self.commit_changes()

    def get_count(self):
        try:
            return self.base_query.count()
        finally:
            self.execute_query()


class ReadQuery(Query):
    def __init__(self, table):
        super().__init__(table)
        self.include_related_entities = False
        self.is_distinct_fields_query = False

    def commit_changes(self):
        log.info("Closing DB session")

    def execute_query(self):
        self.commit_changes()

    def get_single_result(self):
        result = self.base_query.first()
        if result is not None:
            return result
        raise MissingRecordError(" No result found")

    def get_all_results(self):
        results = self.base_query.all()
        if results is not None:
            return results
        raise MissingRecordError(" No results found")


class CreateQuery(Query):
    def __init__(self, table, row):
        super().__init__(table)
        self.row = row
        self.inserted_row = None

    def execute_query(self):
        """
        Determines if the row is a row object or dictionary then commits it to the table
        """
        if type(self.row) is not dict:
            record = self.row
        else:
            record = self.table()
            record.update_from_dict(self.row)
            record.CREATE_TIME = datetime.datetime.now()
            record.MOD_TIME = datetime.datetime.now()
            record.CREATE_ID = "user"
            record.MOD_ID = "user"  # These will need changing
        self.session.add(record)
        self.commit_changes()
        self.session.refresh(record)
        self.inserted_row = record


class UpdateQuery(Query):
    def __init__(self, table, row, new_values):
        super().__init__(table)
        self.row = row
        self.new_values = new_values

    def execute_query(self):
        log.info(" Updating row in %s", self.table)
        self.row.update_from_dict(self.new_values)
        self.session.add(self.row)
        self.commit_changes()


class DeleteQuery(Query):
    def __init__(self, table, row):
        super().__init__(table)
        self.row = row

    def execute_query(self):
        log.info(" Deleting row %s from %s", self.row, self.table.__tablename__)
        self.session.delete(self.row)
        self.commit_changes()


class QueryFilterFactory(object):
    @staticmethod
    def get_query_filter(filter):
        """
        Given a filter return a matching Query filter object

        This factory is not in common.filters so the created filter can be for the
        correct backend. Moving the factory into that file would mean the filters would
        be based off the abstract classes (because they're in the same file) which won't
        enable filters to be unique to the backend

        :param filter: dict - The filter to create the QueryFilter for
        :return: The QueryFilter object created
        """
        filter_name = list(filter)[0].lower()
        if filter_name == "where":
            field = list(filter[filter_name].keys())[0]
            operation = list(filter[filter_name][field].keys())[0]
            value = filter[filter_name][field][operation]
            return WhereFilter(field, value, operation)
        elif filter_name == "order":
            field = filter["order"].split(" ")[0]
            direction = filter["order"].split(" ")[1]
            return OrderFilter(field, direction)
        elif filter_name == "skip":
            return SkipFilter(filter["skip"])
        elif filter_name == "limit":
            return LimitFilter(filter["limit"])
        elif filter_name == "include":
            return IncludeFilter(filter)
        elif filter_name == "distinct":
            return DistinctFieldFilter(filter["distinct"])
        else:
            raise FilterError(f" Bad filter: {filter}")


def insert_row_into_table(table, row):
    """
    Insert the given row into its table
    :param table: The table to be inserted to
    :param row: The row to be inserted
    """
    with CreateQuery(table, row) as create_query:
        create_query.execute_query()


def create_row_from_json(table, data):
    """
    Given a json dictionary create a row in the table from it
    :param table: the table for the row to be inserted into
    :param data: the dictionary containing the values
    :return: The inserted row as a dictionary
    """
    with CreateQuery(table, data) as create_query:
        create_query.execute_query()
        return create_query.inserted_row.to_dict()


def create_rows_from_json(table, data):
    """
    Given a List containing dictionary representations of entities, or a dictionary
    representation of an entity, insert the entities into the table and return the
    created entities

    :param table: The table to insert the entities in
    :param data: The entities to be inserted
    :return: The inserted entities
    """
    if type(data) is list:
        return [create_row_from_json(table, entity) for entity in data]
    return create_row_from_json(table, data)


def get_row_by_id(table, id_):
    """
    Gets the row matching the given ID from the given table, raises MissingRecordError
    if it can not be found

    :param table: the table to be searched
    :param id_: the id of the record to find
    :return: the record retrieved
    """
    with ReadQuery(table) as read_query:
        log.info(" Querying %s for record with ID: %d", table.__tablename__, id_)
        where_filter = WhereFilter("ID", id_, "eq")
        where_filter.apply_filter(read_query)
        return read_query.get_single_result()


def delete_row_by_id(table, id_):
    """
    Deletes the row matching the given ID from the given table, raises
    MissingRecordError if it can not be found

    :param table: the table to be searched
    :param id_: the id of the record to delete
    """
    log.info(" Deleting row from %s with ID: %d", table.__tablename__, id_)
    row = get_row_by_id(table, id_)
    with DeleteQuery(table, row) as delete_query:
        delete_query.execute_query()


def update_row_from_id(table, id_, new_values):
    """
    Updates a record in a table

    :param table: The table the record is in
    :param id_: The id of the record
    :param new_values: A JSON string containing what columns are to be updated
    """
    row = get_row_by_id(table, id_)
    with UpdateQuery(table, row, new_values) as update_query:
        update_query.execute_query()


def get_filtered_read_query_results(filter_handler, filters, query):
    """
    Given a filter handler, list of filters and a query. Apply the filters and execute
    the query

    :param filter_handler: The filter handler to apply the filters
    :param filters: The filters to be applied
    :param query: The query for the filters to be applied to
    :return: The results of the query as a list of dictionaries
    """
    filter_handler.add_filters(filters)
    filter_handler.apply_filters(query)
    results = query.get_all_results()
    if query.is_distinct_fields_query:
        return _get_distinct_fields_as_dicts(results)
    if query.include_related_entities:
        return _get_results_with_include(filters, results)
    return list(map(lambda x: x.to_dict(), results))


def _get_results_with_include(filters, results):
    """
    Given a list of entities and a list of filters, use the include filter to nest the
    included entities requested in the include filter given

    :param filters: The list of filters
    :param results: The list of entities
    :return: A list of nested dictionaries representing the entity results
    """
    for query_filter in filters:
        if type(query_filter) is IncludeFilter:
            return [x.to_nested_dict(query_filter.included_filters) for x in results]


def _get_distinct_fields_as_dicts(results):
    """
    Given a list of column results return a list of dictionaries where each column name
    is the key and the column value is the dictionary key value

    :param results: A list of sql alchemy result objects
    :return: A list of dictionary representations of the sqlalchemy result objects
    """
    dictionaries = []
    for result in results:
        dictionary = {k: getattr(result, k) for k in result.keys()}
        dictionaries.append(dictionary)
    return dictionaries


def get_rows_by_filter(table, filters):
    """
    Given a list of filters supplied in json format, returns entities that match the
    filters from the given table

    :param table: The table to checked
    :param filters: The list of filters to be applied
    :return: A list of the rows returned in dictionary form
    """
    with ReadQuery(table) as query:
        filter_handler = FilterOrderHandler()
        return get_filtered_read_query_results(filter_handler, filters, query)


def get_first_filtered_row(table, filters):
    """
    returns the first row that matches a given filter, in a given table
    :param table: the table to be checked
    :param filters: the filter to be applied to the query
    :return: the first row matching the filter
    """
    log.info(" Getting first filtered row for %s", table.__tablename__)
    return get_rows_by_filter(table, filters)[0]


def get_filtered_row_count(table, filters):
    """
    returns the count of the rows that match a given filter in a given table
    :param table: the table to be checked
    :param filters: the filters to be applied to the query
    :return: int: the count of the rows
    """

    log.info(" getting count for %s", table.__tablename__)
    with CountQuery(table) as count_query:
        filter_handler = FilterOrderHandler()
        filter_handler.add_filters(filters)
        filter_handler.apply_filters(count_query)
        return count_query.get_count()


def patch_entities(table, json_list):
    """
    Update one or more rows in the given table, from the given list containing json.
    Each entity must contain its ID

    :param table: The table of the entities
    :param json_list: the list of updated values or a dictionary
    :return: The list of updated rows.
    """
    log.info(" Patching entities in %s", table.__tablename__)
    results = []
    if type(json_list) is dict:
        for key in json_list:
            if key.upper() == "ID":
                update_row_from_id(table, json_list[key], json_list)
                result = get_row_by_id(table, json_list[key])
                results.append(result.to_dict())
    else:
        for entity in json_list:
            for key in entity:
                if key.upper() == "ID":
                    update_row_from_id(table, entity[key], entity)
                    result = get_row_by_id(table, entity[key])
                    results.append(result.to_dict())
    if len(results) == 0:
        raise BadRequestError(f" Bad request made, request: {json_list}")

    return results


class InstrumentFacilityCyclesQuery(ReadQuery):
    def __init__(self, instrument_id):
        super().__init__(FACILITYCYCLE)
        investigation_instrument = aliased(INSTRUMENT)
        self.base_query = (
            self.base_query.join(FACILITYCYCLE.FACILITY)
            .join(FACILITY.INSTRUMENT)
            .join(FACILITY.INVESTIGATION)
            .join(INVESTIGATION.INVESTIGATIONINSTRUMENT)
            .join(investigation_instrument, INVESTIGATIONINSTRUMENT.INSTRUMENT)
            .filter(INSTRUMENT.ID == instrument_id)
            .filter(investigation_instrument.ID == INSTRUMENT.ID)
            .filter(INVESTIGATION.STARTDATE >= FACILITYCYCLE.STARTDATE)
            .filter(INVESTIGATION.STARTDATE <= FACILITYCYCLE.ENDDATE)
        )


def get_facility_cycles_for_instrument(instrument_id, filters):
    """
    Given an instrument_id get facility cycles where the instrument has investigations
    that occur within that cycle

    :param filters: The filters to be applied to the query
    :param instrument_id: The id of the instrument
    :return: A list of facility cycle entities
    """
    with InstrumentFacilityCyclesQuery(instrument_id) as query:
        filter_handler = FilterOrderHandler()
        return get_filtered_read_query_results(filter_handler, filters, query)


class InstrumentFacilityCyclesCountQuery(CountQuery):
    def __init__(self, instrument_id):
        super().__init__(FACILITYCYCLE)
        investigation_instrument = aliased(INSTRUMENT)
        self.base_query = (
            self.base_query.join(FACILITYCYCLE.FACILITY)
            .join(FACILITY.INSTRUMENT)
            .join(FACILITY.INVESTIGATION)
            .join(INVESTIGATION.INVESTIGATIONINSTRUMENT)
            .join(investigation_instrument, INVESTIGATIONINSTRUMENT.INSTRUMENT)
            .filter(INSTRUMENT.ID == instrument_id)
            .filter(investigation_instrument.ID == INSTRUMENT.ID)
            .filter(INVESTIGATION.STARTDATE >= FACILITYCYCLE.STARTDATE)
            .filter(INVESTIGATION.STARTDATE <= FACILITYCYCLE.ENDDATE)
        )


def get_facility_cycles_for_instrument_count(instrument_id, filters):
    """
    Given an instrument_id get the facility cycles count where the instrument has
    investigations that occur within that cycle

    :param filters: The filters to be applied to the query
    :param instrument_id: The id of the instrument
    :return: The count of the facility cycles
    """
    with InstrumentFacilityCyclesCountQuery(instrument_id) as query:
        filter_handler = FilterOrderHandler()
        filter_handler.add_filters(filters)
        filter_handler.apply_filters(query)
        return query.get_count()


class InstrumentFacilityCycleInvestigationsQuery(ReadQuery):
    def __init__(self, instrument_id, facility_cycle_id):
        super().__init__(INVESTIGATION)
        investigation_instrument = aliased(INSTRUMENT)
        self.base_query = (
            self.base_query.join(INVESTIGATION.FACILITY)
            .join(FACILITY.FACILITYCYCLE)
            .join(FACILITY.INSTRUMENT)
            .join(INVESTIGATION.INVESTIGATIONINSTRUMENT)
            .join(investigation_instrument, INVESTIGATIONINSTRUMENT.INSTRUMENT)
            .filter(INSTRUMENT.ID == instrument_id)
            .filter(FACILITYCYCLE.ID == facility_cycle_id)
            .filter(investigation_instrument.ID == INSTRUMENT.ID)
            .filter(INVESTIGATION.STARTDATE >= FACILITYCYCLE.STARTDATE)
            .filter(INVESTIGATION.STARTDATE <= FACILITYCYCLE.ENDDATE)
        )


def get_investigations_for_instrument_in_facility_cycle(
    instrument_id, facility_cycle_id, filters
):
    """
    Given an instrument id and facility cycle id, get investigations that use the given
    instrument in the given cycle

    :param filters: The filters to be applied to the query
    :param instrument_id: The id of the instrument
    :param facility_cycle_id:  the ID of the facility cycle
    :return: The investigations
    """
    filter_handler = FilterOrderHandler()
    with InstrumentFacilityCycleInvestigationsQuery(
        instrument_id, facility_cycle_id
    ) as query:
        return get_filtered_read_query_results(filter_handler, filters, query)


class InstrumentFacilityCycleInvestigationsCountQuery(CountQuery):
    def __init__(self, instrument_id, facility_cycle_id):
        super().__init__(INVESTIGATION)
        investigation_instrument = aliased(INSTRUMENT)
        self.base_query = (
            self.base_query.join(INVESTIGATION.FACILITY)
            .join(FACILITY.FACILITYCYCLE)
            .join(FACILITY.INSTRUMENT)
            .join(INVESTIGATION.INVESTIGATIONINSTRUMENT)
            .join(investigation_instrument, INVESTIGATIONINSTRUMENT.INSTRUMENT)
            .filter(INSTRUMENT.ID == instrument_id)
            .filter(FACILITYCYCLE.ID == facility_cycle_id)
            .filter(investigation_instrument.ID == INSTRUMENT.ID)
            .filter(INVESTIGATION.STARTDATE >= FACILITYCYCLE.STARTDATE)
            .filter(INVESTIGATION.STARTDATE <= FACILITYCYCLE.ENDDATE)
        )


def get_investigations_for_instrument_in_facility_cycle_count(
    instrument_id, facility_cycle_id, filters
):
    """
    Given an instrument id and facility cycle id, get the count of the investigations
    that use the given instrument in the given cycle

    :param filters: The filters to be applied to the query
    :param instrument_id: The id of the instrument
    :param facility_cycle_id:  the ID of the facility cycle
    :return: The investigations count
    """
    with InstrumentFacilityCycleInvestigationsCountQuery(
        instrument_id, facility_cycle_id
    ) as query:
        filter_handler = FilterOrderHandler()
        filter_handler.add_filters(filters)
        filter_handler.apply_filters(query)
        return query.get_count()
