from pydantic import BaseModel

from datagateway_api.src.common.date_handler import DateHandler
from datagateway_api.src.search_api.models import SearchAPIDatetime


class DateModel(BaseModel):
    """
    A Pydantic model that wraps a date value for serialization and validation.

    Attributes
    ----------
    date : SearchAPIDatetime
        A custom datetime type used by the Search API for consistent date handling.
    """

    date: SearchAPIDatetime


def normalise_date(date_str: str):
    """
    Convert a date string to the JSON-serializable 'date' field using DateModel.
    """
    dt_obj = DateHandler.str_to_datetime_object(date_str)
    return DateModel(date=dt_obj).model_dump(mode="json")["date"]
