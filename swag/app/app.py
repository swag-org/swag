import socket
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
    def __init__(self, config: SwagAppConfig = SwagAppConfig()):
        self.host = config.host
        self.port = config.port
        self.config = config
        self.not_found = config.http_statuses_responses[404]
        self.__route_factory = HTTPRouteFactory(self.config.http_statuses_responses)


    def route(self, method: HTTPMethod, path: str):
        def decorator(func):
            http_route = self.__route_factory.register(method, path, func)

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator


    def start(self):
        """Method for starting the server"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(self.config.backlog)
        print(f"Looks like we are live at: {self.host}:{self.port}")

        # main event loop
        while True:
            try:
                conn, addr = s.accept()
                raw_data: bytes = conn.recv(self.config.max_http_request_size)

                try:
                    data: str = raw_data.decode()
                    request = HTTPRequest.from_string(data, addr)
                    response: BaseResponse = self.handle_request(request)
                    conn.send(response.package())
                    conn.close()
                except Exception as e:
                    conn.send(self.config.http_statuses_responses[500].package())
                    if self.config.dev_mode: raise e
                    print(e)

            except Exception as e:
                if self.config.dev_mode: raise e
                print(e)


    def handle_request(self, request: HTTPRequest):
        """Handles incoming data and returns a response.
        feel free to override this in your subclass, if you need.
        """
        method = request.method
        route = request.route
        http_route = None

        # when route not found.
        try:
            http_route, kwargs = self.__route_factory.search(method, route)
        except TypeError:
            return self.not_found

        if http_route is None:
            return self.not_found

        return http_route.func(request, **kwargs)
