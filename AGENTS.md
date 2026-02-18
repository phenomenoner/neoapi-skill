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
- `skills/neoapi-python/references/response-shapes.md`

## Required Behavior

1. Chinese-first responses; English as supplement for API terms and enums.
2. Prefer online LLM docs endpoints; use bundled `llms*.txt` only when offline/unavailable.
3. For test-environment order limits, use `sdk.stock.query_symbol_quote`.
4. `intraday.ticker` is for limit-up/limit-down in market data; `intraday.quote` is trade-oriented.
5. In `get_order_results`, status `30` means canceled order and can remain visible.

## 文件查詢（Using llms.txt）

優先使用公開 URL 為主要來源，bundled 檔案作為離線 fallback：

- Public:
  - <https://www.fbs.com.tw/TradeAPI/llms.txt>
  - <https://www.fbs.com.tw/TradeAPI/llms-full.txt>
  - <https://www.fbs.com.tw/TradeAPI/en/llms.txt>
  - <https://www.fbs.com.tw/TradeAPI/en/llms-full.txt>
- Bundled (offline):
  - `llms.txt` / `llms-full.txt`
  - `llms.en.txt` / `llms-full.en.txt`

使用 `llms.txt` 做導覽，`llms-full.txt` 查精確參數與範例。

## 語言與術語（Language & Localization）

- **Source of Truth**: 主要文件 `llms-full.txt` 為**繁體中文**。
- **回覆風格**:
  - 使用者用中文提問 → 中文回覆，程式碼註解用英文。
  - 使用者用英文提問 → 英文回覆，括號補充中文術語（e.g., "ROD (當日有效)"）。
- **術語對照**:
  - **Limit Order**: 限價 (LMT)
  - **Market Order**: 市價 (MKT)
  - **ROD**: 當日有效
  - **IOC**: 立即成交否則取消
  - **FOK**: 全部成交否則取消
  - **Margin Trading**: 融資
  - **Short Selling**: 融券
  - **Day Trade**: 當沖

## Maintenance Rule

When `skills/neoapi-python/` changes, update this adapter and `CLAUDE.md` / `GEMINI.md` in the same commit.
