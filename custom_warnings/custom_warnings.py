import warnings
from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import update_wrapper, wraps
from typing import ParamSpec, TypeVar


P = ParamSpec("P")
R = TypeVar("R")


class _CustomWarning(ABC):
    @abstractmethod
    def __init__(self, message: str) -> None: ...


class Unstable(_CustomWarning):
    def __init__(self, message: str) -> None:
        self._message: str = message

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            warnings.warn(self._message)
            return func(*args, **kwargs)

        update_wrapper(wrapper, func)
        wraps(func)(wrapper)

        return wrapper
