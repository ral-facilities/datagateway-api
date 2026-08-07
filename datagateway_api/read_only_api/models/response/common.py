from pydantic import BaseModel, Field


class EntityModel(BaseModel):
    id_: int | None = Field(default=None, alias="id")
