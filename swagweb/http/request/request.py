from __future__ import annotations
from typing import Dict, Tuple, List
from swagweb.abstractions.request import BaseRequest
from swagweb.abstractions.methods import HTTPMethod
from swagweb.exceptions.request import EmptyRequestException


class HTTPRequest(BaseRequest):
    @staticmethod
    def from_string(raw_string: str, ip: Tuple[str, int]) -> HTTPRequest:
        if len(raw_string) == 0:
            raise EmptyRequestException()

        request_data: List = raw_string.split("\r\n")
        request_meta = request_data[0].split()
        method: HTTPMethod = request_meta[0]
        route = request_meta[1]
        headers = {}
        body: str | None = None

        for index, line in enumerate(request_data):
            if line == "":
                body = "".join(request_data[index::])
                break
            line = line.split(":", 1)
            if len(line) > 1:
                headers[line[0]] = line[1]

        return HTTPRequest(
            method=method, headers=headers, body=body, route=route, ip=ip
        )

    def __init__(
        self,
        method: HTTPMethod,
        headers: Dict[str, str],
        body: str | None,
        route: str,
        ip: Tuple[str, int],
    ):
        self.method = method
        self.headers = headers
        self.body = body
        self.route = route
        self.ip = ip
