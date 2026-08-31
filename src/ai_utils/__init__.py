"""
ai_utils
========
A lightweight Python toolkit for building robust AI agents.

Modules:
    retry    — Exponential backoff retry decorator
    cache    — Memoization cache decorator
    timer    — Execution timing context manager
    batch    — Batch processing generator

Example:
    >>> from ai_utils import retry_with_backoff, cache_result
    >>> @retry_with_backoff(max_attempts=3)
    ... @cache_result
    ... def call_api(x: int) -> int:
    ...     return x * 2
"""

from .retry import retry_with_backoff
from .cache import cache_result
from .timer import timer
from .batch import batch_generator

__version__ = "0.1.0"
__all__ = [
    "retry_with_backoff",
    "cache_result",
    "timer",
    "batch_generator",
]
