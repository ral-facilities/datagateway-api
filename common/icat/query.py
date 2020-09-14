import logging
from datetime import datetime

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
        """

        try:
            query_result = client.search(self.query)
        except ICATValidationError as e:
            raise PythonICATError(e)

        if self.query.aggregate == "DISTINCT":
            distinct_filter_flag = True
            # Check query's conditions for the ones created by the distinct filter
            self.attribute_names = []
            log.debug("Query conditions: %s", self.query.conditions)

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
            data = []
            for result in query_result:
                dict_result = result.as_dict()
                distinct_result = {}

                for key in dict_result:
                    # Convert datetime objects to strings so they can be JSON
                    # serialisable
                    if isinstance(dict_result[key], datetime):
                        # Remove timezone data which isn't utilised in ICAT
                        dict_result[key] = (
                            dict_result[key]
                            .replace(tzinfo=None)
                            .strftime(Constants.ACCEPTED_DATE_FORMAT)
                        )

                    if distinct_filter_flag:
                        # Add only the required data as per request's distinct filter
                        # fields
                        if key in self.attribute_names:
                            distinct_result[key] = dict_result[key]

                # Add to the response's data depending on whether request has a distinct
                # filter
                if distinct_filter_flag:
                    data.append(distinct_result)
                else:
                    data.append(dict_result)
            return data
        else:
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
