from datetime import datetime
from dateutil.parser import parse

from datagateway_api.common.exceptions import BadRequestError
from datagateway_api.common.constants import Constants


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
        3.7 for a single line of code

        :param data: Single data value from the request body
        :type data: Data type of the data as per user's request body
        :return: Date converted into a :class:`datetime` object
        :raises BadRequestError: If the date is entered in the incorrect format, as per
            `Constants.ACCEPTED_DATE_FORMAT`
        """

        try:
            data = datetime.strptime(data, Constants.ACCEPTED_DATE_FORMAT)
        except ValueError:
            raise BadRequestError(
                "Bad request made, the date entered is not in the correct format. Use"
                f" the {Constants.ACCEPTED_DATE_FORMAT} format to submit dates to the"
                " API"
            )

        return data

    @staticmethod
    def datetime_object_to_str(date_obj):
        """
        Convert a datetime object to a string so it can be outputted in JSON

        :param date_obj: Datetime object from data from an ICAT entity
        :type date_obj: :class:`datetime.datetime`
        :return: Datetime (of type string) in the agreed format
        """
        return date_obj.replace(tzinfo=None).strftime(Constants.ACCEPTED_DATE_FORMAT)
