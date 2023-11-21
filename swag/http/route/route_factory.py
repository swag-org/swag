from typing import List, Callable, Union
from swag.abstractions.methods import HTTPMethod
from swag.abstractions.route import BaseRouteFactory
from swag.abstractions.request import BaseRequest
from swag.abstractions.response import BaseResponse
from .route import HTTPRoute


class HTTPRouteFactory(BaseRouteFactory):
    routes: List[HTTPRoute] = []

    def register(self, method: HTTPMethod, route: str, func: Callable[[BaseRequest, ...], BaseResponse]) -> HTTPRoute:
        http_route = HTTPRoute(method, route, func)
        http_route.tokenize()
        self.routes.append(http_route)
        return http_route

    def search(self, method: HTTPMethod, route: str) -> Union[HTTPRoute, None]:
        for http_route in self.routes:
            if http_route.method == method and http_route.route == route:
                return http_route
        return None
