from enum import StrEnum
import json
from typing import Any

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt, model_serializer, model_validator

from datagateway_api.common.config import Config
from datagateway_api.datagateway_api.icat.filters import (
    PythonICATIncludeFilter,
    PythonICATLimitFilter,
    PythonICATOrderFilter,
    PythonICATSkipFilter,
    PythonICATWhereFilter,
)

WHERE_DESCRIPTION = (
    "Apply conditions to specified fields.\n\nQueryable fields are: {queryable_fields}.\n\nPossible operators are: "
    "'eq' (equals), 'neq'/'ne' (not equals), 'isnull', 'like' (includes), 'ilike' (case-insensitive includes), "
    "'nlike' (does not include), 'lt' (less than), 'lte' (less than or equals), 'gt' (greater than), "
    "'gte' (greater than or equals), 'in'/'inq', 'nin' (not in), 'between', 'regexp' (regular expression pattern).\n\n"
    "The format of a condition should be {{field: {{operator: value}}}}."
)
ORDER_DESCRIPTION = (
    "Order results by the value of the specified field(s) in ascending or descending order.\n\n"
    "Orderable fields are: {orderable_fields}.\n\nThe format of an order should be 'field asc' or 'field desc'."
)
INCLUDE_DESCRIPTION = "Include related entities.\n\nPossible includes are: {includable_paths}"


class EqualFilter(BaseModel):
    eq: str


class NotEqualFilter(BaseModel):
    ne: str = Field(alias="neq")


class IsNullFilter(BaseModel):
    isnull: bool


class LikeFilter(BaseModel):
    like: str


class InsensitiveLikeFilter(BaseModel):
    ilike: str


class NotLikeFilter(BaseModel):
    nlike: str


class NotInsensitiveLikeFilter(BaseModel):
    nilike: str


class LessThanFilter(BaseModel):
    lt: str


class LessThanOrEqualToFilter(BaseModel):
    lte: str


class GreaterThanFilter(BaseModel):
    gt: str


class GreaterThanOrEqualToFilter(BaseModel):
    gte: str


class InFilter(BaseModel):
    inq: list = Field(alias="in")


class NotInFilter(BaseModel):
    nin: list


class BetweenFilter(BaseModel):
    between: list = Field(min_length=2, max_length=2)


class RegexFilter(BaseModel):
    regexp: str


AnyFilter = (
    EqualFilter
    | NotEqualFilter
    | IsNullFilter
    | LikeFilter
    | InsensitiveLikeFilter
    | NotLikeFilter
    | NotInsensitiveLikeFilter
    | LessThanFilter
    | LessThanOrEqualToFilter
    | GreaterThanFilter
    | GreaterThanOrEqualToFilter
    | InFilter
    | NotInFilter
    | BetweenFilter
    | RegexFilter
    | None
)


class CommonWhereFilter(BaseModel):
    name: AnyFilter = None

    @model_validator(mode="before")
    @classmethod
    def validate(cls, data: Any) -> Any:
        if isinstance(data, str):
            return json.loads(data)

        return data


def validate_order(order: list[StrEnum]) -> list[StrEnum]:
    unique_keys = set()
    for o in order:
        key, _ = o.split()
        if key in unique_keys:
            raise ValueError("Cannot order on the same field multiple times")
        unique_keys.add(key)

    return order


class CommonFilters(BaseModel):
    # where: list[BaseModel]
    where: list[CommonWhereFilter]
    order: list[StrEnum]
    skip: NonNegativeInt = Field(
        default=0,
        description="Skip the first results returned by the query. Used for pagination.",
    )
    limit: PositiveInt = Field(
        default=Config.config.read_only_api.limit.default if Config.config.read_only_api is not None else 100,
        le=Config.config.read_only_api.limit.maximum if Config.config.read_only_api is not None else 100,
        description="Return at most this many results per request.",
    )

    @model_serializer(mode="plain")
    def serialize(self) -> list:
        filters = [PythonICATSkipFilter(skip_value=self.skip), PythonICATLimitFilter(limit_value=self.limit)]
        for where_filter in self.where:
            for field, inner in where_filter.model_dump(by_alias=True, exclude_none=True).items():
                for operation, value in inner.items():
                    filters.append(PythonICATWhereFilter(field=field, operation=operation, value=value))

        for order_filter in self.order:
            filters.append(PythonICATOrderFilter(*order_filter.split()))

        return filters


class CommonAndIncludeFilters(CommonFilters):
    include: list[StrEnum]

    @model_serializer(mode="plain")
    def serialize(self) -> list:
        filters = super().serialize()
        if self.include:
            filters.append(PythonICATIncludeFilter([i.value for i in self.include]))

        return filters
