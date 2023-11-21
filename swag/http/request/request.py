from __future__ import annotations
from typing import Dict
from swag.abstractions.request import BaseRequest
from swag.abstractions.methods import HTTPMethod


class HTTPRequest(BaseRequest):
    @staticmethod
    def from_string(raw_string: str, ip: int) -> HTTPRequest:
        request_data = raw_string.split("\r\n")
        request_meta = request_data[0].split()
        method = request_meta[0]
        route = request_meta[1]

        headers = {}
        for line in request_data:
            line = line.split(":", 1)
            if len(line) > 1:
                headers[line[0]] = line[1]

        return HTTPRequest(
            method=method,
            headers=headers,
            route=route,
            ip=ip
        )

    def __init__(self, method: HTTPMethod, headers: Dict[str, str], route: str, ip: int):
        self.method = method
        self.headers = headers
        self.route = route
        self.ip = ip
