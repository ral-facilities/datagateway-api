from datagateway_api.common.helpers import map_distinct_attributes_to_results
from datetime import datetime
import logging

from icat.entity import Entity, EntityList
from icat.exception import ICATInternalError, ICATValidationError
from icat.query import Query

from datagateway_api.common.date_handler import DateHandler
from datagateway_api.common.exceptions import PythonICATError


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
        # Needed for ISIS endpoints as they use DISTINCT keyword but don't select
        # multiple attributes
        self.isis_endpoint = False

        try:
            log.info("Creating ICATQuery for entity: %s", entity_name)
            self.query = Query(
                client,
                entity_name,
                conditions=conditions,
                aggregate=aggregate,
                includes=includes,
            )
            # Initialising flag for distinct filter on count endpoints
            self.query.manual_count = False
        except ValueError:
            raise PythonICATError(
                "An issue has occurred while creating a Python ICAT Query object,"
                " suggesting an invalid argument",
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

        # If the query has a COUNT function applied to it, some of these steps can be
        # skipped
        count_query = False
        if self.query.aggregate is not None:
            if "COUNT" in self.query.aggregate:
                count_query = True
                log.debug("This ICATQuery is used for COUNT purposes")

        distinct_query = False
        if (
            self.query.aggregate == "DISTINCT"
            and not count_query
            and not self.query.manual_count
            and not self.isis_endpoint
        ):
            distinct_query = True
            log.info("Extracting the distinct fields from query's conditions")
            # Check query's conditions for the ones created by the distinct filter
            distinct_attributes = self.get_distinct_attributes()

        if return_json_formattable:
            log.info("Query results will be returned in a JSON format")
            data = []

            if self.query.manual_count:
                # Manually count the number of results
                data.append(len(query_result))
                return data

            for result in query_result:
                if distinct_query:
                    # When multiple attributes are given in a distinct filter, Python
                    # ICAT returns the results in a nested list. This doesn't happen
                    # when a single attribute is given, so the result is encased in a
                    # list as `map_distinct_attributes_to_results()` assumes a list as
                    # input
                    if not isinstance(result, tuple):
                        result = [result]

                    # Map distinct attributes and result
                    data.append(
                        map_distinct_attributes_to_results(distinct_attributes, result),
                    )
                elif not count_query:
                    dict_result = self.entity_to_dict(result, flat_query_includes)
                    data.append(dict_result)
                else:
                    data.append(result)

            return data
        else:
            log.info("Query results will be returned as ICAT entities")
            return query_result

    def get_distinct_attributes(self):
        return self.query.attributes

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
                        " cause an issue further on in the request",
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
                    entity_data = DateHandler.datetime_object_to_str(entity_data)

                d[key] = entity_data
        return d

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

        return [m for n in (field.split(".") for field in sorted(includes)) for m in n]
