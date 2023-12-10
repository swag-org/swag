from dataclasses import dataclass
from swagweb.abstractions.config import BaseSwagAppConfig
from swagweb.http.response import HTTPResponse


@dataclass
class SwagAppConfig(BaseSwagAppConfig):
    """
    Swag application config
    """

    port: int = 8000
    host: str = "127.0.0.1"
    backlog: int = 100
    dev_mode: bool = True  # if an exception occurs while the program is running, throws an exception if true, if false it does not.
    max_http_request_size: int = 1024  # in bytes
    http_statuses_responses = {
        404: HTTPResponse(
            "<h1>404 Not Found</h1",
            content_type="text/html",
            status=404,
            message="Not Found",
        ),
        500: HTTPResponse(
            "<h1>500 Internal Server Error</h1",
            content_type="text/html",
            status=500,
            message="Internal Server Error",
        ),
        422: HTTPResponse(
            "<h1>422 Unprocessable Content</h1",
            content_type="text/html",
            status=422,
            message="Unprocessable Content",
        ),
    }
