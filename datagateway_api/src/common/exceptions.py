class ApiError(Exception):
    status_code = 500


class MissingRecordError(ApiError):
    def __init__(self, msg="No such record in table", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.status_code = 404


class FilterError(ApiError):
    def __init__(self, msg="Invalid filter requested", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.status_code = 400


class MultipleIncludeError(FilterError):
    def __init__(
        self,
        msg="Bad request, only one include filter may be given per request",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)
        self.status_code = 400


class AuthenticationError(ApiError):
    def __init__(self, msg="Authentication error", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.status_code = 403


class MissingCredentialsError(AuthenticationError):
    def __init__(self, msg="No credentials provided in auth header", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.status_code = 401


class BadRequestError(ApiError):
    def __init__(self, msg="Bad request", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.status_code = 400


class DatabaseError(ApiError):
    def __init__(self, msg="Database error", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.status_code = 500


class PythonICATError(ApiError):
    def __init__(self, msg="Python ICAT error", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.status_code = 500


class SearchAPIError(ApiError):
    def __init__(self, msg="Search API error", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.status_code = 500
