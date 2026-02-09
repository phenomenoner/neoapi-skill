# NeoAPI Python Skill Adapter (Gemini)

此檔用於 Gemini 專案上下文導引；核心內容請讀：

- `skills/neoapi-python/SKILL.md`
- `skills/neoapi-python/references/doc-index.md`
- `skills/neoapi-python/references/test-environment.md`
- `skills/neoapi-python/references/examples-guidance.md`
- `skills/neoapi-python/references/skill-tests.md`

執行重點（Chinese-first）：

- 先確認環境（test/prod）、Python 版本（3.12–3.13）、SDK 版本（2.x）。
- 文件查詢優先線上：
  - `https://www.fbs.com.tw/TradeAPI/llms.txt`
  - `https://www.fbs.com.tw/TradeAPI/llms-full.txt`
  - `https://www.fbs.com.tw/TradeAPI/en/llms.txt`
  - `https://www.fbs.com.tw/TradeAPI/en/llms-full.txt`
- 測試環境價格判斷以 `query_symbol_quote` 為主，不要用 `intraday.quote` 判定可下單價格。
- 回覆語氣：中文為主，英文補充術語與 API 名稱。

English note:
Treat this file as an adapter only; canonical implementation guidance lives under `skills/neoapi-python/`.
