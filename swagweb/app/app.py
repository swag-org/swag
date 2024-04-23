import socket
from swagweb.exceptions.request import EmptyRequestException
from swagweb.http.request import HTTPRequest
from swagweb.http.route import HTTPRouteFactory
from swagweb.abstractions.methods import HTTPMethod
from .config import SwagAppConfig
from ..abstractions.response import BaseResponse


class SwagApp:
    """
    Main class for creating applications in swag library
    currently supports only HTTP/1.1
    """

    def __init__(self, config: SwagAppConfig = SwagAppConfig()):
        self.host = config.host
        self.port = config.port
        self.config = config
        self.not_found = config.http_statuses_responses[404]
        self.__route_factory = HTTPRouteFactory(
            self.config.http_statuses_responses,
            self.config.booleans_true,
            self.config.booleans_false,
        )

    def route(self, method: HTTPMethod, path: str):
        def decorator(func):
            http_route = self.__route_factory.register(method, path, func)

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def start(self) -> None:
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

                except EmptyRequestException:
                    conn.close()

                except Exception as e:
                    conn.send(self.config.http_statuses_responses[500].package())
                    if self.config.dev_mode:
                        raise e
                    print(e)

            except Exception as e:
                if self.config.dev_mode:
                    raise e
                print(e)

    def handle_request(self, request: HTTPRequest):
        """Handles incoming data and returns a response.
        feel free to override this in your subclass, if you need.
        """
        method = request.method
        route = request.route
        http_route = None

        search_result = self.__route_factory.search(method, route)
        # when route not found.
        if search_result is None:
            return self.not_found

        http_route, kwargs = search_result
        if http_route is None:
            return self.not_found

        return http_route.func(request, **kwargs)
