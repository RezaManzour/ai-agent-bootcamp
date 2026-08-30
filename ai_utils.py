"""
ai_utils.py
===========
Utility functions for AI agent development.
Includes retry logic, caching, timing, and batch processing.
"""

import time
import functools
from typing import Any, Callable, Iterator, TypeVar, ParamSpec
from contextlib import contextmanager

P = ParamSpec("P")
T = TypeVar("T")


# ───────────────────────────────────────────────
# 1. Decorator: retry با exponential backoff
# ───────────────────────────────────────────────
def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Retry a function with exponential backoff.

    Args:
        max_attempts: Maximum number of attempts before giving up.
        base_delay: Initial delay between retries in seconds.
        exceptions: Tuple of exception types to catch and retry on.

    Returns:
        Decorated function that retries on failure.

    Raises:
        The last exception if all attempts fail.
    """
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    delay = base_delay * (2 ** (attempt - 1))
                    print(f"[retry] Attempt {attempt} failed: {e}. Retrying in {delay:.2f}s...")
                    time.sleep(delay)
            # Unreachable, but satisfies type checker
            raise RuntimeError("Unexpected exit from retry loop")
        return wrapper
    return decorator


# ───────────────────────────────────────────────
# 2. Decorator: simple cache
# ───────────────────────────────────────────────
def cache_result(func: Callable[P, T]) -> Callable[P, T]:
    """
    Cache function results based on args and kwargs.

    Args:
        func: The function to cache.

    Returns:
        Wrapped function with caching.
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


# ───────────────────────────────────────────────
# 3. Context Manager: timer
# ───────────────────────────────────────────────
@contextmanager
def timer(operation_name: str) -> Iterator[None]:
    """
    Context manager to measure execution time of a code block.

    Args:
        operation_name: Name of the operation being timed.

    Yields:
        None

    Example:
        >>> with timer("API call"):
        ...     result = fetch_data()
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"[timer] {operation_name} took {elapsed:.4f} seconds")


# ───────────────────────────────────────────────
# 4. Generator: batch processor
# ───────────────────────────────────────────────
def batch_generator(items: list[Any], batch_size: int) -> Iterator[list[Any]]:
    """
    Split a list into equal-sized batches.

    Args:
        items: List of items to batch.
        batch_size: Number of items per batch.

    Yields:
        Sublists of the original list.

    Raises:
        ValueError: If batch_size is less than 1.
    """
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]


# ───────────────────────────────────────────────
# 5. تابع تست
# ────────────────────────────────────────────
def test_all() -> None:
    """
    Run all tests for ai_utils.py.
    """
    print("=" * 50)
    print("Running ai_utils tests...")
    print("=" * 50)

    # ── Test cache_result ──
    call_count = 0

    @cache_result
    def add(a: int, b: int) -> int:
        nonlocal call_count
        call_count += 1
        return a + b

    assert add(2, 3) == 5
    assert add(2, 3) == 5  # should use cache
    assert call_count == 1, "Cache should prevent second call"
    print("✅ cache_result passed")

    # ── Test batch_generator ──
    items = [1, 2, 3, 4, 5, 6, 7]
    batches = list(batch_generator(items, 3))
    assert batches == [[1, 2, 3], [4, 5, 6], [7]], f"Got {batches}"
    print("✅ batch_generator passed")

    # ── Test timer ──
    import io
    import sys
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    with timer("sleep_test"):
        time.sleep(0.01)
    sys.stdout = old_stdout
    output = captured.getvalue()
    assert "sleep_test" in output and "seconds" in output
    print("✅ timer passed")

    # ── Test retry_with_backoff ──
    attempt_count = 0

    @retry_with_backoff(max_attempts=3, base_delay=0.01)
    def flaky() -> str:
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise ValueError("Not yet")
        return "success"

    result = flaky()
    assert result == "success"
    assert attempt_count == 3
    print("✅ retry_with_backoff passed")

    print("=" * 50)
    print("All tests passed! 🎉")
    print("=" * 50)


if __name__ == "__main__":
    test_all()
