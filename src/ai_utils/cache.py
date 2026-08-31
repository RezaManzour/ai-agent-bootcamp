"""Memoization cache decorator."""

import functools
from typing import Any, Callable, TypeVar, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")


def cache_result(func: Callable[P, T]) -> Callable[P, T]:
    """
    Cache function results based on positional and keyword arguments.

    The cache key is a tuple of (args, sorted_kwargs), ensuring that
    different orderings of keyword arguments produce the same key.

    Args:
        func: The function whose results should be cached.

    Returns:
        A wrapped function with an attached ``.cache`` dict for inspection.

    Example:
        >>> @cache_result
        ... def expensive_compute(x: int) -> int:
        ...     return x ** 2
    """
    cache: dict[Any, T] = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    wrapper.cache = cache  # type: ignore[attr-defined]
    return wrapper
