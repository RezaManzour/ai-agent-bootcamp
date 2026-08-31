"""Execution timing context manager."""

import time
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def timer(operation_name: str) -> Iterator[None]:
    """
    Context manager to measure and print execution time.

    Uses ``time.perf_counter()`` for high-resolution timing.

    Args:
        operation_name: Descriptive name of the timed block.

    Yields:
        None

    Example:
        >>> with timer("LLM inference"):
        ...     response = model.generate(prompt)
        [timer] LLM inference took 1.2345 seconds
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"[timer] {operation_name} took {elapsed:.4f} seconds")
