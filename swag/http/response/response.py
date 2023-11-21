from datetime import datetime
from typing import Dict, Union
from sys import getsizeof
from swag.abstractions.response import BaseResponse
from swag.abstractions.methods import HTTPMethod


class HTTPResponse(BaseResponse):
    extra_headers: Union[Dict[str, str], None]
    date: Union[str, None] = None
    content_length: Union[int, None] = None
    content_type: str
    content_data: Union[str, bytes]
    status: int
    method: Union[HTTPMethod, None] = None
    server: str = "SwagServer"

    def __init__(self, data: Union[str, bytes] = "",
                 content_type: str = "text/plain",
                 date: Union[str, None] = None,
                 message: str = "",
                 extra_headers: Union[Dict[str, str], None] = None,
                 status: int = 200):
        self.content_type = content_type
        self.content_data = data
        self.message = message
        self.date = date
        self.extra_headers = extra_headers
        self.status = status

    def _update_current_datetime(self):
        """
        set self.date formatted datetime
        if you want to set your own time zone or do something,
        feel free to override this function
        """
        self.date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")

    def _get_content_length(self) -> int:
        return len(self.content_data)

    def _get_headers_as_string(self) -> str:
        final_header_string: str = (
            f"Date: {self.date}\r\n"
            f"Server: {self.server}\r\n"
            f"Content-Type: {self.content_type}\r\n"
            f"Content-Length: {self.content_length}\r\n"
            f"Connection: close\r\n"
        )

        if self.extra_headers:
            for header, value in self.extra_headers.items():
                final_header_string += header + ": " + value + "\r\n"
        return final_header_string

    def package(self) -> bytes:
        """Returns bytes that will be sent over a tcp connection"""
        self._update_current_datetime()
        self.content_length = self._get_content_length()
        headers = self._get_headers_as_string()
        return ('HTTP/1.1 %i %s \r\n%s\r\n%s' % (self.status, self.message, headers, self.content_data)).encode()
