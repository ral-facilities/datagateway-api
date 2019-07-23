import logging

log = logging.getLogger()


class ApiError(Exception):
    pass


class MissingRecordError(ApiError):
    pass


class BadFilterError(ApiError):
    pass


class AuthenticationError(ApiError):
    pass


class BadRequestError(ApiError):
    pass
