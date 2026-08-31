"""Tests for cache_result."""

from ai_utils import cache_result


def test_cache_returns_correct_value():
    """Cached function should return correct result."""

    @cache_result
    def add(a: int, b: int) -> int:
        return a + b

    assert add(2, 3) == 5


def test_cache_avoids_redundant_calls():
    """Second call with same args should not re-execute function."""
    call_count = 0

    @cache_result
    def compute(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    compute(5)
    compute(5)
    assert call_count == 1


def test_cache_different_args():
    """Different args should trigger separate executions."""
    call_count = 0

    @cache_result
    def compute(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    compute(1)
    compute(2)
    assert call_count == 2


def test_cache_kwargs_order_independence():
    """Different kwarg orderings should hit same cache key."""
    call_count = 0

    @cache_result
    def compute(a: int, b: int) -> int:
        nonlocal call_count
        call_count += 1
        return a + b

    compute(a=1, b=2)
    compute(b=2, a=1)
    assert call_count == 1


def test_cache_exposed_for_inspection():
    """Wrapper should expose internal cache dict."""

    @cache_result
    def identity(x: int) -> int:
        return x

    identity(42)
    assert len(identity.cache) == 1
    assert identity.cache[((42,), ())] == 42
