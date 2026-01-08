from pydantic import BaseModel

from datagateway_api.src.search_api import models


class DateModel(BaseModel):
    date: models.SearchAPIDatetime
