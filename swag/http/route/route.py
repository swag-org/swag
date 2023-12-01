from typing import Callable, List, Union, Any, Dict
from swag.abstractions.methods import HTTPMethod
from swag.abstractions.route import BaseRoute
from swag.abstractions.response import BaseResponse
from swag.abstractions.request import BaseRequest

# in python sets .contains() operation time complexity  is O(1)
SUPPORTED_TYPES_FOR_HTTP_PATH_QUERY = {int, float, str} # TODO: rename to  SUPPORTED_TYPES_FOR_HTTP_PATH_PLACEHOLDER
SupportedTypes = Union[str, int, float] # TODO: rename to SupportedPlaceholderTypes


class HTTPRoute(BaseRoute):
    def __init__(self, method: HTTPMethod, route: str, func: Callable[[BaseRequest, ...], BaseResponse]):
        self.method = method
        self.route = route
        self.func: Callable[[BaseRequest, Any, Any], BaseResponse] = func
        self.cached_path_queries: Union[Dict[int, List[str, SupportedTypes]], None] = None

    def tokenize(self):
        """This function cache path queries"""
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
                    self.cached_path_queries[index] = ([var_name, var_type])
