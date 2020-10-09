import logging
from datetime import datetime

from icat.entity import Entity, EntityList
from icat.query import Query
from icat.exception import ICATValidationError

from common.exceptions import PythonICATError
from common.constants import Constants

log = logging.getLogger()


class ICATQuery:
    def __init__(
        self, client, entity_name, conditions=None, aggregate=None, includes=None
    ):
        """
        Create a Query object within Python ICAT 

        :param client: ICAT client containing an authenticated user
        :type client: :class:`icat.client.Client`
        :param entity_name: Name of the entity to get data from
        :type entity_name: :class:`suds.sax.text.Text`
        :param conditions: Constraints used when an entity is queried
        :type conditions: :class:`dict`
        :param aggregate: Name of the aggregate function to apply. Operations such as
            counting the number of records. See `icat.query.setAggregate` for valid
            values.
        :type aggregate: :class:`str`
        :param includes: List of related entity names to add to the query so related
            entities (and their data) can be returned with the query result
        :type includes: :class:`str` or iterable of :class:`str`
        :return: Query object from Python ICAT
        :raises PythonICATError: If a ValueError is raised when creating a Query(), 500
            will be returned as a response
        """

        try:
            log.info("Creating ICATQuery for entity: %s", entity_name)
            self.query = Query(
                client,
                entity_name,
                conditions=conditions,
                aggregate=aggregate,
                includes=includes,
            )
        except ValueError:
            raise PythonICATError(
                "An issue has occurred while creating a Python ICAT Query object,"
                " suggesting an invalid argument"
            )

    def execute_query(self, client, return_json_formattable=False):
        """
        Execute a previously created ICAT Query object and return in the format
        specified by the return_json_formattable flag

        :param client: ICAT client containing an authenticated user
        :type client: :class:`icat.client.Client`
        :param return_json_formattable: Flag to determine whether the data from the 
            query should be returned as a list of data ready to be converted straight to
            JSON (i.e. if the data will be used as a response for an API call) or
            whether to leave the data in a Python ICAT format (i.e. if it's going to be
            manipulated at some point)
        :type return_json_formattable_data: :class:`bool`
        :return: Data (of type list) from the executed query
        :raises PythonICATError: If an error occurs during query execution
        """

        try:
            log.debug("Executing ICAT query")
            query_result = client.search(self.query)
        except ICATValidationError as e:
            raise PythonICATError(e)

        if self.query.aggregate == "DISTINCT":
            log.info("Extracting the distinct fields from query's conditions")
            distinct_filter_flag = True
            # Check query's conditions for the ones created by the distinct filter
            self.attribute_names = []

            for key, value in self.query.conditions.items():
                # Value can be a list if there's multiple WHERE filters for the same
                # attribute name within an ICAT query
                if isinstance(value, list):
                    for sub_value in value:
                        self.check_attribute_name_for_distinct(key, sub_value)
                elif isinstance(value, str):
                    self.check_attribute_name_for_distinct(key, value)
            log.debug(
                "Attribute names used in the distinct filter, as captured by the"
                " query's conditions %s",
                self.attribute_names,
            )
        else:
            distinct_filter_flag = False

        if return_json_formattable:
            log.info("Query results will be returned in a JSON format")
            data = []

            for result in query_result:
                distinct_result = {}
                dict_result = self.entity_to_dict(result, self.query.includes)

                for key, value in dict_result.items():
                    if distinct_filter_flag:
                        # Add only the required data as per request's distinct filter
                        # fields
                        if key in self.attribute_names:
                            distinct_result[key] = dict_result[key]

                if distinct_filter_flag:
                    data.append(distinct_result)
                else:
                    data.append(dict_result)
            return data
        else:
            log.info("Query results will be returned as ICAT entities")
            return query_result

    def check_attribute_name_for_distinct(self, key, value):
        """
        Check the attribute name to see if its associated value is used to signify the
        attribute is requested in a distinct filter and if so, append it to the list of
        attribute names

        :param key: Name of an attribute
        :type key: :class:`str`
        :param value: Expression that should be applied to the associated attribute
            e.g. "= 'Metadata'"
        :type value: :class:`str`
        """
        if value == Constants.PYTHON_ICAT_DISTNCT_CONDITION:
            self.attribute_names.append(key)

    def datetime_object_to_str(self, date_obj):
        """
        Convert a datetime object to a string so it can be outputted in JSON

        There's currently no reason to make this function static, but it could be useful
        in the future if a use case required this functionality.

        :param date_obj: Datetime object from data from an ICAT entity
        :type date_obj: :class:`datetime.datetime`
        :return: Datetime (of type string) in the agreed format
        """
        return date_obj.replace(tzinfo=None).strftime(Constants.ACCEPTED_DATE_FORMAT)

    def entity_to_dict(self, entity, includes):
        """
        This expands on Python ICAT's implementation of `icat.entity.Entity.as_dict()`
        to use set operators to create a version of the entity as a dictionary

        Most of this function is dedicated to recursing over included fields from a
        query, since this is functionality isn't part of Python ICAT's `as_dict()`. This
        function can be used when there are no include filters in the query/request
        however.

        :param entity: Python ICAT entity from an ICAT query
        :type entity: :class:`icat.entities.ENTITY` (implementation of
            :class:`icat.entity.Entity`) or :class:`icat.entity.EntityList`
        :param includes: Set of fields that have been included in the ICAT query. Where
            fields have a chain of relationships, they're a single element string
            separated by dots
        :type includes: :class:`set`
        :return: ICAT Data (of type dictionary) ready to be serialised to JSON
        """
        d = {}

        # Split up the fields separated by dots and flatten the resulting lists
        flat_includes = [m for n in (field.split(".") for field in includes) for m in n]

        # Verifying that `flat_includes` only has fields which are related to the entity
        include_set = (entity.InstRel | entity.InstMRel) & set(flat_includes)
        for key in entity.InstAttr | entity.MetaAttr | include_set:
            if key in flat_includes:
                target = getattr(entity, key)
                # Copy and remove don't return values so must be done separately
                includes_copy = flat_includes.copy()
                try:
                    includes_copy.remove(key)
                except ValueError:
                    log.warning(
                        "Key couldn't be found to remove from include list, this could"
                        " cause an issue further on in the request"
                    )
                if isinstance(target, Entity):
                    d[key] = self.entity_to_dict(target, includes_copy)
                # Related fields with one-many relationships are stored as EntityLists
                elif isinstance(target, EntityList):
                    d[key] = []
                    for e in target:
                        d[key].append(self.entity_to_dict(e, includes_copy))
            # Add actual piece of data to the dictionary
            else:
                entity_data = getattr(entity, key)
                # Convert datetime objects to strings ready to be outputted as JSON
                if isinstance(entity_data, datetime):
                    # Remove timezone data which isn't utilised in ICAT
                    entity_data = self.datetime_object_to_str(entity_data)
                d[key] = entity_data
        return d
