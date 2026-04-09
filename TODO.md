# TODO — neoapi-python skill

上次更新：2026-04-09（beta.28）

---

## ~~1. Response Shapes 驗證~~ ✅ 已完成

`references/response-shapes.md` 所有欄位已驗證完畢（beta.28）。

重大修正：

- `place_order()` 回傳完整 `OrderResult`（非僅 `order_no`），`price` 為 `float`（非 `str`）
- `modify_price()` / `modify_quantity()` 需先呼叫 `make_modify_price_obj` / `make_modify_quantity_obj`（API 簽名已修正）
- `cancel_order()` 回傳完整 `OrderResult`
- `query_symbol_quote()` 回傳完整 `SymbolQuote`（25 個欄位），`reference_price` 欄位名正確
- `on_filled` callback 的 `content` 為 `FillResult`（非 `OrderResult`），含 `filled_avg_price`、`filled_no`、`filled_time` 等欄位
- `on_event` 的 `code` 為 `str`（非 `int`）
- `login()` 帳號名稱欄位為 `name`（非 `account_name`），另有 `branch_no`
- `intraday.quote()` 額外欄位：`total`, `lastTrade`, `lastTrial`, `avgPrice`, `change`, `changePercent` 等
- `intraday.ticker()` 額外欄位：`industry`, `securityType`, `canBelowFlatMarginShortSell` 等

---

## ~~2. Error / Status Code 知識庫~~ ✅ 已完成

`implementation-practices.md` 的 3 個 TODO 已全部補完（beta.28）：

- [x] 訂單狀態碼：10=委託成功, 30=已刪單, 90=委託失敗
- [x] 數量不符規則：`"Quantity must be multiply of 1000, input is {n}"`
- [x] 重複刪單：`"證券委託目前狀態取消單已不允許取消交易"`
- [x] 超出價格範圍：`"單價輸入錯誤[4385715]"`

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

- [x] 反向單配對成交（兩筆反向委託撮合）— beta.28 驗證成功（`on_filled` callback 觸發）
- [ ] 部分成交情境
- [ ] 不同 `MarketType`（`IntradayOdd` 盤中零股、`Odd` 盤後零股）行為
- [ ] 不同 `TimeInForce`（`IOC`、`FOK`）測試
- [ ] 融資 / 融券下單流程（`MarginTrading`、`ShortSelling`）

---

## 6. Skill 內容持續改善

- [ ] 期貨 / 選擇權（Futures & Options）工作流程：如有社群貢獻或需求，補充 futopt 下單/行情範例
- [ ] 條件單（ConditionOrder / TPSL）完整範例：目前僅在 §當沖 提及，可補獨立章節
- [ ] `.skill` archive 重新打包：beta.28 內容變更後需重建 `neoapi-python.skill`

---

## 7. 跨代理驗證

- [ ] 在 Gemini（Google AI Studio / Antigravity）上安裝 skill 並跑 Tier 1–2
- [ ] 在 OpenAI Codex 上安裝 skill 並跑 Tier 1–2
- [ ] 記錄各代理的差異與改善建議

---

## 優先順序建議

| 優先 | 項目 | 依賴 | 狀態 |
| :--- | :--- | :--- | :--- |
| ~~**P0**~~ | ~~#1 Response Shapes 驗證~~ | ~~測試環境~~ | ✅ beta.28 |
| ~~**P0**~~ | ~~#2 Error Code 知識庫~~ | ~~測試環境~~ | ✅ beta.28 |
| **P1** | #3 Effectiveness 測試（Tier 1-2, 4-5） | 無（可隨時跑） | |
| **P1** | #3 Effectiveness 測試（Tier 3, B5） | 測試環境 | |
| **P2** | #4 13:30 後行情 | 測試環境（13:30 後） | |
| **P2** | #5 更多交易情境 | 測試環境 | |
| **P3** | #6 Skill 內容改善 | 社群需求 | |
| **P3** | #7 跨代理驗證 | 各平台 access | |
