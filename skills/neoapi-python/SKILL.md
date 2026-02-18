---
name: neoapi-python
version: 1.0.0-beta.23
description: "Fubon Neo (富邦新一代/富邦 API) Python SDK guidance focused on trading and market data workflows, including login, market data access, order placement, and locating the right docs/llms outputs. Use when prompts mention FubonNeo API or the Python SDK."
---

# NeoAPI Python

## Overview

本 skill 教導 AI 編程代理使用 **Fubon Neo Python SDK** 進行台股**證券交易**與**行情資料**存取。適用 Python 3.12–3.13、SDK >= 2.x（避免 3.14）。預設 SDK ~2.2.7，除非使用者另外指定。

> **TL;DR** — 三大工作流程：
> 1. **登入** → `sdk.login(ID, PWD, cert, cert_pwd)` 取得帳號清單
> 2. **下單** → 建構 `Order(...)` → `sdk.stock.place_order(acc, order)`
> 3. **行情** → `sdk.init_realtime()` → `sdk.marketdata.rest_client.stock.intraday.*`

## 常見錯誤（Common Mistakes）

| 錯誤 | 正確做法 |
| :--- | :--- |
| `pip install fubon-neo` | SDK 不在 PyPI，需從[官方頁面](https://www.fbs.com.tw/TradeAPI/docs/sdk/python/download?type=download)下載 `.whl` 安裝 |
| 在測試環境用 `intraday.quote` 判斷可下單價格 | 測試環境應用 `sdk.stock.query_symbol_quote(acc, symbol)` |
| SDK >= 2.2.1 仍用 `FubonSDK()` 初始化 | 需用 `FubonSDK(30, 2)` （或含 `url=` 參數） |
| 下單後找不到已刪的單 | 已刪單仍在 `get_order_results` 中，status=30 |
| 登入後直接用 `sdk.marketdata.rest_client` | 需先呼叫 `sdk.init_realtime()` |
| `user_def` 字串過長 | 建議 10 字元以內，過長會被截斷 |
| 在 Python 3.14 使用 SDK v2 | SDK v2 僅支援 3.12–3.13 |
| 數量填「張數」而非「股數」 | FubonNeo 數量一律為**股數**（1 張 = 1000 股） |

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
acc = accounts.data[0]  # Pick stock account

# Place Order (Buy 1000 shares of 2330 at Limit 580)
# Keyword form recommended (matches official docs); positional form also works.
order = Order(
    buy_sell=BSAction.Buy,
    symbol="2330",
    quantity=1000,
    market_type=MarketType.Common,
    price_type=PriceType.Limit,
    time_in_force=TimeInForce.ROD,
    order_type=OrderType.Stock,
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

## SDK 版本相容性（Version Compatibility）

| SDK Version | Python | Constructor | 備註 |
| :--- | :--- | :--- | :--- |
| >= 2.2.6 | 3.12–3.13 | `FubonSDK(30, 2)` | 下單錯誤拋出 `FugleAPIError` |
| 2.2.1–2.2.5 | 3.12–3.13 | `FubonSDK(30, 2)` | 錯誤在 response 物件中 |
| <= 2.2.0 | 3.12–3.13 | `FubonSDK()` | 無位置參數 |
| 1.3.1–1.x | 3.8–3.12 | `FubonSDK()` | 測試環境最低要求 |

測試環境一律加 `url="wss://neoapitest.fbs.com.tw/TASP/XCPXWS"` 參數。

## 工作流程決策樹（Workflow Decision Tree）

```
需求是什麼？
├── 交易（Trading）
│   ├── 下單 / 改單 / 刪單
│   │   ├── 測試環境？→ FubonSDK(30, 2, url=test_url) + query_symbol_quote 取價格
│   │   └── 正式環境？→ FubonSDK(30, 2) + intraday.ticker 取漲跌停
│   ├── 查詢帳務 → sdk.stock.get_order_results / get_inventories
│   └── 當沖（Day Trade）→ 見下方「當沖」章節
├── 行情（Market Data）
│   ├── 即時快照 → HTTP: intraday.quote（成交）/ intraday.ticker（參考價/漲跌停）
│   ├── 歷史資料 → HTTP: historical
│   └── 即時串流 → WebSocket: sdk.init_realtime() + subscribe
└── 環境確認
    ├── SDK 版本 → 見上方「版本相容性」
    ├── 安裝方式 → 官方 .whl（非 PyPI）
    └── 文件查詢 → references/doc-index.md
```

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

## 當沖（Day Trading）

台股當沖分為：

- **先買後賣**（現股當沖-買）：先以 `BSAction.Buy` 下單，同日再以 `BSAction.Sell` 賣出。使用 `OrderType.Stock`。
- **先賣後買**（現股當沖-賣/融券當沖）：先以融券賣出，同日再買回。使用 `OrderType.ShortSelling`。

### 關鍵判斷

- 使用 `intraday.ticker` 回傳的 `canDayTrade` / `canBuyDayTrade` 欄位確認標的可否當沖。
- 部位平倉（沖銷）：在收盤前以反向委託等量股數沖銷。

### 條件單當沖

SDK >= 2.2.4 支援條件單當沖（搜尋 llms-full.txt 中 `ConditionDayTrade` 或「當沖條件單」），可設定停損停利自動回補。

### 參考實作

- [StrategyExecutor_feather](https://github.com/phenomenoner/StrategyExecutor_feather)：現股當沖先賣的自動化策略範例。

## 期貨 / 選擇權（Futures & Options）

本 skill 目前以**證券（Stock）**交易與行情為主要範圍。SDK 支援期貨/選擇權帳號（`account_type == "futopt"`），但本 skill 尚未涵蓋對應的下單/行情 API。期貨條件單說明可搜尋 llms-full.txt 中「期貨條件單」。歡迎社群補充期貨/選擇權工作流程。

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
- Local integrated runner (maintainer/local): `.test/test_runner.py`
  - `--suite smoke`: basic login + market/trade sanity checks
  - `--suite complex`: multi-symbol marketdata + dual-order lifecycle + callback coverage
  - `--suite all`: full coverage (includes complex checks)
- For limit-down/limit-up in test env, prefer `sdk.stock.query_symbol_quote` (test environment data). `intraday.quote` uses market data (prod) and may differ.

## SDK Install (Quick Note)

- Python SDK is not on PyPI. Download the wheel from the official page and install locally.
- SDK >= v2 works on Python 3.12–3.13 (avoid 3.14 for now).

## Implementation Patterns

For production-tested patterns, see `references/implementation-practices.md`. Key topics:

- **SDK Manager**: Connection lifecycle, auto-reconnect, graceful termination
- **WebSocket**: Multi-connection load balancing (200 symbols/connection limit)
- **Async Patterns**: ThreadPoolExecutor for blocking calls, per-symbol locking
- **Error Handling**: FugleAPIError compatibility for old/new SDK versions
- **Order Placement**: Order creation, placement, and fill handling
- **Strategy Patterns**: Tick-to-decision pipeline, stop loss, position sizing
- **Error & Status Codes**: Order status codes, HTTP errors, common rejection reasons

## References

- **Doc index**: `references/doc-index.md`
- **Implementation practices**: `references/implementation-practices.md`
- **Response shapes**: `references/response-shapes.md`
- **Source docs (maintainers)**: `docs/` and `i18n/en/docusaurus-plugin-content-docs/current`

When code or docs need updating, mirror changes in the English localization if the content is user-facing.
