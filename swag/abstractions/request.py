from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict
from .methods import HTTPMethod


class BaseRequest(ABC):
    headers: Dict[str, str]
    route: str
    ip: str
    method: HTTPMethod

    @staticmethod
    @abstractmethod
    def from_string(raw_string: str, ip: str) -> BaseRequest:
        ...
