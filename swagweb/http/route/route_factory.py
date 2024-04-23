from __future__ import annotations
import re
from typing import List, Callable, Union, Dict, Any, Optional
from swagweb.abstractions.handler import HTTPHandlerProtocol
from swagweb.abstractions.methods import HTTPMethod
from swagweb.http.response.response import HTTPResponse
from swagweb.http.request.request import HTTPRequest
from swagweb.abstractions.route import BaseRouteFactory
from swagweb.exceptions.node import NodeNotFoundException
from .route import HTTPRoute


class Node:
    handler: Union[HTTPRoute, None] = None
    childrens: Union[Dict[str, Node], None] = None

    def __init__(self, childrens=None, handler=None):
        self.handler = handler
        self.childrens = childrens

    def __getitem__(self, item: str) -> Node:
        patterns = [item, "{str}", "{int}", "{float}", "{bool}"]

        if self.childrens is None:
            raise NodeNotFoundException()

        for pattern in patterns:
            if pattern in self.childrens:
                return self.childrens[pattern]

        raise NodeNotFoundException()

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
    parse_curly_brace_values = re.compile(r"\{([^{}]+)}")

    def __init__(
        self,
        http_responses_statuses: Dict[int, HTTPResponse],
        booleans_true: set[str],
        booleans_false: set[str],
    ):
        self.routes: Dict[str, Node] = {
            "GET": Node({"/": Node({})}),
            "POST": Node({"/": Node({})}),
            "PUT": Node({"/": Node({})}),
            "DELETE": Node({"/": Node({})}),
            "PATCH": Node({"/": Node({})}),
            "OPTIONS": Node({"/": Node({})}),
            "HEAD": Node({"/": Node({})}),
        }
        self.booleans_true = booleans_true
        self.booleans_false = booleans_false

        self.http_responses_statuses = http_responses_statuses

    def prepare_route(self, route: str) -> str:
        route = route.strip()
        if route[-1] == "/":
            route = route[:-1:]

        return route

    def __get_default_unprocessable_response(
        self, request: HTTPRequest, **kwargs: Any
    ) -> HTTPResponse:
        return self.http_responses_statuses[422]

    def register(
        self,
        method: HTTPMethod,
        route: str,
        func: HTTPHandlerProtocol,
    ) -> HTTPRoute:
        route = self.prepare_route(route)
        http_route = HTTPRoute(method, route, func)
        http_route.tokenize()

        route_tree = self.routes[method]
        tokens: List[str] = route.split("/")
        actual_node: Node = route_tree["/"]

        if len(tokens) == 1:  # when it's just /
            actual_node.set_handler(http_route)
            return http_route

        index: int
        token: str

        for index, token in enumerate(tokens[1::]):
            if token[0] == "{" and token[-1] == "}":
                token = self.parse_curly_brace_values.findall(token)[0]

                if token in func.__annotations__.keys():  # NOQA
                    token_type = func.__annotations__[token]  # NOQA

                    if token_type == str:
                        token = "{str}"
                    elif token_type == int:
                        token = "{int}"
                    elif token_type == float:
                        token = "{float}"
                    elif token_type == bool:
                        token = "{bool}"
                    else:
                        token = "{str}"

            if actual_node.childrens is None:
                raise RuntimeError("Idk handle in future")

            if token not in actual_node.childrens.keys():
                actual_node.childrens[token] = Node({})
            actual_node = actual_node.childrens[token]

            if index == len(tokens) - 2:
                actual_node.handler = http_route
        return http_route

    def search(
        self, method: HTTPMethod, route: str
    ) -> Optional[tuple[Any, dict[Any, Any]]]:
        tokens: List[str] = route.split("/")[1::]
        route_tree = self.routes[method]

        # If we get something like /path/, we first split it into ['path', '']
        # and then remove the empty token if there is one.
        if tokens[-1] == "":
            tokens.pop()

        actual_node: Node = route_tree["/"]
        kwargs = {}

        try:
            for index, raw_token in enumerate(tokens):
                next_node = actual_node[raw_token]
                actual_node = next_node
        except NodeNotFoundException:
            return None

        # TODO: refactor it to iterating on handler_cached_path_queries
        if actual_node.handler:
            for index, raw_token in enumerate(tokens):
                if raw_token == "":
                    break
                if (
                    actual_node.handler.cached_path_queries
                    and index in actual_node.handler.cached_path_queries
                ):
                    arg_type = actual_node.handler.cached_path_queries[index][1]
                    token: Any = None

                    # TODO: refactoring
                    try:
                        if arg_type == int:
                            token = int(raw_token)
                        elif arg_type == float:
                            token = float(raw_token)
                        elif arg_type == bool:
                            if raw_token in self.booleans_true:
                                token = True
                            elif raw_token in self.booleans_false:
                                token = False
                            else:
                                raise ValueError(
                                    f"Cant find the boolean value for {raw_token}"
                                )
                        else:
                            token = raw_token
                    except (TypeError, ValueError) as e:
                        return (
                            HTTPRoute(
                                method,
                                route,
                                self.__get_default_unprocessable_response,
                            ),
                            {},
                        )  # return cached 422 response

                    kwargs[actual_node.handler.cached_path_queries[index][0]] = token

        return actual_node.handler, kwargs
