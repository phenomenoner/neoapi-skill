# TODO — neoapi-python skill

上次更新：2026-02-18（beta.23）

---

## 1. Response Shapes 驗證（需測試環境 09:30–19:00）

`references/response-shapes.md` 中有 **42 個 [TODO] 欄位**待驗證。在測試環境中執行 API 呼叫，印出回傳結構後逐一確認。

### 高優先（交易流程核心）

- [ ] `sdk.stock.place_order()` — `data.price` 格式、`data.quantity`
- [ ] `sdk.stock.get_order_results()` — `buy_sell`、`symbol`、`price`、`quantity`、`filled_qty` 欄位名稱與型別
- [ ] `sdk.stock.modify_price()` — `data.order_no`
- [ ] `sdk.stock.modify_quantity()` — `message`
- [ ] `sdk.stock.cancel_order()` — `message`
- [ ] `sdk.stock.query_symbol_quote()` — `reference_price` 欄位名稱

### 中優先（行情資料）

- [ ] `intraday.quote()` — 全部 16 個欄位（date, type, exchange, prices, bids, asks 等）
- [ ] `intraday.ticker()` — `symbol`, `canDayTrade`, `canBuyDayTrade`

### 中優先（Callbacks）

- [ ] `on_filled` callback — `code`, `content.order_no`, `content.symbol`, `content.filled_price`, `content.filled_qty`, `content.user_def`
- [ ] `on_order` / `on_order_changed` callback — `code`, `content.status`, `content.user_def`

### 低優先

- [ ] `sdk.login()` — `data[].account_name`

### 驗證方法

```python
# 在每個 API 呼叫後加這段，擷取完整結構
import json
response = sdk.stock.place_order(acc, order)
print(type(response))
print(vars(response) if hasattr(response, '__dict__') else response)
if hasattr(response, 'data') and response.data:
    print(type(response.data))
    print(vars(response.data) if hasattr(response.data, '__dict__') else response.data)
```

---

## 2. Error / Status Code 知識庫（需測試環境）

`implementation-practices.md` §10 有 **3 個 [TODO]**：

- [ ] 訂單狀態碼：補充 status 30 以外的常見狀態（如「已成交」「部分成交」等）
- [ ] 數量不符規則的 exact error message
- [ ] 重複刪單的 error 行為

### 收集方法

在測試環境中故意觸發各種錯誤情境：
- 下單數量非 1000 倍數
- 對已刪的單再刪一次
- 超出漲跌停價格下單
- 非交易時段下單
- 觀察各情境的 `is_success`、`message`、`FugleAPIError` 內容

---

## 3. Skill Effectiveness 測試執行

`references/skill-effectiveness-tests.md` 定義了 23 個測試，分五個 Tier。

### 可立即執行（不需測試環境）— 17 tests

- [ ] Tier 1（K1–K6）：知識回取測試 — 在 Claude Code **有/無 skill** 下各跑一次
- [ ] Tier 2（C1–C6）：程式碼生成 — 審查產出程式碼正確性
- [ ] Tier 4（B1–B4）：策略修改 — 基於 StrategyExecutor_feather 的擴展測試
- [ ] Tier 5（X1–X3）：跨代理一致性 — 至少在 Claude + Gemini 上測試

### 需測試環境（09:30–19:00）— 5 tests

- [ ] Tier 3（I1–I4）：整合測試 — SDKManager、價格監控、下單生命週期、行情矩陣
- [ ] Tier 4（B5）：當沖流程執行驗證

### 產出

- [ ] 填寫結果模板（skill-effectiveness-tests.md 底部）
- [ ] 計算 Skill Value Score（Treatment - Control delta）

---

## 4. 13:30 後行情行為驗證

- [ ] 補充 `post_1330` suite 的驗證紀錄：在 13:30 之後執行 `intraday.quote` / `intraday.ticker`，確認 stale snapshot 行為
- [ ] 更新 `tested-cases.zh.md` 紀錄結果

---

## 5. 更多交易情境覆蓋

- [ ] 反向單配對成交（兩筆反向委託撮合）
- [ ] 部分成交情境
- [ ] 不同 `MarketType`（`IntradayOdd` 盤中零股、`Odd` 盤後零股）行為
- [ ] 不同 `TimeInForce`（`IOC`、`FOK`）測試
- [ ] 融資 / 融券下單流程（`MarginTrading`、`ShortSelling`）

---

## 6. Skill 內容持續改善

- [ ] 期貨 / 選擇權（Futures & Options）工作流程：如有社群貢獻或需求，補充 futopt 下單/行情範例
- [ ] 條件單（ConditionOrder / TPSL）完整範例：目前僅在 §當沖 提及，可補獨立章節
- [ ] `.skill` archive 重新打包：beta.23 內容變更後需重建 `neoapi-python.skill`

---

## 7. 跨代理驗證

- [ ] 在 Gemini（Google AI Studio / Antigravity）上安裝 skill 並跑 Tier 1–2
- [ ] 在 OpenAI Codex 上安裝 skill 並跑 Tier 1–2
- [ ] 記錄各代理的差異與改善建議

---

## 優先順序建議

| 優先 | 項目 | 依賴 |
| :--- | :--- | :--- |
| **P0** | #1 Response Shapes 驗證 | 測試環境 |
| **P0** | #2 Error Code 知識庫 | 測試環境 |
| **P1** | #3 Effectiveness 測試（Tier 1-2, 4-5） | 無（可隨時跑） |
| **P1** | #3 Effectiveness 測試（Tier 3, B5） | 測試環境 |
| **P2** | #4 13:30 後行情 | 測試環境（13:30 後） |
| **P2** | #5 更多交易情境 | 測試環境 |
| **P3** | #6 Skill 內容改善 | 社群需求 |
| **P3** | #7 跨代理驗證 | 各平台 access |
