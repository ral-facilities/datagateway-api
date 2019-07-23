import datetime
import logging
from abc import ABC, abstractmethod

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

from common.constants import Constants
from common.exceptions import MissingRecordError, BadFilterError, BadRequestError

log = logging.getLogger()
# The session used throughout the database logic
_session = None


def get_icat_db_session():
    """
    Checks if there is a current session active and returns the session
    :return: the session object
    """
    global _session
    if _session is None:
        log.info(" Getting ICAT DB session")
        engine = create_engine(Constants.DATABASE_URL)
        Session = sessionmaker(bind=engine)
        _session = Session()
    return _session


class QueryFilterFactory(object):
    @staticmethod
    def get_query_filter(filter):
        """
        Given a filter return a matching QueryFilter object

        :param filter: dict - The filter to create the QueryFilter for
        :return: The QueryFilter object
        """
        filter_name = list(filter)[0]
        if filter_name == "where":
            return WhereFilter(list(filter["where"])[0], filter["where"][list(filter["where"])[0]])
        elif filter_name == "order":
            return OrderFilter(filter["order"].split(" ")[0], filter["order"].split(" ")[1])
        elif filter_name == "skip":
            return SkipFilter(filter["skip"])
        elif filter_name == "limit":
            return LimitFilter(filter["limit"])
        elif filter_name == "include":
            return IncludeFilter(filter)
        else:
            raise BadFilterError(f" Bad filter: {filter}")


class QueryFilter(ABC):
    @abstractmethod
    def apply_filter(self, query):
        pass


class WhereFilter(QueryFilter):
    def __init__(self, field, value):
        """

        :param field: Str - The field name to filter
        :param value: The value to match
        """
        self.field = field
        self.value = value

    def apply_filter(self, query):
        """
        Given a Query object, apply a where filter to it

        :param query: Query Object - The query to apply the filter to.
        """
        query.base_query = query.base_query.filter(getattr(query.table, self.field) == self.value)


class OrderFilter(QueryFilter):
    def __init__(self, field, direction):
        self.field = field
        self.direction = direction

    def apply_filter(self, query):
        if query.is_limited:
            query.base_query = query.base_query.from_self()
        if self.direction.upper() == "ASC":
            query.base_query = query.base_query.order_by(asc(getattr(query.table, self.field.upper())))
        elif self.direction.upper() == "DESC":
            query.base_query = query.base_query.order_by(desc(getattr(query.table, self.field.upper())))
        else:
            raise BadFilterError(f" Bad filter given: {self.direction}")


class LimitFilter(QueryFilter):
    def __init__(self, limit_value):
        self.limit_value = limit_value

    def apply_filter(self, query):
        query.base_query = query.base_query.limit(self.limit_value)
        query.is_limited = True


class SkipFilter(QueryFilter):
    def __init__(self, skip_value):
        self.skip_value = skip_value

    def apply_filter(self, query):
        query.base_query = query.base_query.offset(self.skip_value)

class Query(ABC):
    @abstractmethod
    def __init__(self, table):
        self.session = get_icat_db_session()
        self.table = table
        self.base_query = self.session.query(table)
        self.is_limited = False

    @abstractmethod
    def execute_query(self):
        pass

    def commit_changes(self):
        """
        Commits all changes made to the database and closes the active session
        """
        log.info(f" Committing changes to {self.table}")
        self.session.commit()
        log.info(f" Closing DB session")
        self.session.close()


class ReadQuery(Query):
    def __init__(self, table):
        super().__init__(table)

    def execute_query(self):
        self.commit_changes()

    def get_single_result(self):
        self.execute_query()
        if self.base_query.first() is not None:
            return self.base_query.first()
        raise MissingRecordError(" Could not find result")

    def get_all_results(self):
        self.execute_query()
        if self.base_query.all() is not None:
        return self.base_query.all()
        raise MissingRecordError(" No results found")


class CreateQuery(Query):
    def __init__(self, table, row):
        super().__init__(table)
        self.row = row

    def execute_query(self):
    """
        Determines if the row is in dictionary form or a row object and then commits it to the table

    """
        log.info(f" Inserting row into {self.table.__tablename__}")
        if type(self.row) is not dict:
            record = self.row
        else:
            record = self.table()
            record.update_from_dict(self.row)
            record.CREATE_TIME = datetime.datetime.now()
            record.MOD_TIME = datetime.datetime.now()
            record.CREATE_ID = "user"  # These will need changing
            record.MOD_ID = "user"
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
        self.commit_changes()


