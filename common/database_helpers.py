import datetime
import logging
from abc import ABC, abstractmethod

from sqlalchemy import asc, desc

from common.exceptions import MissingRecordError, BadFilterError, BadRequestError
from common.models.db_models import INVESTIGATIONUSER, INVESTIGATION, INSTRUMENT, FACILITYCYCLE
from common.session_manager import session_manager

log = logging.getLogger()


class Query(ABC):
    @abstractmethod
    def __init__(self, table):
        self.session = session_manager.get_icat_db_session()
        self.table = table
        self.base_query = self.session.query(table)

    @abstractmethod
    def execute_query(self):
        pass

    def commit_changes(self):
        """
        Commits all changes to the database and closes the session
        """
        log.info(f" Commiting changes to {self.table}")
        self.session.commit()
        log.info(f" Closing DB session")
        self.session.close()


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

    def commit_changes(self):
        log.info("Closing DB session")
        self.session.close()

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

    def execute_query(self):
        """Determines if the row is a row object or dictionary then commits it to the table"""
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


class UpdateQuery(Query):

    def __init__(self, table, row, new_values):
        super().__init__(table)
        self.row = row
        self.new_values = new_values

    def execute_query(self):
        log.info(f" Updating row in {self.table}")
        self.row.update_from_dict(self.new_values)
        self.session.add(self.row)
        self.commit_changes()


class DeleteQuery(Query):

    def __init__(self, table, row):
        super().__init__(table)
        self.row = row

    def execute_query(self):
        log.info(f" Deleting row {self.row} from {self.table.__tablename__}")
        self.session.delete(self.row)
        self.commit_changes()


class QueryFilter(ABC):
    @abstractmethod
    def apply_filter(self, query):
        pass


class WhereFilter(QueryFilter):
    precedence = 0

    def __init__(self, field, value, operation):
        self.field = field
        self.value = value
        self.operation = operation

    def apply_filter(self, query):
        table = self._get_table_to_filter(query)
        if self.operation == "eq":
            query.base_query = query.base_query.filter(getattr(table, self.field) == self.value)
        elif self.operation == "like":
            query.base_query = query.base_query.filter(getattr(table, self.field).like(f"%{self.value}%"))
        elif self.operation == "lte":
            query.base_query = query.base_query.filter(getattr(table, self.field) <= self.value)
        elif self.operation == "gte":
            query.base_query = query.base_query.filter(getattr(table, self.field) >= self.value)
        else:
            raise BadFilterError(f" Bad operation given to where filter. operation: {self.operation}")

    def _get_table_to_filter(self, query):
        if type(query) is UserInvestigationsQuery or type(query) is UserInvestigationsCountQuery:
            return INVESTIGATION
        else:
            return query.table


class OrderFilter(QueryFilter):
    precedence = 1

    def __init__(self, field, direction):
        self.field = field
        self.direction = direction

    def apply_filter(self, query):
        if self.direction.upper() == "ASC":
            query.base_query = query.base_query.order_by(asc(self.field.upper()))
        elif self.direction.upper() == "DESC":
            query.base_query = query.base_query.order_by(desc(self.field.upper()))
        else:
            raise BadFilterError(f" Bad filter: {self.direction}")


class SkipFilter(QueryFilter):
    precedence = 2

    def __init__(self, skip_value):
        self.skip_value = skip_value

    def apply_filter(self, query):
        query.base_query = query.base_query.offset(self.skip_value)


class LimitFilter(QueryFilter):
    precedence = 3

    def __init__(self, limit_value):
        self.limit_value = limit_value

    def apply_filter(self, query):
        query.base_query = query.base_query.limit(self.limit_value)


class IncludeFilter(QueryFilter):
    precedence = 4

    def __init__(self, included_filters):
        self.included_filters = included_filters

    def apply_filter(self, query):
        query.include_related_entities = True


