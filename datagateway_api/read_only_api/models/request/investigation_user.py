from typing import Literal

from pydantic import BaseModel, Field

from datagateway_api.read_only_api.models.request.common import CommonCountFilters, EqualFilter


class InvestigationUserWhereFilters(BaseModel):
    user_name: EqualFilter | None = Field(alias="user.name")


class InvestigationUserSearchFilters(CommonCountFilters):
    distinct: list[Literal["role"]] = Field(default=["role"], min_length=1, max_length=1)
    where: list[InvestigationUserWhereFilters] = Field(min_length=1, max_length=1)
