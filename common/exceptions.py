import logging

log = logging.getLogger()


class ApiError(Exception):
    def __init__(self):
        log.info(" ApiError(): An error has been raised.")


class MissingRecordError(ApiError):
    def __init__(self):
        log.info(" MissingRecordError(): Record not found, DB session Closed")



class BadFilterError(ApiError):
    def __init__(self):
        log.info(" BadFilterError(): Bad filter supplied")


class AuthenticationError(ApiError):
    def __init__(self):
        log.info(" AuthenticationError(): Error authenticating consumer")


class BadRequestError(ApiError):
    def __init__(self):
        log.info(" BadRequestError(): Bad request by Consumer")
