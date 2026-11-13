from enum import StrEnum
import json
from typing import Any, Generator, Literal

from pydantic import (
    BaseModel,
    Field,
    NonNegativeInt,
    PositiveInt,
    field_validator,
    model_serializer,
)

from datagateway_api.common.config import config
from datagateway_api.datagateway_api.icat.filters import (
    PythonICATDistinctFieldFilter,
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


class CommonWhereFilters(BaseModel):
    id_: EqualFilter | None = Field(default=None, alias="id")


class BaseFilters(BaseModel):
    @staticmethod
    def _validate_include(value: Any) -> Generator[str]:
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                pass  # `value` may be JSON encoded ('"string"') or not ('string'), allow either

        if isinstance(value, list):
            for inner_value in value:
                yield from BaseFilters._validate_include(inner_value)
        elif isinstance(value, dict):
            for key, inner_value in value.items():
                for inner_inner_value in BaseFilters._validate_include(inner_value):
                    yield f"{key}.{inner_inner_value}"
        else:
            yield value

    @field_validator("where", mode="before", check_fields=False)
    @classmethod
    def validate_where(cls, value: Any) -> Any:
        if isinstance(value, list):
            value = [json.loads(v) if isinstance(v, str) else v for v in value]

        return value

    @field_validator("order", mode="after", check_fields=False)
    @classmethod
    def validate_order(cls, value: list[StrEnum]) -> list[StrEnum]:
        unique_keys = set()
        for order in value:
            key, _ = order.split()
            if key in unique_keys:
                raise ValueError("Cannot order on the same field multiple times")
            unique_keys.add(key)

        return value

    @field_validator("include", mode="before", check_fields=False)
    @classmethod
    def validate_include(cls, value: Any) -> Any:
        return list(cls._validate_include(value))

    @model_serializer(mode="plain")
    def serialize(self) -> list:
        filters = []
        if getattr(self, "distinct", None):
            filters.append(PythonICATDistinctFieldFilter([str(d) for d in self.distinct]))

        if hasattr(self, "skip"):
            filters.append(PythonICATSkipFilter(skip_value=self.skip))

        if hasattr(self, "limit"):
            filters.append(PythonICATLimitFilter(limit_value=self.limit))

        if hasattr(self, "where"):
            for where_filter in self.where:
                for field, inner in where_filter.model_dump(by_alias=True, exclude_none=True).items():
                    for operation, value in inner.items():
                        filters.append(PythonICATWhereFilter(field=field, operation=operation, value=value))

        if hasattr(self, "order"):
            for order_filter in self.order:
                filters.append(PythonICATOrderFilter(*order_filter.split()))

        if hasattr(self, "include"):
            filters.append(PythonICATIncludeFilter([str(i) for i in self.include]))

        return filters


class CommonCountFilters(BaseFilters):
    distinct: list[Literal["id"]] = []
    where: list[CommonWhereFilters] = []


class CommonSearchFilters(CommonCountFilters):
    order: list[StrEnum] = []
    skip: NonNegativeInt = Field(
        default=0,
        description="Skip the first results returned by the query. Used for pagination.",
    )
    limit: PositiveInt = Field(
        default=config.read_only_api.limit.default if config.read_only_api is not None else 100,
        le=config.read_only_api.limit.maximum if config.read_only_api is not None else 100,
        description="Return at most this many results per request.",
    )
    include: list[str] = []


class CommonGetFilters(BaseFilters):
    include: list[str] = []

    @model_serializer(mode="plain")
    def serialize(self) -> list[str]:
        return [str(i) for i in self.include]
