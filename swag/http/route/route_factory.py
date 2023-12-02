import re
from typing import List, Callable, Union, Dict, Any, Optional, get_args
from swag.abstractions.methods import HTTPMethod
from swag.abstractions.route import BaseRouteFactory
from swag.abstractions.request import BaseRequest
from swag.abstractions.response import BaseResponse
from .route import HTTPRoute


class Node:
    handler: Union[HTTPRoute, None]
    childrens: Union[Dict[str, 'Node'], None]

    def __init__(self, childrens=None, handler=None):
        self.handler = handler
        self.childrens = childrens

    def __getitem__(self, item: str):
        patterns = [item, "{str}", "{int}", "{float}"]
        for pattern in patterns:
            if pattern in self.childrens:
                return self.childrens[pattern]

        return None

    def set_handler(self, handler: HTTPRoute):
        if self.handler:
            raise RuntimeError("Two handlers for one endpoint")
        self.handler = handler

    def __str__(self, level=0):
        result = "\t" * level + f"Handler: {self.handler}\n"
        if self.childrens:
            for key, value in self.childrens.items():
                result += "\t" * level + f"Path: {key}\n"
                result += value.__str__(level + 1)
        return result


class HTTPRouteFactory(BaseRouteFactory):
    routes: Dict[str, List[Node]] = {
        "GET": Node({"/": Node({})}),
        "POST": Node({"/": Node({})}),
        "PUT": Node({"/": Node({})}),
        "DELETE": Node({"/": Node({})}),
        "PATCH": Node({"/": Node({})}),
        "OPTIONS": Node({"/": Node({})}),
        "HEAD": Node({"/": Node({})})
    }

    parse_curly_brace_values = re.compile(r'\{([^{}]+)}')


    def __init__(self, http_responses_statuses: Dict[int, BaseResponse]):
        self.http_responses_statuses = http_responses_statuses


    def prepare_route(self, route: str) -> str:
        route = route.strip()
        if route[-1] == "/":
            route = route[:-1:]

        return route

    def register(self, method: HTTPMethod, route: str, func: Callable[[BaseRequest, ...], BaseResponse]) -> HTTPRoute:
        if method in get_args(HTTPMethod):
            method = method.__args__[0].__forward_arg__

        route = self.prepare_route(route)
        http_route = HTTPRoute(method, route, func)
        http_route.tokenize()

        route_tree = self.routes[method]
        tokens = route.split("/")
        actual_node = route_tree["/"]

        if len(tokens) == 1:  # when it's just /
            actual_node.set_handler(http_route)
            return actual_node

        for index, token in enumerate(tokens[1::]):
            if token[0] == "{" and token[-1] == "}":
                token: str = self.parse_curly_brace_values.findall(token)[0]

                if token in func.__annotations__.keys(): # NOQA
                    token = func.__annotations__[token] # NOQA

                   if token == str:
                        token = "{str}"
                    elif token == int:
                        token = "{int}"
                    elif token == float:
                        token = "{float}"
                    else: token = "{str}"

            if not (token in actual_node.childrens):
                actual_node.childrens[token] = Node({})
            actual_node = actual_node.childrens[token]

            if index == len(tokens) - 2:
                actual_node.handler = http_route
        return http_route

    def search(self, method: HTTPMethod, route: str) -> Optional[tuple[Any, dict[Any, Any]]]:
        tokens = route.split("/")[1::]
        route_tree = self.routes[method]

       # If we get something like /path/, we first split it into ['path', '']
       # and then remove the empty token if there is one.
        if tokens[-1] == "":
            tokens.pop()

        actual_node = route_tree["/"]
        kwargs = {}

        for index, token in enumerate(tokens):
            next_node = actual_node[token]
            if next_node is None: return None
            actual_node = next_node

        # TODO: refactor it to iterating on handler_cached_path_queries
        if actual_node.handler:
            for index, token in enumerate(tokens):
                if token == "": break
                if index in actual_node.handler.cached_path_queries:
                    arg_type = actual_node.handler.cached_path_queries[index][1]

                    try:
                        if arg_type == "int":
                            token = int(token)
                        if arg_type == "float":
                            token = float(token)
                    except (TypeError, ValueError):
                        return HTTPRoute(method, route, lambda x: self.http_responses_statuses[422]), {} # create cached 422 response

                    kwargs[actual_node.handler.cached_path_queries[index][0]] = token

        return actual_node.handler, kwargs
