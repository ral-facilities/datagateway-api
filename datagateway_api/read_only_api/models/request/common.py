from collections.abc import Iterable, Sequence
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

SKIP_DESCRIPTION = "Skip the first results returned by the query. Used alongside `limit` for pagination."
LIMIT_DESCRIPTION = "Return at most this many results per request."
DISTINCT_DESCRIPTION = (
    "Return distinct value(s) of the specified field(s).\n\nOnly the specified fields are returned in the response."
)

# Each entry maps the aliases accepted for an operator to a description of what it matches
WHERE_OPERATORS: tuple[tuple[tuple[str, ...], str], ...] = (
    (("eq",), "equal to the value"),
    (("neq", "ne"), "not equal to the value"),
    (("isnull",), "null when `true`, not null when `false`"),
    (("like",), "includes the value"),
    (("ilike",), "includes the value, ignoring case"),
    (("nlike",), "does not include the value"),
    (("nilike",), "does not include the value, ignoring case"),
    (("lt",), "less than the value"),
    (("lte",), "less than or equal to the value"),
    (("gt",), "greater than the value"),
    (("gte",), "greater than or equal to the value"),
    (("in", "inq"), "equal to any value in the given list"),
    (("nin",), "not equal to any value in the given list"),
    (("between",), "within the range of the two given values"),
    (("regexp",), "matches the given regular expression"),
)


def _code_list(values: Iterable[str]) -> str:
    """Render values as a comma separated list of inline code spans."""
    return ", ".join(f"`{value}`" for value in values)


def where_description(queryable_fields: Sequence[str]) -> str:
    """Build the Markdown description of the `where` filter for the given queryable fields."""
    operators = "\n".join(
        f"- {' / '.join('`' + alias + '`' for alias in aliases)} - {meaning}"
        for aliases, meaning in WHERE_OPERATORS
    )
    example = '{"' + queryable_fields[0] + '": {"eq": "value"}}'

    return (
        "Apply conditions to the specified fields.\n\n"
        f"**Queryable fields:** {_code_list(queryable_fields)}\n\n"
        '**Format:** `{"field": {"operator": value}}`\n\n'
        f"**Example:** `{example}`\n\n"
        f"**Operators:**\n\n{operators}"
    )


def order_description(orderable_fields: Sequence[str]) -> str:
    """Build the Markdown description of the `order` filter for the given orderable fields."""
    return (
        "Order results by the value of the specified field(s), in ascending or descending order.\n\n"
        f"**Orderable fields:** {_code_list(orderable_fields)}\n\n"
        "**Format:** `field asc` or `field desc`\n\n"
        "Multiple orders are applied in the order they are given. A field can only be ordered on once."
    )


def include_description(includable_paths: Sequence[str]) -> str:
    """Build the Markdown description of the `include` filter for the given related entity paths."""
    return (
        "Include related entities in the response.\n\n"
        f"**Includable paths:** {_code_list(includable_paths)}"
    )


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
    skip: NonNegativeInt = Field(default=0, description=SKIP_DESCRIPTION)
    limit: PositiveInt = Field(
        default=Config.config.read_only_api.limit.default if Config.config.read_only_api is not None else 100,
        le=Config.config.read_only_api.limit.maximum if Config.config.read_only_api is not None else 100,
        description=LIMIT_DESCRIPTION,
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
