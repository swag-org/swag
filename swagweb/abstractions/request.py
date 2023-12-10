from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Tuple
from .methods import HTTPMethod


class BaseRequest(ABC):
    headers: Dict[str, str]
    route: str
    ip: Tuple[str, int]  # actually it is ip and port
    method: HTTPMethod

    @staticmethod
    @abstractmethod
    def from_string(raw_string: str, ip: str) -> BaseRequest:
        ...
