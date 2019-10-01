class ApiError(Exception):
    pass


class MissingRecordError(ApiError):
    pass


class BadFilterError(ApiError):
    pass


class MultipleIncludeError(BadFilterError):
    pass


class AuthenticationError(ApiError):
    pass


class MissingCredentialsError(AuthenticationError):
    pass


class BadRequestError(ApiError):
    pass


class DatabaseError(ApiError):
    pass
