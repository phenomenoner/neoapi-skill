# Skill Effectiveness Test Suite

本文件定義一套分層測試，用以衡量 `neoapi-python` skill 對 AI 代理的實際幫助程度。測試分為五個 Tier（層級），由淺到深，從「知識是否正確」到「能否建構交易系統」。

> **核心方法：Ablation（消融）測試** — 每個 Tier 的測試都應**有 skill** vs **無 skill** 各跑一次，兩次結果的正確率差距即為 skill 的量化價值。

---

## 測試方法論

### Ablation 設計

每位受測代理（Claude Code、Gemini、Codex、OpenClaw 等）分兩組：

| 組別 | 條件 | 目的 |
| :--- | :--- | :--- |
| **Control（對照組）** | 不安裝 skill，僅提供「請用 Fubon Neo Python SDK 回答」提示 | 測量代理的 baseline 能力 |
| **Treatment（實驗組）** | 安裝 skill（SKILL.md + references/） | 測量 skill 的增量效果 |

### 計分方式

每個測試案例的判定結果為以下之一：

| 結果 | 分數 | 定義 |
| :--- | :--- | :--- |
| **Pass** | 1 | 完全滿足 Expected 中所有條件 |
| **Partial** | 0.5 | 滿足部分條件，但有關鍵遺漏或小錯誤 |
| **Fail** | 0 | 主要條件未滿足或產出不可用的程式碼 |

### 報告格式

每次執行後產出一份結果表：

```
| Test ID | Tier | Control | Treatment | Delta | Notes |
|---------|------|---------|-----------|-------|-------|
| K1      | 1    | 0       | 1         | +1    | Control suggested pip install |
| ...     |      |         |           |       |       |
```

**Skill Value Score** = `sum(Treatment) - sum(Control)` / `total_tests`

---

## Tier 1: Knowledge Retrieval（知識回取）

> 代理是否能回答關於 SDK 的事實性問題？不需要執行程式碼。

### K1: SDK 安裝方式

- **Prompt**: `"How do I install the Fubon Neo Python SDK?"`
- **Expected**:
  - [ ] 明確說明 SDK **不在 PyPI** 上
  - [ ] 提供官方下載頁面 URL 或提及從官方網站下載 `.whl`
  - [ ] 給出安裝指令範例（如 `uv pip install <wheel>` 或 `pip install <wheel>`）
- **Skill section tested**: SKILL.md §常見錯誤、§SDK Install

### K2: `intraday.quote` vs `intraday.ticker` 差異

- **Prompt**: `"What is the difference between intraday.quote and intraday.ticker in the Fubon Neo SDK?"`
- **Expected**:
  - [ ] `intraday.quote` — 即時成交/報價資料
  - [ ] `intraday.ticker` — 參考價、漲跌停價、`canDayTrade` 等
  - [ ] 在測試環境下，下單價格應使用 `query_symbol_quote` 而非兩者
- **Skill section tested**: SKILL.md §Validating Prices、§常見錯誤

### K3: 測試環境初始化

- **Prompt**: `"How do I connect to the Fubon Neo test environment using SDK 2.2.7?"`
- **Expected**:
  - [ ] 使用 `FubonSDK(30, 2, url="wss://neoapitest.fbs.com.tw/TASP/XCPXWS")`
  - [ ] 提到測試密碼為 `12345678`
  - [ ] 提到 cert ID 作為登入帳號
- **Skill section tested**: SKILL.md §SDK 版本相容性、§Testing / Sandbox

### K4: 下單被拒原因

- **Prompt**: `"My limit order was rejected in the Fubon Neo test environment. What might be wrong?"`
- **Expected**:
  - [ ] 提到測試環境的中台參考價可能與正式行情不同
  - [ ] 建議使用 `sdk.stock.query_symbol_quote` 取得有效價格範圍
  - [ ] 提到交易時段限制（09:30–19:00）
- **Skill section tested**: SKILL.md §常見錯誤、references/test-environment.md

### K5: 當沖知識（beta.23 新增）

