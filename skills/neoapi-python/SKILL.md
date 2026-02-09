---
name: neoapi-python
description: "Fubon Neo (富邦新一代/富邦 API) Python SDK guidance focused on trading and market data workflows, including login, market data access, order placement, and locating the right docs/llms outputs. Use when prompts mention FubonNeo API or the Python SDK."
---

# NeoAPI Python

## Overview

Use this skill to answer questions or write code with the Fubon Neo Python SDK, prioritizing trading and market data. Keep solutions OS-agnostic (Windows/Linux/macOS) and align with Python 3.12–3.13 for SDK >= 2.x (avoid 3.14), and SDK ~2.2.7 unless the user specifies otherwise.

## Public Docs Access

- Base site: <https://www.fbs.com.tw/TradeAPI/>
- English locale: <https://www.fbs.com.tw/TradeAPI/en/>
- Build with LLM (zh): <https://www.fbs.com.tw/TradeAPI/docs/welcome/build-with-llm>
- Build with LLM (en): <https://www.fbs.com.tw/TradeAPI/en/docs/welcome/build-with-llm/>
- LLM indexes:
  - <https://www.fbs.com.tw/TradeAPI/llms.txt>
  - <https://www.fbs.com.tw/TradeAPI/llms-full.txt>
  - <https://www.fbs.com.tw/TradeAPI/en/llms.txt>
  - <https://www.fbs.com.tw/TradeAPI/en/llms-full.txt>
- Note: The `.md` URL trick is no longer supported; rely on `llms.txt` and `llms-full.txt`.

## Usage Cheat Sheet

### Quickstart (Trading)

```python
from fubon_neo.sdk import FubonSDK, Order, Mode
from fubon_neo.constant import BSAction, MarketType, PriceType, TimeInForce, OrderType

# Init & Login
sdk = FubonSDK()  # Use FubonSDK(30, 2) if on SDK 2.2.1+
accounts = sdk.login("ID", "PWD", "C:/path/to/cert.pfx", "CertPWD")
acc = accounts.data[0] # Pick stock account

# Place Order (Buy 1000 shares of 2330 at Limit 580)
order = Order(
    BSAction.Buy, "2330", 1000,
    MarketType.Common, PriceType.Limit, TimeInForce.ROD, OrderType.Stock,
    price="580"
)
res = sdk.stock.place_order(acc, order)
print(f"Order: {res.data.order_no}")
```

### Critical Constants

| Category | Class | Common Values |
| :--- | :--- | :--- |
| **Action** | `BSAction` | `.Buy`, `.Sell` |
| **Price** | `PriceType` | `.Limit` (限價), `.Market` (市價), `.Reference` (參考價) |
| **Time** | `TimeInForce` | `.ROD` (當日有效), `.IOC` (立即成交否則取消), `.FOK` (全部成交否則取消) |
| **Market** | `MarketType` | `.Common` (整股), `.IntradayOdd` (盤中零股), `.Odd` (盤後零股) |
| **Order** | `OrderType` | `.Stock` (現股), `.MarginTrading` (融資), `.ShortSelling` (融券) |

### Validating Prices

Real-time quotes (`intraday.quote`) may differ from valid order prices (especially in Test Env).

- **For Orders**: Always check `sdk.stock.query_symbol_quote(acc, symbol)`.
  - Use `limit_up_price` / `limit_down_price` from this result for placing limit orders.
  - This source reflects the *order system's* view of validity.
- **For Display**: Use `sdk.marketdata.rest_client.stock.intraday.quote(symbol)`.

### Rate Limits (Summary)

- **REST**: 300 req/min (IP-based).
- **WebSocket**: 200 subscriptions per connection.

## Workflow Decision Tree

1. **Identify scope**: trading vs market data.
2. **Confirm environment**: test vs production, credentials, API keys, and certificates.
3. **Confirm SDK constraints**: Python version, SDK version, OS.
4. **Locate the right doc** (see `references/doc-index.md`).
5. **Draft code**: minimal, runnable example; call out required configuration.

## Trading Workflow

- Start from `docs/trading/prepare` and `docs/trading/quickstart` for setup.
- Use Python library references under `docs/trading/library/python/` for exact function names, parameters, and return types.
- Typical flow: login (password or API key) → place/modify/cancel order → query order/account info → logout.
- Always mention rate limits when relevant (`docs/trading/trade-rate-limit`).

## Market Data Workflow

- Decide on **HTTP** vs **WebSocket**:
  - HTTP API for snapshots, intraday, historical.
  - WebSocket API for real-time streams.
- Use `docs/market-data/http-api/getting-started` and `docs/market-data/websocket-api/getting-started`.
- Mention connection setup and rate limits when relevant.
- To use `sdk.marketdata.rest_client`, call `sdk.init_realtime()` after login.
- For limit-up/limit-down prices in market data, use `intraday.ticker` (not `intraday.quote`).

## Examples

- Use `references/examples-guidance.md` to map SDK calls to docs and avoid common modification pitfalls.

## Testing / Sandbox

- Official test bundle: `https://www.fbs.com.tw/TradeAPI_SDK/sample_code/test_environment.zip`
- Use SDK v1.3.1+ and the test URL `wss://neoapitest.fbs.com.tw/TASP/XCPXWS`.
- SDK v2.2.0 and earlier: `FubonSDK(url=...)`
- SDK v2.2.1 and later: `FubonSDK(30, 2, url=...)` (30/2 are reference values).
- Test credentials: ID from certificate; login password and cert password are `12345678`.
- See `references/test-environment.md` for operational notes (trading hours, shared account caveats).
- Python SDK is downloaded from the official site (not PyPI); install the wheel locally.
- Skill validation checklist: `references/skill-tests.md`.
- For limit-down/limit-up in test env, prefer `sdk.stock.query_symbol_quote` (test environment data). `intraday.quote` uses market data (prod) and may differ.

## SDK Install (Quick Note)

- Python SDK is not on PyPI. Download the wheel from the official page and install locally.
- SDK >= v2 works on Python 3.12–3.13 (avoid 3.14 for now).

## Using llms.txt Outputs

Prefer public URLs as the primary source. Use bundled files as offline fallback:

- Public:
  - <https://www.fbs.com.tw/TradeAPI/llms.txt>
  - <https://www.fbs.com.tw/TradeAPI/llms-full.txt>
  - <https://www.fbs.com.tw/TradeAPI/en/llms.txt>
  - <https://www.fbs.com.tw/TradeAPI/en/llms-full.txt>
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

## Language & Localization

- **Source of Truth**: The primary documentation `llms-full.txt` is in **Traditional Chinese**.
- **Response Style**:
  - If the user asks in Chinese, answer in Chinese with English code comments.
  - If the user asks in English, answer in English but provide the Chinese Terminology in parenthesis for clarity (e.g., "ROD (當日有效)").
- **Terminology Mapping**:
  - **Limit Order**: 限價 (LMT)
  - **Market Order**: 市價 (MKT)
  - **ROD**: 當日有效
  - **IOC**: 立即成交否則取消
  - **FOK**: 全部成交否則取消
  - **Margin Trading**: 融資
  - **Short Selling**: 融券
  - **Day Trade**: 當沖
