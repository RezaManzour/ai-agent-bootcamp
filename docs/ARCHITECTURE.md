# Architecture

## Overview

`ai_utils` is a zero-dependency Python toolkit designed for AI agent developers.
It provides four core primitives:

1. **Retry** — Resilient API interaction via exponential backoff
2. **Cache** — Memoization to avoid redundant LLM/API calls
3. **Timer** — High-resolution profiling of agent loops
4. **Batch** — Memory-efficient chunked processing

## Design Decisions

- **Zero runtime dependencies**: No external packages required for core functionality.
- **Type-safe**: Full `ParamSpec` / `TypeVar` annotations for decorator composability.
- **Composable decorators**: `retry_with_backoff` and `cache_result` can be stacked.
- **Generator-based batching**: Memory-efficient for large datasets.

## Module Map
