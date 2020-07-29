from common.filters import WhereFilter, DistinctFieldFilter, OrderFilter, SkipFilter, LimitFilter, \
    IncludeFilter

class DatabaseWhereFilter(WhereFilter):
    precedence = 1

    def __init__(self, field, value, operation):
        self.field = field
        self.included_field = None
        self.included_included_field = None
        self._set_filter_fields()
        self.value = value
        self.operation = operation

    def _set_filter_fields(self):
        if self.field.count(".") == 1:
            self.included_field = self.field.split(".")[1]
            self.field = self.field.split(".")[0]

        if self.field.count(".") == 2:
            self.included_included_field = self.field.split(".")[2]
            self.included_field = self.field.split(".")[1]
            self.field = self.field.split(".")[0]

    def apply_filter(self, query):
        try:
            field = getattr(query.table, self.field)
        except AttributeError:
            raise BadFilterError(f"Bad  WhereFilter requested")

        if self.included_included_field:
            included_table = getattr(db_models, self.field)
            included_included_table = getattr(db_models, self.included_field)
            query.base_query = query.base_query.join(
                included_table).join(included_included_table)
            field = getattr(included_included_table,
                            self.included_included_field)

        elif self.included_field:
            included_table = getattr(db_models, self.field)
            query.base_query = query.base_query.join(included_table)
            field = getattr(included_table, self.included_field)

        if self.operation == "eq":
            query.base_query = query.base_query.filter(field == self.value)
        elif self.operation == "like":
            query.base_query = query.base_query.filter(
                field.like(f"%{self.value}%"))
        elif self.operation == "lte":
            query.base_query = query.base_query.filter(field <= self.value)
        elif self.operation == "gte":
            query.base_query = query.base_query.filter(field >= self.value)
        elif self.operation == "in":
            query.base_query = query.base_query.filter(field.in_(self.value))
        else:
            raise BadFilterError(
                f" Bad operation given to where filter. operation: {self.operation}")


class DatabaseDistinctFieldFilter(DistinctFieldFilter):
    precedence = 0

    def __init__(self, fields):
        # This allows single string distinct filters
        self.fields = fields if type(fields) is list else [fields]

    def apply_filter(self, query):
        query.is_distinct_fields_query = True
        try:
            self.fields = [getattr(query.table, field)
                           for field in self.fields]
        except AttributeError:
            raise BadFilterError("Bad field requested")
        query.base_query = query.session.query(*self.fields).distinct()


class DatabaseOrderFilter(OrderFilter):
    precedence = 2

    def __init__(self, field, direction):
        self.field = field
        self.direction = direction

    def apply_filter(self, query):
        if self.direction.upper() == "ASC":
            query.base_query = query.base_query.order_by(
                asc(self.field.upper()))
        elif self.direction.upper() == "DESC":
            query.base_query = query.base_query.order_by(
                desc(self.field.upper()))
        else:
            raise BadFilterError(f" Bad filter: {self.direction}")


class DatabaseSkipFilter(SkipFilter):
    precedence = 3

    def __init__(self, skip_value):
        self.skip_value = skip_value

    def apply_filter(self, query):
        query.base_query = query.base_query.offset(self.skip_value)


class DatabaseLimitFilter(LimitFilter):
    precedence = 4

    def __init__(self, limit_value):
        self.limit_value = limit_value

    def apply_filter(self, query):
        query.base_query = query.base_query.limit(self.limit_value)


class DatabaseIncludeFilter(IncludeFilter):
    precedence = 5

    def __init__(self, included_filters):
        self.included_filters = included_filters["include"]

    def apply_filter(self, query):
        if not query.include_related_entities:
            query.include_related_entities = True
        else:
            raise MultipleIncludeError()
