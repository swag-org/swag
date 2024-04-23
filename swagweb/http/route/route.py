from typing import Callable, Union, Any, Dict, Tuple
from swagweb.abstractions.handler import HTTPHandlerProtocol
from swagweb.abstractions.methods import HTTPMethod
from swagweb.abstractions.route import BaseRoute
from swagweb.http.request.request import HTTPRequest
from swagweb.http.response.response import HTTPResponse

# in python sets .contains() operation time complexity is O(1)
SUPPORTED_TYPES_FOR_HTTP_PATH_QUERY = {
    int,
    float,
    str,
}  # TODO: rename to  SUPPORTED_TYPES_FOR_HTTP_PATH_PLACEHOLDER
SupportedTypes = Union[str, int, float]  # TODO: rename to SupportedPlaceholderTypes


class HTTPRoute(BaseRoute):
    def __init__(
        self,
        method: HTTPMethod,
        route: str,
        func: HTTPHandlerProtocol,
    ):
        self.method = method
        self.route = route
        self.func: HTTPHandlerProtocol = func
        self.cached_path_queries: Union[Dict[int, Tuple[str, SupportedTypes]], None] = (
            None
        )

    def tokenize(self) -> None:
        """This function caches path queries"""
        if self.route == "/":
            return None

        tokens = self.route.split("/")[1:]
        for index, token in enumerate(tokens):
            if token[0] == "{" and token[-1] == "}":
                var_name = token[1:-1]
                if var_name in self.func.__annotations__.keys():  # NOQA
                    if self.cached_path_queries is None:
                        self.cached_path_queries = {}
                    var_type: Any = self.func.__annotations__[var_name]  # NOQA
                    self.cached_path_queries[index] = var_name, var_type
