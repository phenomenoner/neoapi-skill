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

## Credentials

- **Test account ID** = the ID shown on the test certificate.
- **Login password** = `12345678`.
- **Certificate password** = `12345678`.

## Behavior Notes

- You can test market data and order placement after login.
- Because this is a shared test account, account balances are **not** real and may look incorrect.
- Test inventory is pre-seeded and **resets daily** (no carry-over after trades).

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

## Trade Testing Tips

- To simulate a fill, submit two opposite orders.
- Use `user_def` to distinguish your orders in the shared account.

## Trading Session (Test)

- Open hours: **09:30–19:00**.
