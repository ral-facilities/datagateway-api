from datetime import datetime

from pydantic import BaseModel


class Session(BaseModel):
    id: str
    expireDateTime: datetime | None = None
    username: str | None = None