class QueryFilterFactory(object):
    @staticmethod
    def get_query_filter(filter):
        """
        Given a filter return a matching Query filter object
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
        else:
            raise BadFilterError(f" Bad filter: {filter}")


class FilterOrderHandler(object):
    """
    The FilterOrderHandler takes in filters, sorts them according to the order of operations, then applies them.
    """

    def __init__(self):
        self.filters = []

    def add_filter(self, filter):
        self.filters.append(filter)

    def sort_filters(self):
        """
        Sorts the filters according to the order of operations
        """
        self.filters.sort(key=lambda x: x.precedence)

    def apply_filters(self, query):
        """
        Given a query apply the filters the handler has in the correct order.
        :param query: The query to have filters applied to
        """
        self.sort_filters()
        for filter in self.filters:
            filter.apply_filter(query)


def insert_row_into_table(table, row):
    """
    Insert the given row into its table
    :param table: The table to be inserted to
    :param row: The row to be inserted
    """
    create_query = CreateQuery(table, row)
    create_query.execute_query()


def create_row_from_json(table, json):
    """
    Given a json dictionary create a row in the table from it
    :param table: the table for the row to be inserted into
    :param json: the dictionary containing the values
    :return: nothing atm
    """
    create_query = CreateQuery(table, json)
    create_query.execute_query()


def get_row_by_id(table, id):
    """
    Gets the row matching the given ID from the given table, raises MissingRecordError if it can not be found
    :param table: the table to be searched
    :param id: the id of the record to find
    :return: the record retrieved
    """
    read_query = ReadQuery(table)
    try:
        log.info(f" Querying {table.__tablename__} for record with ID: {id}")
        where_filter = WhereFilter("ID", id, "eq")
        where_filter.apply_filter(read_query)
        return read_query.get_single_result()
    finally:
        read_query.session.close()


def delete_row_by_id(table, id):
    """
    Deletes the row matching the given ID from the given table, raises MissingRecordError if it can not be found
    :param table: the table to be searched
    :param id: the id of the record to delete
    """
    log.info(f" Deleting row from {table.__tablename__} with ID: {id}")
    row = get_row_by_id(table, id)
    delete_query = DeleteQuery(table, row)
    delete_query.execute_query()


def update_row_from_id(table, id, new_values):
    """
    Updates a record in a table
    :param table: The table the record is in
    :param id: The id of the record
    :param new_values: A JSON string containing what columns are to be updated
    """
    row = get_row_by_id(table, id)
    update_query = UpdateQuery(table, row, new_values)
    update_query.execute_query()


def get_filtered_read_query_results(filter_handler, filters, query):
    """
    Given a filter handler, list of filters and a query. Apply the filters and execute the query
    :param filter_handler: The filter handler to apply the filters
    :param filters: The filters to be applied
    :param query: The query for the filters to be applied to
    :return: The results of the query as a list of dictionaries
    """
    try:
        for query_filter in filters:
            if len(query_filter) == 0:
                pass
            else:
                filter_handler.add_filter(QueryFilterFactory.get_query_filter(query_filter))
        filter_handler.apply_filters(query)
        results = query.get_all_results()
        if query.include_related_entities:
            for query_filter in filters:
                if list(query_filter)[0].lower() == "include":
                    return list(map(lambda x: x.to_nested_dict(query_filter["include"]), results))
        return list(map(lambda x: x.to_dict(), results))

    finally:
        query.session.close()


def get_rows_by_filter(table, filters):
    """
    Given a list of filters supplied in json format, returns entities that match the filters from the given table
    :param table: The table to checked
    :param filters: The list of filters to be applied
    :return: A list of the rows returned in dictionary form
    """
    query = ReadQuery(table)
    filter_handler = FilterOrderHandler()
    return get_filtered_read_query_results(filter_handler, filters, query)


def get_first_filtered_row(table, filters):
    """
    returns the first row that matches a given filter, in a given table
    :param table: the table to be checked
    :param filters: the filter to be applied to the query
    :return: the first row matching the filter
    """
    log.info(f" Getting first filtered row for {table.__tablename__}")
    return get_rows_by_filter(table, filters)[0]


def get_filtered_row_count(table, filters):
    """
    returns the count of the rows that match a given filter in a given table
    :param table: the table to be checked
    :param filters: the filters to be applied to the query
    :return: int: the count of the rows
    """

    log.info(f" getting count for {table.__tablename__}")
    count_query = CountQuery(table)
    filter_handler = FilterOrderHandler()
    for query_filter in filters:
        if len(query_filter) == 0:
            pass
        else:
            filter_handler.add_filter(QueryFilterFactory.get_query_filter(query_filter))
    filter_handler.apply_filters(count_query)
    return count_query.get_count()


def patch_entities(table, json_list):
    """
    Update one or more rows in the given table, from the given list containing json. Each entity must contain its ID
    :param table: The table of the entities
    :param json_list: the list of updated values or a dictionary
    :return: The list of updated rows.
    """
    log.info(f" Patching entities in {table.__tablename__}")
    results = []
    if type(json_list) is dict:
        for key in json_list:
            if key.upper() == "ID":
                update_row_from_id(table, json_list[key], json_list)
                result = get_row_by_id(table, json_list[key])
                results.append(result)
    else:
        for entity in json_list:
            for key in entity:
                if key.upper() == "ID":
                    update_row_from_id(table, entity[key], entity)
                    result = get_row_by_id(table, entity[key])
                    results.append(result)
    if len(results) == 0:
        raise BadRequestError(f" Bad request made, request: {json_list}")

    return results


class UserInvestigationsQuery(ReadQuery):
    """
    The query class used for the /users/<:id>/investigations endpoint
    """

    def __init__(self, user_id):
        super().__init__(INVESTIGATIONUSER)
        self.base_query = self.base_query.join(INVESTIGATION).filter(INVESTIGATIONUSER.USER_ID == user_id)

    def get_all_results(self):
        return list(map(lambda x: x.INVESTIGATION, super().get_all_results()))

    def get_single_result(self):
        return list(map(lambda x: x.INVESTIGATION, super().get_single_result()))


def get_investigations_for_user(user_id, filters):
    """
    Given a user id and a list of filters, return a filtered list of all investigations that belong to that user
    :param user_id: The id of the user
    :param filters: The list of filters
    :return: A list of dictionary representations of the investigation entities
    """
    query = UserInvestigationsQuery(user_id)
    filter_handler = FilterOrderHandler()
    return get_filtered_read_query_results(filter_handler, filters, query)


class UserInvestigationsCountQuery(CountQuery):
    """
    The query class used for /users/<:id>/investigations/count
    """

    def __init__(self, user_id):
        super().__init__(INVESTIGATIONUSER)
        self.base_query = self.base_query.join(INVESTIGATION).filter(INVESTIGATIONUSER.USER_ID == user_id)


def get_investigations_for_user_count(user_id, filters):
    """
    Given a user id and a list of filters, return the count of all investigations that belong to that user
    :param user_id: The id of the user
    :param filters: The list of filters
    :return: The count
    """
    count_query = UserInvestigationsCountQuery(user_id)
    filter_handler = FilterOrderHandler()
    for query_filter in filters:
        if len(query_filter) == 0:
            pass
        else:
            filter_handler.add_filter(QueryFilterFactory.get_query_filter(query_filter))
    filter_handler.apply_filters(count_query)
    return count_query.get_count()


class InstrumentFacilityCyclesQuery(ReadQuery):
    def __init__(self, instrument_id):
        super().__init__(FACILITYCYCLE)
        self._get_start_and_end_date_filters(instrument_id)

    def _get_start_and_end_date_filters(self, instrument_id):
        """
        Given an instrument ID, get the start_date and end_date filters that will be applied to the query
        :param instrument_id: the id of the instrument
        :return:
        """
        investigations = self._get_investigations_for_instrument(instrument_id)
        start_date = datetime.datetime(3000, 1, 1)
        end_date = datetime.datetime(1, 1, 1)
        for investigation in investigations:
            if investigation.STARTDATE < start_date:
                start_date = investigation.STARTDATE
            if investigation.ENDDATE > end_date:
                end_date = investigation.ENDDATE
        self.start_date_filter = WhereFilter("STARTDATE", start_date, "gte")
        self.end_date_filter = WhereFilter("STARTDATE", end_date, "lte")

    @staticmethod
    def _get_investigations_for_instrument(instrument_id):
        """
        Given an instrument id get a list of investigation entities that use the given instrument
        :param instrument_id: - The Id of the instrument
        :return: The list of investigation entities
        """
        instrument = get_row_by_id(INSTRUMENT, instrument_id)
        session = session_manager.get_icat_db_session()
        try:
            session.add(instrument)
            investigations = [i.INVESTIGATION for i in instrument.INVESTIGATIONINSTRUMENT]
        finally:
            session.close()
        return investigations


def get_facility_cycles_for_instrument(instrument_id, filters):
    """
    Given an instrument_id get facility cycles where the instrument has investigations that occur within that cycle
    :param filters: The filters to be applied to the query
    :param instrument_id: The id of the instrument
    :return: A list of facility cycle entities
    """
    query = InstrumentFacilityCyclesQuery(instrument_id)
    filter_handler = FilterOrderHandler()
    filter_handler.add_filter(query.start_date_filter)
    filter_handler.add_filter(query.end_date_filter)
    return get_filtered_read_query_results(filter_handler, filters, query)


def get_facility_cycles_for_instrument_count(instrument_id, filters):
    """
    Given an instrument_id get the facility cycles count where the instrument has investigations that occur within
    that cycle
    :param filters: The filters to be applied to the query
    :param instrument_id: The id of the instrument
    :return: The count of the facility cycles
    """
    return len(get_facility_cycles_for_instrument(instrument_id, filters))


class InstrumentFacilityCycleInvestigationsQuery(ReadQuery):
    def __init__(self, instrument_id, facility_cycle_id):
        super().__init__(INVESTIGATION)
        self.instrument_id = instrument_id
        self.facility_cycle_id = facility_cycle_id
        self._get_date_filters()

    def _get_date_filters(self):
        """
        Sets the date filters to be applied to the query
        """
        self.start_date_filter = WhereFilter("STARTDATE", self._get_facility_cycle()["STARTDATE"], "gte")
        self.end_date_filter = WhereFilter("STARTDATE", self._get_facility_cycle()["ENDDATE"], "lte")

    def _get_facility_cycle(self):
        """
        Given a facility cycle_id and instrument_id, get the facility cycle that has an investigation using the given
        instrument in the cycle
        :return: The facility cycle
        """
        facility_cycles = get_facility_cycles_for_instrument(self.instrument_id, filters=[])
        try:
            #  The ID value gets previously converted to str
            return [cycle for cycle in facility_cycles if cycle["ID"] == str(self.facility_cycle_id)][0]
        except IndexError:
            raise MissingRecordError()


def get_investigations_for_instrument_in_facility_cycle(instrument_id, facility_cycle_id, filters):
    """
    Given an instrument id and facility cycle id, get investigations that use the given instrument in the given cycle
    :param filters: The filters to be applied to the query
    :param instrument_id: The id of the instrument
    :param facility_cycle_id:  the ID of the facility cycle
    :return: The investigations
    """
    filter_handler = FilterOrderHandler()
    query = InstrumentFacilityCycleInvestigationsQuery(instrument_id, facility_cycle_id)
    filter_handler.add_filter(query.end_date_filter)
    filter_handler.add_filter(query.start_date_filter)
    return get_filtered_read_query_results(filter_handler, filters, query)


def get_investigations_for_instrument_in_facility_cycle_count(instrument_id, facility_cycle_id, filters):
    """
    Given an instrument id and facility cycle id, get the count of the investigations that use the given instrument in
    the given cycle
    :param filters: The filters to be applied to the query
    :param instrument_id: The id of the instrument
    :param facility_cycle_id:  the ID of the facility cycle
    :return: The investigations count
    """
    return len(get_investigations_for_instrument_in_facility_cycle(instrument_id, facility_cycle_id, filters))
