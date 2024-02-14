from swagweb.abstractions.exception import SwagException


class BaseRequestException(SwagException):
    pass


class EmptyRequestException(BaseRequestException):
    pass
