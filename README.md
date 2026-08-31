# AI Agent Utilities

[![CI](https://github.com/RezaManzour/ai-agent-bootcamp/actions/workflows/ci.yml/badge.svg)](https://github.com/RezaManzour/ai-agent-bootcamp/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A lightweight, zero-dependency Python toolkit for building **robust, observable, and efficient AI agents**.

Built during an intensive AI Agent Bootcamp — designed for production-grade LLM pipelines.

---

## Features

| Module | What it does | Perfect for |
|--------|--------------|-------------|
| `retry_with_backoff` | Auto-retry failed API calls with exponential delay | Rate-limited LLM APIs |
| `cache_result` | Memoize function results by args/kwargs | Avoid redundant LLM calls |
| `timer` | High-resolution execution profiling | Agent loop benchmarking |
| `batch_generator` | Chunk large lists into batches | Memory-efficient processing |

---

## Quick Start

```bash
git clone https://github.com/RezaManzour/ai-agent-bootcamp.git
cd ai-agent-bootcamp
pip install -e ".[dev]"



EQF
