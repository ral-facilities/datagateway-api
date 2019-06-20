import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.constants import Constants
from common.exceptions import MissingRecordError, BadFilterError


def get_record_by_id(table, id):
    """
    Gets a row from the dummy data credential database
    :param table: the table class mapping
    :param id: the id to find
    :return: the row from the table
    """
    session = get_db_session()
    result = session.query(table).filter(table.ID == id).first()
    if result is not None:
        session.close()
        return result
    session.close()
    raise MissingRecordError()


def get_db_session():
    """
    Gets a session in the dummy data database, currently used for credentials until Authentication is understood
    :return: the dummy data DB session
    """
    engine = create_engine("mysql+pymysql://root:root@localhost:3306/icatdummy")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def get_icat_db_session():
    """
    Gets a session and connects with the ICAT database
    :return: the session object
    """
    engine = create_engine(Constants.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def insert_row_into_table(row):
    """
    Insert the given row into its table
    :param row: The row to be inserted
    """
    session = get_icat_db_session()
    session.add(row)
    session.commit()
    session.close()


def create_row_from_json(table, json):
    """
    Given a json dictionary create a row in the table from it
    :param table: the table for the row to be inserted into
    :param json: the dictionary containing the values
    :return: nothing atm
    """
    session = get_icat_db_session()
    record = table()
    record.update_from_dict(json)
    record.CREATE_TIME = datetime.datetime.now()  # These should probably change
    record.CREATE_ID = "user"
    record.MOD_TIME = datetime.datetime.now()
    record.MOD_ID = "user"
    session.add(record)
    session.commit()
    session.close()


def get_row_by_id(table, id):
    """
    Gets the row matching the given ID from the given table, raises MissingRecordError if it can not be found
    :param table: the table to be searched
    :param id: the id of the record to find
    :return: the record retrieved
    """
    session = get_icat_db_session()
    result = session.query(table).filter(table.ID == id).first()
    if result is not None:
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
    session = get_icat_db_session()
    result = get_row_by_id(table, id)
    if result is not None:
        session.delete(result)
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
    session = get_icat_db_session()
    record = session.query(table).filter(table.ID == id).first()
    if record is not None:
        record.update_from_dict(new_values)
        session.commit()
        session.close()
        return
    session.close()
    raise MissingRecordError()


def get_rows_by_filter(table, filters):
    session = get_icat_db_session()
    base_query = session.query(table)
    for filter in filters:
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
    session.close()
    return list(map(lambda x: x.to_dict(), base_query.all()))


def get_filtered_row_count(table, filters):
    """
    returns the count of the rows that match a given filter in a given table
    :param table: the table to be checked
    :param filters: the filters to be applied to the query
    :return: int: the count of the rows
    """
    return len(get_rows_by_filter(table, filters))


def get_first_filtered_row(table, filters):
    """
    returns the first row that matches a given filter, in a given table
    :param table: the table to be checked
    :param filters: the filter to be applied to the query
    :return: the first row matching the filter
    """
    return get_rows_by_filter(table, filters)[0]


def patch_entities(table, json_list):
    """
    Update one or more rows in the given table, from the given list containing json. Each entity must contain its ID
    :param table: The table of the entities
    :param json_list: the list of updated values
    :return: The list of updated rows.
    """
    results = []
    for entity in json_list:
        for key in entity:
            if key.upper() == "ID":
                update_row_from_id(table, entity[key], entity)
                result = get_row_by_id(table, entity[key])
                results.append(result)

    return results
