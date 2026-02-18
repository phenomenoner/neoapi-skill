# NeoAPI Python Skill Adapter (Gemini)

此檔用於 Gemini 專案上下文導引；核心內容請讀：

- `skills/neoapi-python/SKILL.md`
- `skills/neoapi-python/references/doc-index.md`
- `skills/neoapi-python/references/test-environment.md`
- `skills/neoapi-python/references/examples-guidance.md`
- `skills/neoapi-python/references/skill-tests.md`
- `skills/neoapi-python/references/response-shapes.md`

執行重點（Chinese-first）：

- 先確認環境（test/prod）、Python 版本（3.12–3.13）、SDK 版本（2.x）。
- 文件查詢優先線上：
  - `https://www.fbs.com.tw/TradeAPI/llms.txt`
  - `https://www.fbs.com.tw/TradeAPI/llms-full.txt`
  - `https://www.fbs.com.tw/TradeAPI/en/llms.txt`
  - `https://www.fbs.com.tw/TradeAPI/en/llms-full.txt`
- Bundled（離線 fallback）：`llms.txt` / `llms-full.txt` / `llms.en.txt` / `llms-full.en.txt`
- 使用 `llms.txt` 做導覽，`llms-full.txt` 查精確參數與範例。
- 測試環境價格判斷以 `query_symbol_quote` 為主，不要用 `intraday.quote` 判定可下單價格。
- 回覆語氣：中文為主，英文補充術語與 API 名稱。

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

English note:
Treat this file as an adapter only; canonical implementation guidance lives under `skills/neoapi-python/`.