class DeleteQuery(Query):
    def __init__(self, table, row):
        super().__init__(table)
        self.row = row

    def execute_query(self):
        log.info(f" Deleting row {self.row}")
        self.session.delete(self.row)
        self.commit_changes()


class EntityManager(object):
    @staticmethod
def create_row_from_json(table, json):
    """
        Given a row in the form a dictionary, construct a CreateQuery and execute it

        :param table: - the table for the query to be run against
        :param json: - the row in dictionary form to be used in the query
        :return:
        """
        create_query = CreateQuery(table, json)
        create_query.execute_query()

    @staticmethod
    def insert_row_into_table(table, row):
        """
        Given a row and a table, construct a CreateQuery and execute it

        :param table: - the table for the query to be run against
        :param row:  - the row for the query to use
        """
        create_query = CreateQuery(table, row)
        create_query.execute_query()

    @staticmethod
    def get_row_by_id(table, id):
        """
        Given a table and id find the matching row

        :param table: The table to be searched
        :param id: The ID to find
        :return: The row
        """
        log.info(f" Querying {table.__tablename__} for record with ID: {id}")
        read_query = ReadQuery(table)
        where_filter = WhereFilter("ID", id)
        where_filter.apply_filter(read_query)
        return read_query.get_single_result()

    @staticmethod
def delete_row_by_id(table, id):
        """
        Given a table and ID, delete the matching row

        :param table: The table to be searched
        :param id: The ID to find
        """
        log.info(f" delete_row_by_id")
        row = EntityManager.get_row_by_id(table, id)
        delete_query = DeleteQuery(table, row)
        delete_query.execute_query()

    @staticmethod
def update_row_from_id(table, id, new_values):
        """
        Updates a record in a table
        :param table: The table the record is in
        :param id: The id of the record
        :param new_values: A JSON string containing what columns are to be updated
        """
        row = EntityManager.get_row_by_id(table, id)
        update_query = UpdateQuery(table, row, new_values)
        update_query.execute_query()

    @staticmethod
def get_rows_by_filter(table, filters):
        """
        Given a list of filters and a table, apply the filters to a query and return the results
        :param table: The table to be searched
        :param filters: list of dict - The filters to be applied
        :return: The returned rows
        """
        query = ReadQuery(table)
        qff = QueryFilterFactory()
    includes_relation = False
        for filter in filters:
            qff.get_query_filter(filter).apply_filter(query)
        results = query.get_all_results()
        if includes_relation:
            for query_filter in filters:
                if list(query_filter)[0] == "include":
                    return list(map(lambda x: x.to_nested_dict(query_filter["include"]), results))
        return list(map(lambda x: x.to_dict(), results))

    @staticmethod
def get_filtered_row_count(table, filters):
    """
    returns the count of the rows that match a given filter in a given table
    :param table: the table to be checked
    :param filters: the filters to be applied to the query
    :return: int: the count of the rows
    """
    log.info(f" Getting filtered row count for {table.__tablename__}")
    return len(EntityManager.get_rows_by_filter(table, filters))

    @staticmethod
def get_first_filtered_row(table, filters):
    """
    returns the first row that matches a given filter, in a given table
    :param table: the table to be checked
    :param filters: the filter to be applied to the query
    :return: the first row matching the filter
    """
    log.info(f" Getting first filtered row for {table.__tablename__}")
    return EntityManager.get_rows_by_filter(table, filters)[0]

    @staticmethod
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
                EntityManager.update_row_from_id(table, json_list[key], json_list)
                result = EntityManager.get_row_by_id(table, json_list[key])
                results.append(result)
    else:
        for entity in json_list:
            for key in entity:
                if key.upper() == "ID":
                    EntityManager.update_row_from_id(table, entity[key], entity)
                    result = EntityManager.get_row_by_id(table, entity[key])
                    results.append(result)
    if len(results) == 0:
        raise BadRequestError(f" Bad request made, request: {json_list}")

    return results
