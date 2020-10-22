import logging
from datetime import datetime

from icat.entity import Entity, EntityList
from icat.entities import getTypeMap
from icat.query import Query
from icat.exception import ICATValidationError, ICATInternalError

from common.exceptions import PythonICATError, FilterError
from common.date_handler import DateHandler
from common.constants import Constants

log = logging.getLogger()


class ICATQuery:
    def __init__(
        self, client, entity_name, conditions=None, aggregate=None, includes=None,
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
        Execute the ICAT Query object and return in the format specified by the
        return_json_formattable flag

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
            log.debug("Executing ICAT query: %s", self.query)
            query_result = client.search(self.query)
        except (ICATValidationError, ICATInternalError) as e:
            raise PythonICATError(e)

        flat_query_includes = self.flatten_query_included_fields(self.query.includes)
        mapped_distinct_fields = None

        # If the query has a COUNT function applied to it, some of these steps can be
        # skipped
        count_query = False
        if self.query.aggregate is not None:
            if "COUNT" in self.query.aggregate:
                count_query = True
                log.debug("This ICATQuery is used for COUNT purposes")

        if self.query.aggregate == "DISTINCT" and not count_query:
            log.info("Extracting the distinct fields from query's conditions")
            # Check query's conditions for the ones created by the distinct filter
            distinct_attributes = self.iterate_query_conditions_for_distinctiveness()
            if distinct_attributes != []:
                mapped_distinct_fields = self.map_distinct_attributes_to_entity_names(
                    distinct_attributes, flat_query_includes
                )
                log.debug(
                    "Attribute names used in the distinct filter, mapped to the entity they"
                    " are a part of: %s",
                    mapped_distinct_fields,
                )

        if return_json_formattable:
            log.info("Query results will be returned in a JSON format")
            data = []

            for result in query_result:
                if not count_query:
                    dict_result = self.entity_to_dict(
                        result, flat_query_includes, mapped_distinct_fields
                    )
                    data.append(dict_result)
                else:
                    data.append(result)

            return data
        else:
            log.info("Query results will be returned as ICAT entities")
            return query_result

    def iterate_query_conditions_for_distinctiveness(self):
        distinct_attributes = []
        for attribute_name, where_statement in self.query.conditions.items():
            if isinstance(where_statement, list):
                for sub_value in where_statement:
                    self.check_attribute_name_for_distinct(
                        distinct_attributes, attribute_name, sub_value
                    )
            elif isinstance(where_statement, str):
                self.check_attribute_name_for_distinct(
                    distinct_attributes, attribute_name, where_statement
                )

        return distinct_attributes

    def check_attribute_name_for_distinct(self, attribute_list, key, value):
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
            attribute_list.append(key)

    def entity_to_dict(self, entity, includes, distinct_fields=None):
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
        :param includes: List of fields that have been included in the ICAT query. It is
            assumed each element has been checked for multiple fields separated by dots,
            split them accordingly and flattened the resulting list. Note: 
            ICATQuery.flatten_query_included_fields performs this functionality.
        :type includes: :class:`list`
        :return: ICAT Data (of type dictionary) ready to be serialised to JSON
        """

        d = {}

        # Verifying that `includes` only has fields which are related to the entity
        include_set = (entity.InstRel | entity.InstMRel) & set(includes)
        for key in entity.InstAttr | entity.MetaAttr | include_set:
            if key in includes:
                target = getattr(entity, key)
                # Copy and remove don't return values so must be done separately
                includes_copy = includes.copy()
                try:
                    includes_copy.remove(key)
                except ValueError:
                    log.warning(
                        "Key couldn't be found to remove from include list, this could"
                        " cause an issue further on in the request"
                    )
                if isinstance(target, Entity):
                    if distinct_fields is not None:
                        distinct_fields_copy = self.prepare_distinct_fields_for_recursion(
                            key, distinct_fields
                        )
                    else:
                        distinct_fields_copy = None

                    d[key] = self.entity_to_dict(
                        target, includes_copy, distinct_fields_copy
                    )

                # Related fields with one-many relationships are stored as EntityLists
                elif isinstance(target, EntityList):
                    d[key] = []
                    for e in target:
                        if distinct_fields is not None:
                            distinct_fields_copy = self.prepare_distinct_fields_for_recursion(
                                key, distinct_fields
                            )
                        else:
                            distinct_fields_copy = None

                        d[key].append(
                            self.entity_to_dict(e, includes_copy, distinct_fields_copy)
                        )
            # Add actual piece of data to the dictionary
            else:
                entity_data = None

                if distinct_fields is None or key in distinct_fields["base"]:
                    entity_data = getattr(entity, key)
                    # Convert datetime objects to strings ready to be outputted as JSON
                    if isinstance(entity_data, datetime):
                        # Remove timezone data which isn't utilised in ICAT
                        entity_data = DateHandler.datetime_object_to_str(entity_data)

                    d[key] = entity_data
        return d

    def map_distinct_attributes_to_entity_names(self, distinct_fields, included_fields):
        """
        This function looks at a list of dot-separated fields and maps them to which
        entity they belong to

        The result of this function will be a dictionary that has a data structure
        similar to the example below. The values assigned to the 'base' key are the 
        fields that belong to the entity the request is being sent to (e.g. the base
        values of `/users` would be fields belonging to the User entity).

        Example return value: 
        `{'base': ['id', 'modTime'], 'userGroups': ['id', 'fullName'],
         'investigationUser': ['id', 'role']}`

        For distinct fields that are part of included entities (e.g. userGroups.id), it
        is assumed that the relevant entities have been specified in an include filter.
        This is checked, and a suitable exception is thrown. Without this, the query
        would execute, and the user would get a 200 response, but they wouldn't receive
        the data they're expecting, hence it's more sensible to raise a 400 to alert
        them to their probable mistake, rather than to just log a warning.

        :param distinct_fields: List of fields that should be distinctive in the request
            response, as per the distinct filters in the request
        :type distinct_fields: :class:`list`
        :param included_fields: List of fields that have been included in the ICAT
            query. It is assumed each element has been checked for multiple fields
            separated by dots, split them accordingly and flattened the resulting list.
            Note: ICATQuery.flatten_query_included_fields performs this functionality.
        :type included_fields: :class:`list`
        :return: Dictionary of fields, where the key denotes which entity they belong to
        """

        # Mapping which entities have distinct fields
        distinct_field_dict = {"base": []}

        for field in distinct_fields:
            split_fields = field.split(".")
            # Single element list means the field belongs to the entity which the
            # request has been sent to
            if len(split_fields) == 1:
                # Conventional list assignment causes IndexError because -2 is out of
                # range of a list with a single element
                split_fields.insert(-2, "base")

            # If a key doesn't exist in the dictionary, create it and assign an empty
            # list to it
            try:
                distinct_field_dict[split_fields[-2]]
            except KeyError:
                distinct_field_dict[split_fields[-2]] = []

            distinct_field_dict[split_fields[-2]].append(split_fields[-1])

        # Remove "base" key as this isn't a valid entity name in Python ICAT
        distinct_entities = list(distinct_field_dict.keys())
        distinct_entities.remove("base")

        # Search through entity names that have distinct fields for the request and
        # ensure these same entity names are in the query's includes
        for entity in distinct_entities:
            if entity not in included_fields:
                raise FilterError(
                    "A distinct field that has a relationship with another entity does"
                    " not have the included entity within an include filter in this"
                    " request. Please add all related entities which are required for"
                    " the fields in the distinct filter distinct to an include filter."
                )

        return distinct_field_dict

    def prepare_distinct_fields_for_recursion(self, entity_name, distinct_fields):
        """
        Copy `distinct_fields` and move the data held in `entity_name` portion of the
        dictionary to the "base" section of the dictionary. This function is called in
        preparation for recursive calls occurring in entity_to_dict()
        
        See map_distinct_attribute_to_entity_names() for an explanation regarding
        `distinct_fields` and its data structure

        :param entity_name: Name of the Python ICAT entity
        :type entity_name: :class:`str`
        :param distinct_fields: Names of fields in Python ICAT which should be outputted
            in the response, separated by which entities they belong to as the keys
        :type distinct_fields: :class:`dict`
        :return: A copy of `distinct_fields`, with the data from the entity name put
            into the base portion of the dictionary
        """
        # Reset base fields
        distinct_fields["base"] = []

        distinct_fields_copy = distinct_fields.copy()
        if entity_name in distinct_fields_copy.keys():
            distinct_fields_copy["base"] = distinct_fields_copy[entity_name]

        return distinct_fields_copy

    def flatten_query_included_fields(self, includes):
        """
        This will take the set of fields included in an ICAT query, split up the fields
        separated by dots, and flatten the resulting list

        :param includes: Set of fields that have been included in the ICAT query. Where
            fields have a chain of relationships, they're a single element string
            separated by dots
        :type includes: :class:`set`
        :return: Flattened list containing all the fields that have been included in the
            ICAT query
        """

        return [m for n in (field.split(".") for field in includes) for m in n]
