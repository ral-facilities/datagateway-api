from datetime import datetime

from pydantic import BaseModel


class Session(BaseModel):
    id: str
    expireDateTime: datetime | None = None  # noqa: N815
    username: str | None = None
