class ApiError(Exception):
    pass


class MissingRecordError(ApiError):
    pass


class BadFilterError(ApiError):
    pass


class AuthenticationError(ApiError):
    pass
