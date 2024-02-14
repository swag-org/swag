from abc import ABC, abstractmethod
from typing import Dict, Union


class BaseResponse(ABC):
    extra_headers: Union[Dict[str, str], None]
    date: Union[str, None] = None
    content_length: Union[int, None] = None
    content_type: str
    content_data: str
    status: int
    message: str
    server: str

    @abstractmethod
    def package(self) -> bytes:
        """Returns bytes that will be sent over a tcp connection"""
        ...
