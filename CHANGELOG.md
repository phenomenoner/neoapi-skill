# Changelog — neoapi-skill / neoapi-python

This changelog is a **minimal index** derived from the version notes already present in `README.md`.
If details diverge, treat `README.md` + `skills/neoapi-python/VERSION` as the source of truth.

## 1.0.0-beta.28 — 2026-04-09

- **All `response-shapes.md` fields now verified** — zero `[TODO]` remaining.
- `place_order()` / `modify_price()` / `cancel_order()`: return full `OrderResult` (not just `order_no` / `is_success`).
- `modify_price()` / `modify_quantity()`: corrected API signature — must call `make_modify_price_obj()` / `make_modify_quantity_obj()` first.
- `on_filled` callback: `content` is `FillResult` (not `OrderResult`), with `filled_avg_price`, `filled_no`, `filled_time`.
- `on_event` callback: `code` is `str` (not `int`).
- `login()`: account name field is `name` (not `account_name`); also has `branch_no`.
- `query_symbol_quote()`: fully documented all 25 `SymbolQuote` fields; confirmed `reference_price` field name.
- `intraday.quote()`: added `total`, `lastTrade`, `lastTrial`, `change`, `changePercent`, `avgPrice`, etc.
- `intraday.ticker()`: added `industry`, `securityType`, `canBelowFlatMarginShortSell`, `boardLot`, etc.
- `implementation-practices.md`: filled in order status codes (10/30/90) and error messages for invalid quantity, out-of-range price, and duplicate cancel.
- Added error message reference table to `response-shapes.md`.

## 1.0.0-beta.27 — 2026-04-09

- Fixed field name errors in `response-shapes.md`: trading `OrderResult` uses `stock_no` (not `symbol`) for stock identifier.
- Expanded `get_order_results` section with all 30 fields, verified against SDK 2.2.8 + Python 3.13.
- Verified and documented callback fields for `on_order`, `on_order_changed`, and `on_event`.
- Added `on_event` reference section with common event codes (100/200/201/300).

## 1.0.0-beta.26 — 2026-03-31

- Updated doc access notes: `.md` URLs deprecated; use `.txt` suffix for plain-text access under `/TradeAPI/docs/` and `/TradeAPI/en/docs/`.

## 1.0.0-beta.25 — 2026-03-31

- Fixed Python SDK download link: replaced 4 incorrect `/docs/sdk/python/download?type=download` URLs (returning 403) with correct `/docs/download/download-sdk`.

## 1.0.0-beta.24 — 2026-03-26

- Refreshed bundled official `llms.txt` / `llms-full.txt` snapshots for both zh and en variants.
- Updated `README.md` / `README.en.md` to document the llms snapshot refresh rule and the need to bump `VERSION` when bundled snapshots change.
- Bumped `skills/neoapi-python/VERSION` and `SKILL.md` to `1.0.0-beta.24` so update scripts can deliver the refresh.

## 1.0.0-beta.23 — 2026-02-18

- Restructured `SKILL.md` for higher agent reliability (TL;DR, error table, decision tree).
- Expanded response-shape references, day-trade workflow notes, and status/error code tables.
- Moved localization rules into per-agent adapter docs.

## 1.0.0-beta.20 — 2026-02-09

- Added multi-agent root adapters (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`).

## 1.0.0-beta.1 — 2026-01-26

- Initial beta: update scripts, VERSIONing, install guidance.

## Notes

Intermediate betas exist and are recorded in `README.md`; they are not duplicated here.
