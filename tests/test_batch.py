"""Tests for batch_generator."""

import pytest
from ai_utils import batch_generator


def test_batch_even_split():
    """Evenly divisible list should produce equal batches."""
    items = [1, 2, 3, 4, 5, 6]
    batches = list(batch_generator(items, 3))
    assert batches == [[1, 2, 3], [4, 5, 6]]


def test_batch_uneven_split():
    """Unevenly divisible list should have a smaller final batch."""
    items = [1, 2, 3, 4, 5]
    batches = list(batch_generator(items, 2))
    assert batches == [[1, 2], [3, 4], [5]]


def test_batch_single_item():
    """Batch size of 1 should yield single-item lists."""
    items = ["a", "b", "c"]
    batches = list(batch_generator(items, 1))
    assert batches == [["a"], ["b"], ["c"]]


def test_batch_empty_list():
    """Empty list should yield no batches."""
    assert list(batch_generator([], 5)) == []


def test_batch_invalid_size():
    """Batch size < 1 should raise ValueError."""
    with pytest.raises(ValueError, match="at least 1"):
        list(batch_generator([1], 0))
