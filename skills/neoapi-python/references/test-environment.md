# Test Environment (Sandbox)

Source: `test_environment.zip` from the official SDK sample link.

## SDK Version Requirements

- Use SDK v1.3.1 or later.
- **SDK v2.2.0 and earlier (inclusive):**
  - Python: `sdk = FubonSDK(url="wss://neoapitest.fbs.com.tw/TASP/XCPXWS")`
  - C#/JS: `new FubonSDK("wss://neoapitest.fbs.com.tw/TASP/XCPXWS")`
- **SDK v2.2.1 and later:**
  - Python: `sdk = FubonSDK(30, 2, url="wss://neoapitest.fbs.com.tw/TASP/XCPXWS")`
  - C#/JS: `new FubonSDK(30, 2, "wss://neoapitest.fbs.com.tw/TASP/XCPXWS")`
  - Note: `30, 2` are reference values; adjust per official docs.

## SDK Download & Install (Python)

- The Python SDK is **not** published on PyPI; download the official wheel from:
  - https://www.fbs.com.tw/TradeAPI/docs/sdk/python/download?type=download
- Windows wheel example: `fubon_neo-2.2.7-cp37-abi3-win_amd64.whl`
- Install into a virtual environment (recommended):
  - `uv venv .test\.venv`
  - `uv pip install --python .test\.venv\Scripts\python.exe <path-to-wheel>`
- SDK >= v2 works with Python **3.12–3.13**; Python **3.14** is not supported yet.

## Credentials

- **Test account ID** = the ID shown on the test certificate.
- **Login password** = `12345678`.
- **Certificate password** = `12345678`.
- In the sample bundle, the `.pfx` filenames are the IDs (e.g., `41610792.pfx`).

## Behavior Notes

- You can test market data and order placement after login.
- Because this is a shared test account, account balances are **not** real and may look incorrect.
- Test inventory is pre-seeded and **resets daily** (no carry-over after trades).
- Canceled orders remain visible in `get_order_results`; status `30` means the order is canceled.

## Pre-seeded Test Inventory

| Symbol | Type | Shares |
|-------:|------|-------:|
| 2002 | Short sell | 500 |
| 2330 | Margin | 500 |
| 2881 | Cash | 500 |
| 0050 | Cash | 500 |

## Market Data Caveats

- You receive real-time quotes, but the **middle-office reference price** is not real-time.
- Order price limits are enforced against the middle-office reference price.
- To discover the reference price, place orders using the **reference price** first.
- `intraday.quote` is trade data and uses market data (prod); it may not match test environment prices.
- For prod limit prices, use `intraday.ticker`. For test environment limit prices, use `sdk.stock.query_symbol_quote(account, symbol)` and read `limitdown_price` / `limitup_price`.

## Market Data Access (HTTP)

- After login, call `sdk.init_realtime()` before using `sdk.marketdata.rest_client`.
- Example:
  - `sdk.init_realtime()`
  - `reststock = sdk.marketdata.rest_client.stock`

## Trade Testing Tips

- To simulate a fill, submit two opposite orders.
- Use `user_def` to distinguish your orders in the shared account.

## Trading Session (Test)

- Open hours: **09:30–19:00**.

## Validation (Local Smoke Test)

- 2026-01-26: Python 3.12.12 + SDK 2.2.7, login succeeded using sample certificate `41610792.pfx`, returned stock and futures accounts.
- 2026-01-27: Integrated order lifecycle test (symbol 2883):
  - Placed 3000 units, modified qty to 2000, modified price to limit-down (8.89) using `query_symbol_quote`, then canceled (status 30).
  - `intraday.quote` returned prod data (reference 18.3) and no limit-down; `query_symbol_quote` returned test limits.
  - Canceled orders remain visible in `get_order_results` with status 30.
