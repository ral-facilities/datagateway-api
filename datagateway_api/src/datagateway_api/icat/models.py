from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Session(BaseModel):
    id: str
    expireDateTime: Optional[datetime] = None
    username: Optional[str] = None
