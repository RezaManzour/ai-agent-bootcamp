"""Batch processing generator."""

from typing import Any, Iterator


def batch_generator(items: list[Any], batch_size: int) -> Iterator[list[Any]]:
    """
    Split a list into equal-sized batches.

    The final batch may be smaller than ``batch_size`` if the list length
    is not evenly divisible.

    Args:
        items: List of items to partition.
        batch_size: Number of items per batch (must be >= 1).

    Yields:
        Sublists of the original list.

    Raises:
        ValueError: If ``batch_size`` is less than 1.

    Example:
        >>> list(batch_generator([1, 2, 3, 4, 5], 2))
        [[1, 2], [3, 4], [5]]
    """
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]
