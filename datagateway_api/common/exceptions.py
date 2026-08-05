class ApiError(Exception):
    status_code = 500


class MissingRecordError(ApiError):
    status_code = 404

    def __init__(self, msg="No such record in table", *args):
        super().__init__(msg, *args)


class FilterError(ApiError):
    status_code = 400

    def __init__(self, msg="Invalid filter requested", *args):
        super().__init__(msg, *args)


class MultipleIncludeError(FilterError):
    status_code = 400

    def __init__(
        self,
        msg="Bad request, only one include filter may be given per request",
        *args,
    ):
        super().__init__(msg, *args)


class AuthenticationError(ApiError):
    status_code = 403

    def __init__(self, msg="Authentication error", *args):
        super().__init__(msg, *args)


class MissingCredentialsError(AuthenticationError):
    status_code = 401

    def __init__(self, msg="No credentials provided in auth header", *args):
        super().__init__(msg, *args)


class BadRequestError(ApiError):
    status_code = 400

    def __init__(self, msg="Bad request", *args):
        super().__init__(msg, *args)


class DatabaseError(ApiError):
    status_code = 500

    def __init__(self, msg="Database error", *args):
        super().__init__(msg, *args)


class PythonICATError(ApiError):
    status_code = 500

    def __init__(self, msg="Python ICAT error", *args):
        super().__init__(msg, *args)


class SearchAPIError(ApiError):
    status_code = 500

    def __init__(self, msg="Search API error", *args):
        super().__init__(msg, *args)


class ScoringAPIError(ApiError):
    status_code = 500

    def __init__(self, msg="Scoring API error", *args):
        super().__init__(msg, *args)
