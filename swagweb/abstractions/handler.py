from typing import Any, Protocol

from swagweb.http.request import HTTPRequest
from swagweb.http.response.response import HTTPResponse


class HTTPHandlerProtocol(Protocol):
    def __call__(self, request: HTTPRequest, **kwargs: Any) -> HTTPResponse: ...
