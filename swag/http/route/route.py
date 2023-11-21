from typing import Callable, List, Union, Any
from swag.abstractions.methods import HTTPMethod
from swag.abstractions.route import BaseRoute
from swag.abstractions.response import BaseResponse
from swag.abstractions.request import BaseRequest

# in python sets .contains() operation time complexity  is O(1)
SUPPORTED_TYPES_FOR_HTTP_PATH_QUERY = {int, float, bool, str}
SupportedTypes = Union[str, int, float, bool]


class HTTPRoute(BaseRoute):
    def __init__(self, method: HTTPMethod, route: str, func: Callable[[BaseRequest, ...], BaseResponse]):
        self.method = method
        self.route = route
        self.func: Callable[[BaseRequest, ...], BaseResponse] = func
        self.cached_path_queries: Union[List[List[str, int, SupportedTypes]], None] = None

    def tokenize(self):
        if self.route == "/":
            return None

        tokens = self.route.split("/")[:1]
        for index, token in enumerate(tokens):
            if len(token) > 2:
                if token[0] == "{" and token[-1] == "}":
                    var_name = token[1:-1]
                    if var_name in self.func.__annotations__.keys(): # NOQA

                        if self.cached_path_queries is None:
                            self.cached_path_queries = []

                        var_type: Any = self.func.__annotations__[var_name] # NOQA
                        self.cached_path_queries.append([var_name, index, var_type])