import datetime
import logging

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.collections import InstrumentedList

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
    for filter in filters:
        if list(filter)[0].lower() == "where":
            for key in filter:
                where_part = filter[key]
                for k in where_part:
                    column = getattr(table, k.upper())
                    base_query = base_query.filter(column.in_([where_part[k]]), column.in_([where_part[k]]))

        elif list(filter)[0].lower() == "order":
            for key in filter:
                field = filter[key].split(" ")[0]
                direction = filter[key].split(" ")[1]
                # Limit then order, or order then limit
            if is_limited:
                if direction.upper() == "ASC":
                    base_query = base_query.from_self().order_by(asc(getattr(table, field)))
                elif direction.upper() == "DESC":
                    base_query = base_query.from_self().order_by(desc(getattr(table, field)))
                else:
                    raise BadFilterError(f" Bad filter given, filter: {filter}")
            else:
                if direction.upper() == "ASC":
                    base_query = base_query.order_by(asc(getattr(table, field)))
                elif direction.upper() == "DESC":
                    base_query = base_query.order_by(desc(getattr(table, field)))
                else:
                    raise BadFilterError(f" Bad filter given, filter: {filter}")

        elif list(filter)[0].lower() == "skip":
            for key in filter:
                skip = filter[key]
            base_query = base_query.offset(skip)

        elif list(filter)[0].lower() == "limit":
            is_limited = True
            for key in filter:
                limit = filter[key]
            base_query = base_query.limit(limit)
        elif list(filter)[0].lower() == "include":
            includes_relation = True

        else:
            raise BadFilterError(f"Invalid filters provided received {filters}")

    results = base_query.all()
    # check if include was provided, then add included results
    if includes_relation:
        for filter in filters:
            if list(filter)[0] == "include":
                results = get_related_entities(filter["include"], results)
    log.info(" Closing DB session")
    session.close()
    return list(map(lambda x: x.to_dict(), results))


def get_related_entities(include_filters, results):
    """
    Given a set of results from a query and an include filter of the form str, dict or list append to the results
    related entities
    :param include_filters: the include filter: str, dict or list
    :param results: list of rows from a query
    :return: updated list of rows with related entities
    """
        included_relationships = []
        included_included_relationships = []
    if type(include_filters) == str:
        included_relationships.append(include_filters)
    elif type(include_filters) == list:
        included_relationships.extend(include_filters)
    elif type(include_filters) == dict:
        for key in include_filters:
                        included_relationships.append(key)
            included_included_relationships.append(include_filters[key])
                else:
        raise BadFilterError(" Invalid format of included relationships")

        included_results = []
        included_included_results = []
        for row in results:
            for relation in included_relationships:
                # Here we check if the included result returns a list of children and if so iterate through them and
                # add them to the results.
                if isinstance(getattr(row, relation.upper()), InstrumentedList):
                    for i in getattr(row, relation.upper()):
                        included_results.append(i)
                else:
                    included_results.append(getattr(row, relation.upper()))
        for included_row in included_results:
            for relation in included_included_relationships:
                if isinstance(getattr(included_row, relation.upper()), InstrumentedList):
                    for i in getattr(included_row, relation.upper()):
                        included_included_results.append(i)
                else:
                    included_included_results.append(getattr(included_row, relation.upper()))
        results.extend(included_results)
        results.extend(included_included_results)
        return results


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
