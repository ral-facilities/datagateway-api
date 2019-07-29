import datetime
import logging
from abc import ABC, abstractmethod

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

from common.constants import Constants
from common.exceptions import MissingRecordError, BadFilterError, BadRequestError

log = logging.getLogger()


def get_icat_db_session():
    """
    Gets a session and connects with the ICAT database
    :return: the session object
    """
    log.info(" Getting ICAT DB session")
    engine = create_engine(Constants.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


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
        Commits all changes to the database and closes the session
        """
        log.info(f" Commiting changes to {self.table}")
        self.session.commit()
        log.info(f" Closing DB session")
        self.session.close()


class ReadQuery(Query):

    def __init__(self, table):
        super.__init__(table)
        self.include_related_entities = False

    def execute_query(self):
        self.commit_changes()

    def get_single_result(self):
        self.execute_query()
        if self.base_query.first() is not None:
            return self.base_query.first()
        raise MissingRecordError(" No result found")

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
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def apply_filter(self, query):
        query.base_query = query.base_query.filter(getattr(query.table, self.field) == self.value)


class OrderFilter(QueryFilter):
    def __init__(self, field, direction):
        self.field = field
        self.direction = direction

    def apply_filter(self, query):
        if query.is_limited:
            query.base_query = query.base_query.from_self()
        if self.direction.upper() == "ASC":
            query.base_query = query.base_query.order_by(asc(query.table, self.field.upper()))
        elif self.direction.upper() == "DESC":
            query.base_query = query.base_query.order_by(desc(query.table, self.field.upper()))
        else:
            raise BadFilterError(f" Bad filter: {self.direction}")


class SkipFilter(QueryFilter):
    def __init__(self, skip_value):
        self.skip_value = skip_value
    
    def apply_filter(self, query):
        query.base_query = query.base_query.offset(self.skip_value)


class LimitFilter(QueryFilter):
    def __init__(self, limit_value):
        self.limit_value = limit_value

    def apply_filter(self, query):
        query.base_query = query.base_query.limit(self.limit_value)
        query.is_limited = True


class IncludeFilter(QueryFilter):
    def __init__(self, included_filters):
        self.included_filters = included_filters

    def apply_filter(self, query):
        query.include_related_entities = True


def insert_row_into_table(row):
    """
    Insert the given row into its table
    :param row: The row to be inserted
    """
    log.info(f" Inserting row into table {row.__tablename__}")
    session = get_icat_db_session()
    session.add(row)
    session.commit()
    log.info(" Closing DB session")
    session.close()


def create_row_from_json(table, json):
    """
    Given a json dictionary create a row in the table from it
    :param table: the table for the row to be inserted into
    :param json: the dictionary containing the values
    :return: nothing atm
    """
    log.info(f" Creating row from json into table {table.__tablename__}")
    session = get_icat_db_session()
    record = table()
    record.update_from_dict(json)
    record.CREATE_TIME = datetime.datetime.now()  # These should probably change
    record.CREATE_ID = "user"
    record.MOD_TIME = datetime.datetime.now()
    record.MOD_ID = "user"
    session.add(record)
    session.commit()
    log.info(" Closing db session")
    session.close()


def get_row_by_id(table, id):
    """
    Gets the row matching the given ID from the given table, raises MissingRecordError if it can not be found
    :param table: the table to be searched
    :param id: the id of the record to find
    :return: the record retrieved
    """
    log.info(f" Querying {table.__tablename__} for record with ID: {id}")
    session = get_icat_db_session()
    result = session.query(table).filter(table.ID == id).first()
    if result is not None:
        log.info(" Record found, closing DB session")
        session.close()
        return result
    session.close()
    raise MissingRecordError(f" Could not find record in {table.__tablename__} with ID: {id}")


def delete_row_by_id(table, id):
    """
    Deletes the row matching the given ID from the given table, raises MissingRecordError if it can not be found
    :param table: the table to be searched
    :param id: the id of the record to delete
    """
    log.info(f" Deleting row from {table.__tablename__} with ID: {id}")
    session = get_icat_db_session()
    result = get_row_by_id(table, id)
    if result is not None:
        session.delete(result)
        log.info(" record deleted, closing DB session")
        session.commit()
        session.close()
        return
    session.close()
    raise MissingRecordError(f" Could not find record in {table.__tablename__} with ID: {id}")


def update_row_from_id(table, id, new_values):
    """
    Updates a record in a table
    :param table: The table the record is in
    :param id: The id of the record
    :param new_values: A JSON string containing what columns are to be updated
    """
    log.info(f" Updating row with ID: {id} in {table.__tablename__}")
    session = get_icat_db_session()
    record = session.query(table).filter(table.ID == id).first()
    if record is not None:
        record.update_from_dict(new_values)
        session.commit()
        log.info(" Record updated, closing DB session")
        session.close()
        return
    session.close()
    raise MissingRecordError(f" Could not find record in {table.__tablename__} with ID: {id}")


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
                    base_query = base_query.filter(column.in_([where_part[k]]))
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
