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
    eq: int | str


class NotEqualFilter(BaseModel):
    ne: int | str = Field(alias="neq")


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
    lt: int | str


class LessThanOrEqualToFilter(BaseModel):
    lte: int | str


class GreaterThanFilter(BaseModel):
    gt: int | str


class GreaterThanOrEqualToFilter(BaseModel):
    gte: int | str


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
        """
        Includes can be arbitrarily nested in lists or dictionaries, but ultimately represent paths of ICAT Entity
        attributes. In order to validate each attribute path is appropriate for the queried entity, these
        representations must first be cast to `str`s which can then be compared to a `StrEnum` for the given Entity for
        final validation.

        Entries in `list`s are recursively validated, as they may have any type.

        Values in `dict`s are recursively validated with keys prefixed to the start.

        Other types (`str` expected, but since this is before pydantic validation in principle it could be `Any`) are
        `yield`ed as is.

        For example: `{"investigation: ["type", "facility"]}` -> `"investigation.type", "investigation.facility"`.

        :param value: Representation of either full or partial path(s) of ICAT Entity attributes to be included.
        :type value: Any
        :yield: `str` representation(s) of all attribute paths represented in `value`.
        :rtype: Generator[str]
        """
        if isinstance(value, list):
            for inner_value in value:
                yield from BaseFilters._validate_include(inner_value)
        elif isinstance(value, dict):
            for key, inner_value in value.items():
                for inner_inner_value in BaseFilters._validate_include(inner_value):
                    yield f"{key}.{inner_inner_value}"
        else:
            yield value

    @field_validator("include", mode="before", check_fields=False)
    @classmethod
    def validate_include_field(cls, value: Any) -> Any:
        """
        As "before" validators are resolved in reverse order, `value` should already have been JSON decoded by
        `validate_multi_value_field`.

        Performs validation on all include filters requested via query parameters. Mutates `value` into new return
        value.

        :param value: Representations of all requested ICAT Entity attributes to include.
        :type value: Any
        :return:
            Expected `list[str]` where each entry is an ICAT Entity attribute path joined by ".",
            `Any` allowed as pydantic validation has not yet been called.
        :rtype: Any
        """
        return list(cls._validate_include(value))

    @field_validator("distinct", "where", "order", "include", mode="before", check_fields=False)
    @classmethod
    def validate_multi_value_field(cls, value: Any) -> Any:
        """
        Ensure that all fields accepting multiple filters get JSON decoded. Mutates `value` into new return value.

        :param value: Possibly JSON encoded query parameters for a field which can take multiple filters.
        :type value: Any
        :return:
            Expected `list` where each entry has been JSON decoded,
            `Any` allowed as pydantic validation has not yet been called.
        :rtype: Any
        """
        if isinstance(value, list):
            return_value = []
            for inner_value in value:
                try:
                    inner_value = json.loads(inner_value)
                    if isinstance(inner_value, list):
                        return_value.extend(inner_value)
                    else:
                        return_value.append(inner_value)
                except json.JSONDecodeError:
                    # `value` may be JSON encoded ('"string"') or not ('string'), allow either
                    return_value.append(inner_value)

            value = return_value

        return value

    @field_validator("order", mode="after", check_fields=False)
    @classmethod
    def validate_order_field(cls, value: list[StrEnum]) -> list[StrEnum]:
        """
        Performs validation on all order filters requested via query parameters, ensuring that no field appears more
        than once. Does not mutate `value`.

        :param value: `list` of pydantic validated `StrEnum`s in the format `"{field} {direction}"`.
        :type value: list[StrEnum]
        :raises ValueError: If the same field appears multiple times in the list of order filters.
        :return: `value` (unmodified).
        :rtype: list[StrEnum]
        """
        unique_keys = set()
        for order in value:
            key, _ = order.split()
            if key in unique_keys:
                raise ValueError("Cannot order on the same field multiple times")
            unique_keys.add(key)

        return value

    @model_serializer(mode="plain")
    def serialize(self) -> list:
        """
        :return:
            All filters requested via query parameters, instantiated as PythonICAT filter objects and in the appropriate
            order.
        :rtype: list
        """
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
        """
        Note that as GET queries for single Entities only support include filters, this just returns the `list[str]`
        that `get_with_id` expects and not a list of PythonICAT filter objects like other requests require.

        :return:
            Include filters requested via query parameters, represented as `str`s of ICAT Entity attribute paths.
        :rtype: list[str]
        """
        return [str(i) for i in self.include]
