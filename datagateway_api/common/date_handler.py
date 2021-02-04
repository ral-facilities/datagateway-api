from dateutil.parser import parse
from icat import helper

from datagateway_api.common.exceptions import BadRequestError


class DateHandler:
    """
    Utility class to deal with dates. Currently, this class converts dates between
    strings and `datetime.datetime` objects as well as detecting whether a string is
    likely to be a date.
    """

    @staticmethod
    def is_str_a_date(potential_date):
        """
        This function identifies if a string contains a date. This function doesn't
        detect which format the date is, just if there's a date or not.

        :param potential_date: String data that could contain a date of any format
        :type potential_date: :class:`str`
        :return: Boolean to signify whether `potential_date` is a date or not
        """

        try:
            # Disabled fuzzy to avoid picking up dates in things like descriptions etc.
            parse(potential_date, fuzzy=False)
            return True
        except ValueError:
            return False

    @staticmethod
    def str_to_datetime_object(data):
        """
        Convert a string to a `datetime.datetime` object. This is commonly used when
        storing user input in ICAT (using the Python ICAT backend).

        Python 3.7+ has support for `datetime.fromisoformat()` which would be a more
        elegant solution to this conversion operation since dates are converted into ISO
        format within this file, however, the production instance of this API is
        typically built on Python 3.6, and it doesn't seem of enough value to mandate
        3.7 for a single line of code. Instead, a helper function from `python-icat` is
        used which does the conversion using `suds`. This will convert inputs in the ISO
        format (i.e. the format which Python ICAT, and therefore DataGateway API outputs
        data) but also allows for conversion of other "sensible" formats.

        :param data: Single data value from the request body
        :type data: Data type of the data as per user's request body, :class:`str` is
            assumed
        :return: Date converted into a :class:`datetime` object
        :raises BadRequestError: If there is an issue with the date format
        """

        try:
            datetime_obj = helper.parse_attr_string(data, "Date")
        except ValueError as e:
            raise BadRequestError(e)

        return datetime_obj

    @staticmethod
    def datetime_object_to_str(datetime_obj):
        """
        Convert a datetime object to a string so it can be outputted in JSON

        :param datetime_obj: Datetime object from data from an ICAT entity
        :type datetime_obj: :class:`datetime.datetime`
        :return: Datetime (of type string) in the agreed format
        """
        return datetime_obj.isoformat(" ")
