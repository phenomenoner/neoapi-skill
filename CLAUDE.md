# NeoAPI Python Skill Adapter (Claude)

本檔為 Claude 的入口說明；實際內容以下列檔案為準：

- `skills/neoapi-python/SKILL.md`（主流程）
- `skills/neoapi-python/references/doc-index.md`（文件索引）
- `skills/neoapi-python/references/test-environment.md`（測試環境）
- `skills/neoapi-python/references/examples-guidance.md`（範例程式理解與修改）
- `skills/neoapi-python/references/skill-tests.md`（驗證測試）
- `skills/neoapi-python/references/response-shapes.md`（回傳格式參考）

工作原則（zh-first）：

1) 優先使用線上 `llms.txt` / `llms-full.txt`，離線檔案作為 fallback。
2) 若在測試環境下單，價格上下限以 `sdk.stock.query_symbol_quote` 為準。
3) `intraday.quote` 偏即時成交資料；需查漲跌停請改用 `intraday.ticker`。
4) 取消單後在 `get_order_results` 看到狀態 `30` 屬正常（代表已刪單）。
5) 回覆以中文為主，必要時補英文術語（English supplement）。

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

使用 `llms.txt` 做導覽，`llms-full.txt` 查精確參數與範例。若檔案缺失或過時，回退至 `docs/` 來源文件。

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
Use the files above as the canonical source. Prefer online llms endpoints, and treat test-environment order validation rules as authoritative.
