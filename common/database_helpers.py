import datetime
import logging
from abc import ABC, abstractmethod

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

from common.constants import Constants
from common.exceptions import MissingRecordError, BadFilterError, BadRequestError

log = logging.getLogger()

_session = None


def get_icat_db_session():
    """
    Gets a session and connects with the ICAT database
    :return: the session object
    """
    global _session
    if _session is None:
        log.info(" Getting ICAT DB session")
        engine = create_engine(Constants.DATABASE_URL)
        Session = sessionmaker(bind=engine)
        _session = Session()
    return _session


class QueryFilter(ABC):
    @abstractmethod
    def apply_filter(self, query):
        pass


class WhereFilter(QueryFilter):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def apply_filter(self, query):
        """
        Given a Query object, apply a where filter to it

        :param query: Query Object - The query to apply the filter to.
        """
        query.base_query = query.base_query.filter(getattr(query.table, self.field.upper()) == self.value)
        return


class Query(ABC):
    @abstractmethod
    def __init__(self, table):
        self.session = get_icat_db_session()
        self.table = table
        self.base_query = self.session.query(table)

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


class FilteredQuery(Query):
    pass


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
        return self.base_query.all()


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
            print("here")
            record = self.table()
            record.update_from_dict(self.row)
            record.CREATE_TIME = datetime.datetime.now()
            record.MOD_TIME = datetime.datetime.now()
            record.CREATE_ID = "user"  # These will need changing
            record.MOD_ID = "user"
        self.session.add(record)
        self.commit_changes()


class UpdateQuery(FilteredQuery):
    def __init__(self, table, row, new_values):
        super().__init__(table)
        self.row = row
        self.new_values = new_values

    def execute_query(self):
        log.info(f" Updating row in {self.table}")
        self.row.update_from_dict(self.new_values)
        self.commit_changes()


class DeleteQuery(FilteredQuery):
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
        log.info(f" Querying {table.__tablename__} for record with ID: {id}")
        read_query = ReadQuery(table)
        where_filter = WhereFilter("ID", id)
        where_filter.apply_filter(read_query)
        return read_query.get_single_result()

    @staticmethod
def delete_row_by_id(table, id):
        row = EntityManager.get_row_by_id(table, id)
        delete_query = DeleteQuery(table, row)
        delete_query.execute_query()

    @staticmethod
def update_row_from_id(table, id, new_values):
        row = EntityManager.get_row_by_id(table, id)
        update_query = UpdateQuery(table, row, new_values)
        update_query.execute_query()


def get_rows_by_filter(table, filters):
    """
    Given a list of filters supplied in json format, returns entities that match the filters from the given table
    :param table: The table to checked
    :param filters: The list of filters to be applied
    :return: A list of the rows returned in dictionary form
    """
    is_limited = False
    session = get_icat_db_session()
    base_query = session.query(table)
    includes_relation = False
    for query_filter in filters:
        if len(query_filter) == 0:
            pass
        elif list(query_filter)[0].lower() == "where":
            for key in query_filter:
                where_part = query_filter[key]
                for k in where_part:
                    column = getattr(table, k.upper())
                    base_query = base_query.filter(column.in_([where_part[k]]), column.in_([where_part[k]]))
        elif list(query_filter)[0].lower() == "order":
            for key in query_filter:
                field = query_filter[key].split(" ")[0]
                direction = query_filter[key].split(" ")[1]
                # Limit then order, or order then limit
            if is_limited:
                if direction.upper() == "ASC":
                    base_query = base_query.from_self().order_by(asc(getattr(table, field)))
                elif direction.upper() == "DESC":
                    base_query = base_query.from_self().order_by(desc(getattr(table, field)))
                else:
                    raise BadFilterError(f" Bad filter given, filter: {query_filter}")
            else:
                if direction.upper() == "ASC":
                    base_query = base_query.order_by(asc(getattr(table, field)))
                elif direction.upper() == "DESC":
                    base_query = base_query.order_by(desc(getattr(table, field)))
                else:
                    raise BadFilterError(f" Bad filter given, filter: {query_filter}")

        elif list(query_filter)[0].lower() == "skip":
            for key in query_filter:
                skip = query_filter[key]
            base_query = base_query.offset(skip)

        elif list(query_filter)[0].lower() == "limit":
            is_limited = True
            for key in query_filter:
                query_limit = query_filter[key]
            base_query = base_query.limit(query_limit)
        elif list(query_filter)[0].lower() == "include":
            includes_relation = True

        else:
            raise BadFilterError(f"Invalid filters provided received {filters}")

    results = base_query.all()
    # check if include was provided, then add included results
    if includes_relation:
        log.info(" Closing DB session")
        for query_filter in filters:
            if list(query_filter)[0] == "include":
                return list(map(lambda x: x.to_nested_dict(query_filter["include"]), results))

    log.info(" Closing DB session")
    session.close()
    return list(map(lambda x: x.to_dict(), results))


def get_filtered_row_count(table, filters):
    """
    returns the count of the rows that match a given filter in a given table
    :param table: the table to be checked
    :param filters: the filters to be applied to the query
    :return: int: the count of the rows
    """
    log.info(f" Getting filtered row count for {table.__tablename__}")
    return len(get_rows_by_filter(table, filters))


def get_first_filtered_row(table, filters):
    """
    returns the first row that matches a given filter, in a given table
    :param table: the table to be checked
    :param filters: the filter to be applied to the query
    :return: the first row matching the filter
    """
    log.info(f" Getting first filtered row for {table.__tablename__}")
    return get_rows_by_filter(table, filters)[0]


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
