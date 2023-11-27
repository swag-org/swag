from abc import ABC
from typing import Dict
from .response import BaseResponse


class BaseSwagAppConfig(ABC):
    """
    Base config for app writen using swag lib
    """
    port: int
    host: str
    user_lim: int
    max_http_request_size: int  # in bytes
    http_statuses_responses: Dict[int, BaseResponse]
