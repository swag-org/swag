from dataclasses import dataclass
from swag.abstractions.config import BaseSwagAppConfig


@dataclass
class SwagAppConfig(BaseSwagAppConfig):
    """
    Swag application config
    """
    port: int = 8000
    host: str = "127.0.0.1"
    user_lim: int = 100
    max_http_request_size: int = 1024 # in bytes
