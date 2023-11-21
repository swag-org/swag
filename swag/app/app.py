import os
import socket
import mimetypes
from typing import Any
from swag.http.request import HTTPRequest
from swag.http.response import HTTPResponse
from swag.http.route import HTTPRouteFactory, HTTPRoute
from swag.abstractions.methods import HTTPMethod
from .config import SwagAppConfig
from ..abstractions.response import BaseResponse


class SwagApp:
    """
    Main class for creating applications in swag framework
    currently supports only HTTP/1.1 and GET method
    --not_found - response that is sent when none of the existing routes matches the requested one
    """
    not_found = HTTPResponse("<h1>404 Not Found</h1", content_type="text/html", status=404, message="Not Found")

    def __init__(self, config: SwagAppConfig = SwagAppConfig()):
        self.host = config.host
        self.port = config.port
        self.config = config
        self.__route_factory = HTTPRouteFactory()

    def _route(self, method: HTTPMethod, path: str):
        def decorator(func):
            http_route = self.__route_factory.register(method, path, func)

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def get(self, path: str):
        return self._route("GET", path)

    def start(self):
        """Method for starting the server"""

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(self.config.user_lim)

        print("Listening at", s.getsockname())

        # main event loop
        while True:
            conn, addr = s.accept()
            raw_data: bytes = conn.recv(self.config.max_http_request_size)
            data: str = raw_data.decode()
            request = HTTPRequest.from_string(data, addr)
            response: BaseResponse = self.handle_request(request)
            conn.send(response.package())
            conn.close()

    def handle_request(self, request: HTTPRequest):
        """Handles incoming data and returns a response.
        Override this in subclass.
        """
        method = request.method
        route = request.route
        http_route = self.__route_factory.search(method, route)
        if http_route is None:
            return self.not_found

        return http_route.func(request)
