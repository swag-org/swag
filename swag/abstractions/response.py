from abc import ABC, abstractmethod
from typing import Dict, Union
from swag.abstractions.methods import HTTPMethod


class BaseResponse(ABC):
    extra_headers: Union[Dict[str, str], None]
    date: Union[str, None] = None
    content_length: Union[int, None] = None
    content_type: str
    content_data: Union[str, bytes]
    status: int
    message: str
    server: str

    @abstractmethod
    def package(self) -> bytes:
        """Returns bytes that will be sent over a tcp connection"""
        ...
