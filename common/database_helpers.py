import datetime
import logging

from sqlalchemy import create_engine
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
    raise MissingRecordError()


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
    raise MissingRecordError()


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
    raise MissingRecordError()


def get_rows_by_filter(table, filters):
    session = get_icat_db_session()
    base_query = session.query(table)
    for filter in filters:
        if len(filter) == 0:
            raise BadFilterError()
        if list(filter)[0].lower() == "where":
            for key in filter:
                where_part = filter[key]
                for k in where_part:
                    column = getattr(table, k.upper())
                    base_query = base_query.filter(column.in_([where_part[k]]))

        elif list(filter)[0].lower() == "order":
            base_query.order()  # do something probably not .order
        elif list(filter)[0].lower() == "skip":
            for key in filter:
                skip = filter[key]
            base_query = base_query.offset(skip)
        elif list(filter)[0].lower() == "include":
            base_query.include()  # do something probably not .include
        elif list(filter)[0].lower() == "limit":
            for key in filter:
                limit = filter[key]
            base_query = base_query.limit(limit)
        else:
            raise BadFilterError()
    log.info(" Closing DB session")
    session.close()
    return list(map(lambda x: x.to_dict(), base_query.all()))


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
        raise BadRequestError()

    return results
