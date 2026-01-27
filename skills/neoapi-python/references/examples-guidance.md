# Examples Guidance (Code Reading & Modification)

Use this guide to help an AI agent understand existing NeoAPI Python code and make safe modifications.

## 1) Identify Environment & SDK Version

- **Test vs Production:** Look for `FubonSDK(url=...)` and the URL used.
  - Test URL: `wss://neoapitest.fbs.com.tw/TASP/XCPXWS`
  - Prod uses default (no URL override).
- **SDK version clues:** Constructor signature can hint the version:
  - v2.2.0 and earlier: `FubonSDK(url=...)`
  - v2.2.1+ : `FubonSDK(30, 2, url=...)`

## 2) Locate Credentials & Certs

- Login usually calls: `sdk.login(USER_ID, USER_PW, CERT_PATH, CERT_PW)`.
- In test env, **password and cert password are `12345678`** and ID is the cert filename.
- Verify cert path and environment variables (common source of failure).

## 3) Identify Account Type

- `accounts.data` may include multiple account types.
- Stock orders should use `account_type == "stock"`.
- Futures/Options use `account_type == "futopt"`.

## 4) Map Actions to Docs

Match SDK calls to the official docs (via `references/doc-index.md`):

- Login/logout: `docs/trading/library/python/login/`, `docs/trading/library/python/logout.md`
- Stock orders: `docs/trading/library/python/trade/`
- Account info: `docs/trading/library/python/accountManagement/`
- Market data (HTTP/WS): `docs/market-data/http-api/*`, `docs/market-data/websocket-api/*`

## 5) Order Placement Checklist

When modifying orders, confirm:

- `Order(...)` parameters: `buy_sell`, `symbol`, `quantity`, `market_type`, `price_type`, `time_in_force`, `order_type`, `price`, `user_def`.
- `PriceType.Reference` is recommended in test env to discover reference price.
- `user_def` should be short (over 10 chars may be truncated/warned).
- Market type and order type must match the account (e.g., `OrderType.Stock` for stock accounts).

## 6) Callback Handling

If orders or market data are involved, check that callbacks are registered:

- `sdk.set_on_event`
- `sdk.set_on_order`
- `sdk.set_on_order_changed`
- `sdk.set_on_filled`

Missing callbacks often look like “silent success” without notifications.

## 7) Common Modification Pitfalls

- **Wrong environment URL** (prod vs test).
- **Wrong account type** (stock vs futopt).
- **Missing cert path / invalid cert password**.
- **Price limits** in test env (use reference price first).
- **Trading hours** (test env 09:30–19:00).
- **Python version**: SDK >= v2 supports 3.12–3.13, not 3.14.

## 8) When Changing Examples

When updating example code:

- Note SDK version and Python version.
- Keep examples minimal and runnable.
- Include a short “expected output” block when possible.
