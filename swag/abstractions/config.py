from abc import ABC


class BaseSwagAppConfig(ABC):
    """
    Base config for app writen using swag lib
    """
    port: int
    host: str
    user_lim: int
    max_http_request_size: int  # in bytes
