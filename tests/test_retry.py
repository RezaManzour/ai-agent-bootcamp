"""Tests for retry_with_backoff."""

import pytest
from ai_utils import retry_with_backoff


def test_retry_succeeds_on_first_attempt():
    """Function should return immediately on success."""

    @retry_with_backoff(max_attempts=3, base_delay=0.01)
    def stable() -> str:
        return "ok"

    assert stable() == "ok"


def test_retry_eventually_succeeds(capsys):
    """Function should retry and eventually succeed."""
    attempts = 0

    @retry_with_backoff(max_attempts=3, base_delay=0.01)
    def flaky() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("not yet")
        return "success"

    result = flaky()
    assert result == "success"
    assert attempts == 3

    captured = capsys.readouterr()
    assert "Attempt 1 failed" in captured.out
    assert "Attempt 2 failed" in captured.out


def test_retry_exhausts_all_attempts():
    """Should raise the last exception when all attempts fail."""

    @retry_with_backoff(max_attempts=2, base_delay=0.01)
    def always_fails() -> None:
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        always_fails()


def test_retry_respects_exception_filter():
    """Should not retry exceptions not in the filter."""

    @retry_with_backoff(max_attempts=3, base_delay=0.01, exceptions=(ValueError,))
    def raises_type_error() -> None:
        raise TypeError("wrong type")

    with pytest.raises(TypeError, match="wrong type"):
        raises_type_error()