- **Prompt**: `"How do I check if a Taiwan stock can be day-traded using Fubon Neo SDK?"`
- **Expected**:
  - [ ] 提到 `intraday.ticker` 的 `canDayTrade` / `canBuyDayTrade` 欄位
  - [ ] 區分先買後賣（`OrderType.Stock`）與先賣後買（`OrderType.ShortSelling`）
  - [ ] 提到收盤前需反向沖銷
- **Skill section tested**: SKILL.md §當沖

### K6: 版本差異認知（beta.23 新增）

- **Prompt**: `"What changed between Fubon Neo SDK 2.2.0 and 2.2.6 in terms of error handling?"`
- **Expected**:
  - [ ] SDK < 2.2.6：錯誤資訊在 response 物件中
  - [ ] SDK >= 2.2.6：拋出 `FugleAPIError` 例外
  - [ ] 提到 `FugleAPIError` 有 `status_code` 和 `response_text` 屬性
- **Skill section tested**: SKILL.md §版本相容性、implementation-practices.md §10

---

## Tier 2: Code Generation（程式碼生成）

> 代理是否能產出語法正確、邏輯正確的 SDK 呼叫程式碼？

### C1: 登入 + 限價買單

- **Prompt**: `"Write a Python script to login to Fubon Neo test environment and place a limit buy order for 1000 shares of 2330 at price 580."`
- **Expected**:
  - [ ] 正確 import（`FubonSDK`, `Order`, constants）
  - [ ] 使用 `FubonSDK(30, 2, url=...)` 搭配測試 URL
  - [ ] Order 使用 keyword form（`buy_sell=BSAction.Buy, symbol="2330", quantity=1000, ...`）
  - [ ] 數量為 1000（股數，非 1 張）
  - [ ] 設定 callbacks（`set_on_order` 或 `set_on_event`）再登入，或至少登入後立即設定
  - [ ] 呼叫 `sdk.stock.place_order(acc, order)`
- **Skill section tested**: SKILL.md §Quickstart、§常見錯誤

### C2: 多標的 WebSocket 訂閱（>200）

- **Prompt**: `"I need to subscribe to real-time trade data for 350 symbols. How should I manage the WebSocket connections?"`
- **Expected**:
  - [ ] 提到 200 subscriptions/connection 的限制
  - [ ] 建議使用多條 WebSocket 連線
  - [ ] 提供 load-balancing 分配邏輯（或至少提到需要分批）
  - [ ] 提到 `sdk.init_realtime()` 作為連線起點
- **Skill section tested**: implementation-practices.md §2 WebSocket Management

### C3: `user_def` 追蹤下單

- **Prompt**: `"Show me how to tag orders with a custom identifier and then find them in order results."`
- **Expected**:
  - [ ] Order 中設定 `user_def="my_tag"` 參數
  - [ ] 在 `get_order_results` 中用 `user_def` 過濾
  - [ ] 提到 `user_def` 建議 10 字元以內
- **Skill section tested**: implementation-practices.md §5、SKILL.md §常見錯誤

### C4: Shioaji 遷移

- **Prompt**:
  ```
  Convert this Shioaji code to Fubon Neo:

  import shioaji as sj
  api = sj.Shioaji()
  api.login("KEY", "SECRET")
  contract = api.Contracts.Stocks["2330"]
  order = api.Order(price=580, quantity=1, action=sj.constant.Action.Buy,
                    price_type=sj.constant.StockPriceType.LMT,
                    order_type=sj.constant.OrderType.ROD)
  api.place_order(contract, order)
  ```
- **Expected**:
  - [ ] 正確對應常數（`Action.Buy` → `BSAction.Buy`，`StockPriceType.LMT` → `PriceType.Limit`，`OrderType.ROD` → `TimeInForce.ROD`）
  - [ ] 不使用 contract 物件（FubonNeo 直接傳 symbol 字串）
  - [ ] 數量轉換正確（Shioaji 的 1 lot → FubonNeo 的 1000 shares）
  - [ ] 使用 `sdk.login(id, pwd, cert, cert_pwd)` 取代 `api.login(key, secret)` + `activate_ca`
- **Skill section tested**: references/migration-shioaji.md

### C5: 回傳格式處理（beta.23 新增）

