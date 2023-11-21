from abc import ABC
from typing import Callable


class BaseRoute(ABC):
    route: str
    func: Callable


class BaseRouteFactory(ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BaseRouteFactory, cls).__new__(cls)
        return cls._instance
