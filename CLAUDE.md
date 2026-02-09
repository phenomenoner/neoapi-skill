# NeoAPI Python Skill Adapter (Claude)

本檔為 Claude 的入口說明；實際內容以下列檔案為準：

- `skills/neoapi-python/SKILL.md`（主流程）
- `skills/neoapi-python/references/doc-index.md`（文件索引）
- `skills/neoapi-python/references/test-environment.md`（測試環境）
- `skills/neoapi-python/references/examples-guidance.md`（範例程式理解與修改）
- `skills/neoapi-python/references/skill-tests.md`（驗證測試）

工作原則（zh-first）：

1) 優先使用線上 `llms.txt` / `llms-full.txt`，離線檔案作為 fallback。  
2) 若在測試環境下單，價格上下限以 `sdk.stock.query_symbol_quote` 為準。  
3) `intraday.quote` 偏即時成交資料；需查漲跌停請改用 `intraday.ticker`。  
4) 取消單後在 `get_order_results` 看到狀態 `30` 屬正常（代表已刪單）。  
5) 回覆以中文為主，必要時補英文術語（English supplement）。

English note:
Use the files above as the canonical source. Prefer online llms endpoints, and treat test-environment order validation rules as authoritative.