- **Prompt**: `"After placing an order, how do I check if it succeeded and extract the order number? Show the response handling code."`
- **Expected**:
  - [ ] 檢查 `response.is_success`
  - [ ] 成功時取 `response.data.order_no`
  - [ ] 失敗時讀取 `response.message`
  - [ ] 提到 SDK >= 2.2.6 可能拋出 `FugleAPIError`
- **Skill section tested**: references/response-shapes.md、implementation-practices.md §10

### C6: 價格驗證程式碼（beta.23 新增）

- **Prompt**: `"Write code that fetches the valid order price range for a symbol in the test environment before placing a limit order."`
- **Expected**:
  - [ ] 使用 `sdk.stock.query_symbol_quote(acc, symbol)` 取得價格範圍
  - [ ] 讀取 `limitup_price` 和 `limitdown_price`
  - [ ] 在下單前驗證委託價在範圍內
  - [ ] 不使用 `intraday.quote` 作為價格來源
- **Skill section tested**: SKILL.md §Validating Prices、references/response-shapes.md

---

## Tier 3: Integration（整合能力）

> 代理是否能將多個 SDK 功能串接成完整的工作流程？需要測試環境執行（09:30–19:00）。

### I1: SDKManager 類別

- **Prompt**: `"Create an SDKManager class for the Fubon Neo SDK that handles login, reconnection, and graceful shutdown."`
- **Expected**:
  - [ ] 包含 login 方法，儲存 credentials 供重連使用
  - [ ] 在 login **前**設定 callbacks（`set_on_event`, `set_on_filled` 等）
  - [ ] graceful termination：先移除 listeners → 斷開 WS → logout
  - [ ] 使用 `ThreadPoolExecutor` 包裝 blocking calls（或至少提到需要）
- **Skill section tested**: implementation-practices.md §1、§4
- **Needs test env**: Yes（驗證 login 成功）

### I2: 價格監控警報

- **Prompt**: `"Build a script that monitors the price of 2330 via WebSocket and prints an alert when the last price drops below a threshold."`
- **Expected**:
  - [ ] 呼叫 `sdk.init_realtime()` 建立 WS 連線
  - [ ] 訂閱即時行情（WebSocket 或 polling `intraday.quote`）
  - [ ] 條件判斷正確（last price < threshold）
  - [ ] 正確處理行情回傳格式
- **Skill section tested**: SKILL.md §Market Data Workflow、implementation-practices.md §2
- **Needs test env**: Yes（驗證 WS 連線與資料接收）

### I3: 下單 → 等待 Callback → 刪單

- **Prompt**: `"Write a script that places an order in the test environment, waits for the order callback, then cancels the order and verifies it was canceled."`
- **Expected**:
  - [ ] 設定 `set_on_order` callback
  - [ ] 下單後等待 callback 觸發
  - [ ] 使用 `get_order_results` 找到該筆委託
  - [ ] 呼叫 `cancel_order`
  - [ ] 驗證 status = 30
- **Skill section tested**: SKILL.md §常見錯誤（status 30）、references/examples-guidance.md §6
- **Needs test env**: Yes

### I4: 行情矩陣比較（beta.23 新增）

- **Prompt**: `"For symbols 2881, 2883, and 2330, fetch both the market data limit prices (intraday.ticker) and the order-system limit prices (query_symbol_quote). Show them side-by-side."`
- **Expected**:
  - [ ] 先 `sdk.init_realtime()` 再使用 `rest_client`
  - [ ] 兩種 API 都正確呼叫
  - [ ] 展示 prod vs test 價格差異
  - [ ] 提到差異屬預期行為（測試環境已知 caveat）
- **Skill section tested**: SKILL.md §Validating Prices、references/test-environment.md
- **Needs test env**: Yes

---

## Tier 4: Trading Bot（策略系統建構）

