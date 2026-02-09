# Skill Validation Tests

Use these tests to verify that an AI agent can apply the `neoapi-python` skill correctly after installation. Each test includes purpose, steps, and expected results. If a test fails, share the exact prompt, SDK version, Python version, and error output with the skill author.

## Test 1: Test Environment Login (Smoke)

**Purpose:** Confirm the agent can set up the test environment connection and log in.

**Steps:**

1) Install the SDK from the official wheel (not PyPI).
2) Use the test environment URL and credentials:
   - URL: `wss://neoapitest.fbs.com.tw/TASP/XCPXWS`
   - ID: from test certificate (e.g., `41610792.pfx` → `41610792`)
   - Login password: `12345678`
   - Cert password: `12345678`
3) Run a minimal script that logs in and prints accounts, then exits.

**Expected:**

- Login succeeds.
- Account list includes at least stock + futopt accounts.

## Test 2: Correct SDK Init Signature (Version Awareness)

**Purpose:** Ensure the agent selects the correct `FubonSDK` constructor for v2.2.0 vs v2.2.1+.

**Steps:**

1) Ask the agent how to initialize the SDK for test environment.
2) Verify it mentions both:
   - v2.2.0 and earlier: `FubonSDK(url=...)`
   - v2.2.1 and later: `FubonSDK(30, 2, url=...)`

**Expected:**

- The agent distinguishes the two signatures and explains when each applies.

## Test 3: SDK Install Guidance (Wheel Only)

**Purpose:** Confirm the agent does not recommend PyPI and points to the official wheel download.

**Steps:**

1) Ask: “How do I install the NeoAPI Python SDK?”

**Expected:**

- The agent says the SDK is not on PyPI.
- It provides the official download URL and a local install example (e.g., `uv pip install <wheel>`).

## Test 4: Market Data Reference Price Caveat

**Purpose:** Ensure the agent understands the test environment’s reference price caveat.

**Steps:**

1) Ask: “Why is my order rejected in the test environment?”

**Expected:**

- The agent mentions middle-office reference price lag and suggests using reference price first.

## Test 5: Order Placement + Callback

**Purpose:** Verify the agent can place a stock order in the test environment and handle order callbacks.

**Steps:**

1) Log in to the test environment with a stock account.
2) Register callbacks: `set_on_order`, `set_on_order_changed`, `set_on_filled`.
3) Place a stock order for `2881` (suggest `PriceType.Reference` first; fall back to `PriceType.Limit` with a reasonable price).
4) Wait briefly and confirm callback messages are received.

**Expected:**

- `place_order` returns success (or a clear error if outside test hours).
- At least one order-related callback prints a notification.

## Regression Suites (Local)

Use the local runner for repeatable integration checks (kept in `.test/`, not published in the skill bundle):

- Script: `.test/test_runner.py`
- Output:
  - text log: `.test/logs/test_runner_<suite>_<timestamp>.log`
  - JSON summary: `.test/logs/test_runner_<suite>_<timestamp>.json`

Recommended command:

```powershell
$env:NEOAPI_TEST_ID = "41610792"
$env:NEOAPI_TEST_CERT_PATH = "D:\path\to\41610792.pfx"
$env:NEOAPI_TEST_PASSWORD = "12345678"
$env:NEOAPI_TEST_CERT_PASSWORD = "12345678"
& .\.test\.venv\Scripts\python.exe .\.test\test_runner.py --suite all --symbol 2883
```

Suite intent:

- `smoke`: login + basic market/trade path
- `pre_1330`: emphasize realtime marketdata behavior
- `post_1330`: tolerate stale marketdata after realtime close
- `all`: full lifecycle (place/find/modify/cancel/verify + marketdata comparison)

## How to Contribute New Tests

When proposing a new test, include:

- **Name**: short title
- **Goal**: what the agent should do or explain
- **Prereqs**: SDK version, Python version, required files
- **Steps**: minimal, numbered
- **Expected**: clear pass/fail criteria
- **Artifacts**: logs, screenshots, or code snippets (if relevant)

Keep tests small and focused. Prefer one concept per test.

## Test Run Log (Local)

- 2026-01-26:
  - Test 1: Pass (login OK, accounts returned)
  - Test 2: Pass (constructed SDK with both signatures using SDK 2.2.7)
  - Test 3: Pass (PyPI resolution fails; wheel install required)
  - Test 4: Pass (validated against official test-environment PDF notes)
  - Test 5: Pass (order placed for 2881 with PriceType.Reference; order callback received; reference price returned 46)
    - Note: user_def length over 10 triggers a warning and is truncated by the system.
- 2026-02-09:
  - Runner: `.test/test_runner.py --suite all --symbol 2883`
  - Result: Pass (16 pass / 0 fail / 0 skip)
  - Log: `.test/logs/test_runner_all_20260209_131437.log`
  - JSON: `.test/logs/test_runner_all_20260209_131437.json`
  - Verified:
    - `intraday.ticker` vs `query_symbol_quote` price limits may differ (expected in test env).
    - Modify-below-limitdown is rejected with expected error path.
    - Canceled order remains visible in `get_order_results` with status `30`.
