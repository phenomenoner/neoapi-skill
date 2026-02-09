# NeoAPI Python Skill Adapter (Multi-Agent)

## Purpose

This repository provides the `neoapi-python` skill for Fubon Neo API workflows.

本檔作為多代理入口（OpenClaw / generic agents）。  
實際規則與內容以 `skills/neoapi-python/` 內檔案為準。

## Canonical Files

- `skills/neoapi-python/SKILL.md`
- `skills/neoapi-python/references/doc-index.md`
- `skills/neoapi-python/references/test-environment.md`
- `skills/neoapi-python/references/examples-guidance.md`
- `skills/neoapi-python/references/skill-tests.md`

## Required Behavior

1. Chinese-first responses; English as supplement for API terms and enums.
2. Prefer online LLM docs endpoints; use bundled `llms*.txt` only when offline/unavailable.
3. For test-environment order limits, use `sdk.stock.query_symbol_quote`.
4. `intraday.ticker` is for limit-up/limit-down in market data; `intraday.quote` is trade-oriented.
5. In `get_order_results`, status `30` means canceled order and can remain visible.

## Maintenance Rule

When `skills/neoapi-python/` changes, update this adapter and `CLAUDE.md` / `GEMINI.md` in the same commit.