> 代理是否能基於 StrategyExecutor 的架構，修改或擴展交易策略？以 [StrategyExecutor_feather](https://github.com/phenomenoner/StrategyExecutor_feather) 為基礎。

### B1: 新增追蹤停損

- **Prompt**: `"Add a trailing stop loss to this trading strategy. When the profit exceeds 2%, set a trailing stop that triggers when the price drops 1% from the peak."`
- **Context**: 提供 StrategyExecutor_feather 的 strategy 核心邏輯
- **Expected**:
  - [ ] 正確追蹤每個持倉的最高價
  - [ ] 計算回撤百分比
  - [ ] 觸發時下反向委託（`BSAction.Sell` 或 `BSAction.Buy`）
  - [ ] 使用 per-symbol lock 防止競爭
  - [ ] 不破壞既有的 entry/exit 邏輯
- **Skill section tested**: implementation-practices.md §9 Strategy Pattern、§4 Async
- **Needs test env**: Optional（邏輯驗證可離線；執行驗證需 test env）

### B2: 擴展監控標的

- **Prompt**: `"The bot currently watches 50 symbols. I want to expand to 250 symbols. What changes are needed?"`
- **Expected**:
  - [ ] 提到 200 subscriptions/connection 限制
  - [ ] 建議新增第二條 WS 連線
  - [ ] 提供 load-balancing 邏輯或分批訂閱方案
  - [ ] 考慮 per-symbol lock 的記憶體影響
  - [ ] 不建議在單一連線中訂閱超過 200
- **Skill section tested**: implementation-practices.md §2 WebSocket
- **Needs test env**: Optional

### B3: 委託記錄到 CSV

- **Prompt**: `"Add logging so that every order placed by the bot (buy or sell) is appended to a CSV file with timestamp, symbol, action, price, quantity, and order_no."`
- **Expected**:
  - [ ] 在 `on_order` 或 `on_filled` callback 中寫入
  - [ ] 不阻塞 event loop（使用非同步寫入或 queue）
  - [ ] CSV 欄位正確對應 callback 回傳的 field names
  - [ ] 正確處理 `user_def` 以區分 bot 的單
- **Skill section tested**: implementation-practices.md §5 Order Management、references/response-shapes.md
- **Needs test env**: Optional

### B4: 風控限制

- **Prompt**: `"Add a risk control: each symbol can have at most 3 orders per minute. If the limit is exceeded, skip the signal."`
- **Expected**:
  - [ ] 在策略層（非 SDK 層）實作速率限制
  - [ ] Per-symbol 計數器（sliding window 或 token bucket）
  - [ ] 不依賴 SDK 的 REST rate limit（300 req/min 是全域的，此為策略層控制）
  - [ ] 與 per-symbol lock 正確互動
- **Skill section tested**: implementation-practices.md §9 Strategy Pattern、§6 REST Best Practices
- **Needs test env**: Optional

### B5: 當沖流程實作（beta.23 新增）

- **Prompt**: `"Write a day trading workflow: check if 2881 is eligible for day trading, place a short sell order in the morning, then place a buy-to-cover order in the afternoon."`
- **Expected**:
  - [ ] 使用 `intraday.ticker` 檢查 `canDayTrade`
  - [ ] 先賣：`BSAction.Sell` + `OrderType.ShortSelling`
  - [ ] 後買：`BSAction.Buy` + `OrderType.Stock`（或對應的回補方式）
  - [ ] 提到收盤前需完成沖銷
  - [ ] 使用 `query_symbol_quote` 取得有效價格範圍
- **Skill section tested**: SKILL.md §當沖、references/response-shapes.md
- **Needs test env**: Yes

---

## Tier 5: Cross-Agent Consistency（跨代理一致性）

> 不同代理在相同 skill 下是否產出一致的結果？

### X1: 同 Prompt 跨代理比較

- **方法**: 選取 Tier 2 中的 C1（登入+買單）與 C4（Shioaji 遷移），分別在 Claude Code、Gemini、Codex 上執行。
- **Expected**:
  - [ ] 三個代理都使用 keyword form Order
  - [ ] 三個代理都正確設定數量為股數
  - [ ] 三個代理都使用正確的 SDK 初始化方式
- **紀錄**: 每位代理的輸出逐項對比，標記差異點。

### X2: 版本陷阱測試

- **Prompt**: `"Initialize FubonSDK for the test environment. I'm using SDK version 2.2.0."`
- **Expected**:
  - [ ] 代理使用 `FubonSDK(url=...)` 而非 `FubonSDK(30, 2, url=...)`
  - [ ] 代理主動說明此為舊版語法，建議升級到 2.2.1+
- **Skill section tested**: SKILL.md §版本相容性

### X3: 語言切換測試

- **Prompt A** (中文): `"請幫我寫一個程式，登入富邦 Neo 測試環境並下一張 2330 的限價買單。"`
- **Prompt B** (英文): `"Write a script to login to Fubon Neo test environment and place a limit buy order for 2330."`
- **Expected**:
  - [ ] 兩種語言產出的程式碼邏輯一致
  - [ ] 中文回覆包含英文 API 名稱
  - [ ] 英文回覆包含中文術語補充（如 "ROD (當日有效)"）
- **Skill section tested**: adapter files §語言與術語

---

## 測試執行清單

### 不需要測試環境的測試（可隨時執行）

| Test ID | Tier | 類型 | 預估時間 |
| :--- | :--- | :--- | :--- |
| K1–K6 | 1 | 問答 | 每題 1 min |
| C1–C6 | 2 | 程式碼審查 | 每題 3 min |
| B1–B4 | 4 | 程式碼審查 | 每題 5 min |
| X1–X3 | 5 | 跨代理 | 每題 5 min |

### 需要測試環境的測試（09:30–19:00）

| Test ID | Tier | 類型 | 預估時間 |
| :--- | :--- | :--- | :--- |
| I1–I4 | 3 | 執行驗證 | 每題 10 min |
| B5 | 4 | 執行驗證 | 15 min |

### 額外效益：Response Shapes 填補

在執行 Tier 3 測試時，同步擷取 API 回傳結構並更新 `references/response-shapes.md` 中的 `[TODO]` 欄位。具體步驟：

1. 在每個 API 呼叫後印出 `type(response)`, `dir(response)`, `vars(response)` 或 `response.__dict__`
2. 對照 `response-shapes.md` 中的欄位表
3. 將 `[TODO]` 改為 `[verified]`，修正型別與欄位名稱
4. Commit 更新

---

## 結果範本

以下為空白結果模板，執行時填入：

```markdown
## Test Run: [日期] — [代理名稱] — [with/without skill]

| Test ID | Tier | Score | Notes |
| :--- | :--- | :--- | :--- |
| K1 | 1 | _ /1 | |
| K2 | 1 | _ /1 | |
| K3 | 1 | _ /1 | |
| K4 | 1 | _ /1 | |
| K5 | 1 | _ /1 | |
| K6 | 1 | _ /1 | |
| C1 | 2 | _ /1 | |
| C2 | 2 | _ /1 | |
| C3 | 2 | _ /1 | |
| C4 | 2 | _ /1 | |
| C5 | 2 | _ /1 | |
| C6 | 2 | _ /1 | |
| I1 | 3 | _ /1 | (test env required) |
| I2 | 3 | _ /1 | (test env required) |
| I3 | 3 | _ /1 | (test env required) |
| I4 | 3 | _ /1 | (test env required) |
| B1 | 4 | _ /1 | |
| B2 | 4 | _ /1 | |
| B3 | 4 | _ /1 | |
| B4 | 4 | _ /1 | |
| B5 | 4 | _ /1 | (test env required) |
| X1 | 5 | _ /1 | |
| X2 | 5 | _ /1 | |
| X3 | 5 | _ /1 | |
| **Total** | | _ /23 | |

### Skill Value Score

- Control (no skill): _ /23
- Treatment (with skill): _ /23
- **Delta**: _
- **Skill Effectiveness**: _ %
```

---

## 與現有測試的關係

本文件與 `skill-tests.md` 互補：

| 文件 | 用途 | 誰執行 |
| :--- | :--- | :--- |
| `skill-tests.md` | 驗證 skill 內容是否正確（SDK 功能測試） | 人類 + 測試環境 |
| `skill-effectiveness-tests.md`（本文件） | 衡量 skill 對 AI 代理的幫助程度 | AI 代理（被測者）+ 人類（評分者） |
| `.test/test_runner.py` | 自動化回歸測試 | 自動執行 |
