"""Exponential backoff retry decorator."""

import time
import functools
from typing import Any, Callable, TypeVar, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")


def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Retry a function with exponential backoff.

    Delays follow the pattern: base_delay, 2*base_delay, 4*base_delay, ...

    Args:
        max_attempts: Maximum number of attempts before giving up.
        base_delay: Initial delay between retries in seconds.
        exceptions: Tuple of exception types to catch and retry on.

    Returns:
        Decorated function that retries on failure.

    Raises:
        The last exception if all attempts fail.

    Example:
        >>> @retry_with_backoff(max_attempts=3, base_delay=0.5)
        ... def flaky_api() -> dict:
        ...     ...
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    if attempt == max_attempts:
                        raise
                    delay = base_delay * (2 ** (attempt - 1))
                    print(
                        f"[retry] Attempt {attempt} failed: {exc}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    time.sleep(delay)
            raise RuntimeError("Unexpected exit from retry loop")

        return wrapper

    return decorator
