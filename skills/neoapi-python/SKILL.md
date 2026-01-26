---
name: neoapi-python
description: "Fubon Neo (富邦新一代/富邦 API) Python SDK guidance focused on trading and market data workflows, including login, market data access, order placement, and locating the right docs/llms outputs. Use when prompts mention FubonNeo API or the Python SDK."
---

# NeoAPI Python

## Overview

Use this skill to answer questions or write code with the Fubon Neo Python SDK, prioritizing trading and market data. Keep solutions OS-agnostic (Windows/Linux/macOS) and align with Python 3.12–3.13 for SDK >= 2.x (avoid 3.14), and SDK ~2.2.7 unless the user specifies otherwise.

## Public Docs Access

- Base site: https://www.fbs.com.tw/TradeAPI/
- English locale: https://www.fbs.com.tw/TradeAPI/en/
- Markdown pages: append `.md` to any doc URL if the site publishes markdown endpoints, for example:
  - https://www.fbs.com.tw/TradeAPI/docs/trading/prepare.md
- LLM indexes:
  - https://www.fbs.com.tw/TradeAPI/llms.txt
  - https://www.fbs.com.tw/TradeAPI/llms-full.txt
  - https://www.fbs.com.tw/TradeAPI/en/llms.txt
  - https://www.fbs.com.tw/TradeAPI/en/llms-full.txt

## Workflow Decision Tree

1. **Identify scope**: trading vs market data.
2. **Confirm environment**: test vs production, credentials, API keys, and certificates.
3. **Confirm SDK constraints**: Python version, SDK version, OS.
4. **Locate the right doc** (see `references/doc-index.md`).
5. **Draft code**: minimal, runnable example; call out required configuration.

## Trading Workflow

- Start from `docs/trading/prepare.mdx` and `docs/trading/quickstart.mdx` for setup.
- Use Python library references under `docs/trading/library/python/` for exact function names, parameters, and return types.
- Typical flow: login (password or API key) → place/modify/cancel order → query order/account info → logout.
- Always mention rate limits when relevant (`docs/trading/trade-rate-limit.md`).

## Market Data Workflow

- Decide on **HTTP** vs **WebSocket**:
  - HTTP API for snapshots, intraday, historical.
  - WebSocket API for real-time streams.
- Use `docs/market-data/http-api/getting-started.md` and `docs/market-data/websocket-api/getting-started.md`.
- Mention connection setup and rate limits when relevant.

## Testing / Sandbox

- Official test bundle: `https://www.fbs.com.tw/TradeAPI_SDK/sample_code/test_environment.zip`
- Use SDK v1.3.1+ and the test URL `wss://neoapitest.fbs.com.tw/TASP/XCPXWS`.
- SDK v2.2.0 and earlier: `FubonSDK(url=...)`
- SDK v2.2.1 and later: `FubonSDK(30, 2, url=...)` (30/2 are reference values).
- Test credentials: ID from certificate; login password and cert password are `12345678`.
- See `references/test-environment.md` for operational notes (trading hours, shared account caveats).
 - Python SDK is downloaded from the official site (not PyPI); install the wheel locally.

## SDK Install (Quick Note)

- Python SDK is not on PyPI. Download the wheel from the official page and install locally.
- SDK >= v2 works on Python 3.12–3.13 (avoid 3.14 for now).

## Using llms.txt Outputs

Prefer public URLs for external users. Use bundled files when the site endpoints are not available:

- Public:
  - https://www.fbs.com.tw/TradeAPI/llms.txt
  - https://www.fbs.com.tw/TradeAPI/llms-full.txt
  - https://www.fbs.com.tw/TradeAPI/en/llms.txt
  - https://www.fbs.com.tw/TradeAPI/en/llms-full.txt
- Bundled (offline):
  - `llms.txt`
  - `llms-full.txt`
  - `llms.en.txt`
  - `llms-full.en.txt`

Use `llms.txt` for navigation and `llms-full.txt` for exact parameter details or examples. If the files are missing or stale, fall back to the source docs in `docs/`.

## Implementation Patterns

For production-tested patterns, see `references/implementation-practices.md`. Key topics:

- **SDK Manager**: Connection lifecycle, auto-reconnect, graceful termination
- **WebSocket**: Multi-connection load balancing (200 symbols/connection limit)
- **Async Patterns**: ThreadPoolExecutor for blocking calls, per-symbol locking
- **Error Handling**: FugleAPIError compatibility for old/new SDK versions
- **Order Placement**: Order creation, placement, and fill handling

## References

- **Doc index**: `references/doc-index.md`
- **Implementation practices**: `references/implementation-practices.md`
- **Source docs (maintainers)**: `docs/` and `i18n/en/docusaurus-plugin-content-docs/current`

When code or docs need updating, mirror changes in the English localization if the content is user-facing.
