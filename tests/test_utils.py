"""Tests for ai agent utilities."""

import pytest
from src.ai_utils import retry_with_backoff, cache_result, timer, batch_generator


def test_batch_generator_basic() -> None:
    items = [1, 2, 3, 4, 5]
    batches = list(batch_generator(items, batch_size=2))
    assert batches == [[1, 2], [3, 4], [5]]


def test_batch_generator_empty() -> None:
    assert list(batch_generator([], batch_size=2)) == []


def test_cache_result() -> None:
    call_count = 0
    
    @cache_result
    def add(a: int, b: int) -> int:
        nonlocal call_count
        call_count += 1
        return a + b
    
    assert add(2, 3) == 5
    assert add(2, 3) == 5  # cached
    assert call_count == 1  # only called once
