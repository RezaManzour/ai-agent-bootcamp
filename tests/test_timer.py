"""Tests for timer context manager."""

import time
import pytest
from ai_utils import timer


def test_timer_prints_duration(capsys):
    """Timer should print the operation name and duration."""
    with timer("test_op"):
        time.sleep(0.01)

    captured = capsys.readouterr()
    assert "[timer] test_op took" in captured.out
    assert "seconds" in captured.out


def test_timer_always_executes(capsys):
    """Timer should print even if an exception occurs."""
    with pytest.raises(ValueError):
        with timer("failing_op"):
            raise ValueError("boom")

    captured = capsys.readouterr()
    assert "[timer] failing_op took" in captured.out
