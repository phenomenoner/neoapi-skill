# 測試案例總覽（截至 2026-02-09）

此文件整理目前已實際執行過的 `neoapi-python` skill 相關測試，方便維護者與社群快速確認覆蓋範圍與已知行為。

## 一、環境與安裝驗證

1. **測試環境登入（Smoke）**
   - 驗證項目：`sdk.login` 可成功登入並取得帳號資料
   - 結果：通過
   - 備註：回傳至少包含股票與期貨帳號（依測試帳號狀態）

2. **SDK 初始化簽名版本差異**
   - 驗證項目：
     - v2.2.0(含)以前：`FubonSDK(url=...)`
     - v2.2.1(含)以後：`FubonSDK(30, 2, url=...)`
   - 結果：通過

3. **SDK 安裝來源**
   - 驗證項目：確認 SDK 非 PyPI，需使用官方 wheel 安裝
   - 結果：通過

## 二、行情資料（Market Data）驗證

4. **行情連線初始化**
   - 驗證項目：登入後 `sdk.init_realtime()`，再使用 `sdk.marketdata.rest_client.stock`
   - 結果：通過

5. **`intraday.quote` / `intraday.ticker` / `query_symbol_quote` 差異**
   - 驗證項目：
     - `intraday.quote` 屬於即時成交資訊
     - 漲跌停應使用 `intraday.ticker`（prod 行情）
     - 測試環境下單價位應以 `sdk.stock.query_symbol_quote` 為準
   - 結果：通過
   - 關鍵觀察：測試環境價位與行情來源（prod）可能不同，屬預期行為

6. **多標的行情矩陣（2881 / 2883 / 2330）**
   - 驗證項目：同次測試抓取多檔商品的 prod/test 漲跌停價，確認流程穩定
   - 結果：通過

7. **無效代號拒絕（`ZZZZ`）**
   - 驗證項目：`query_symbol_quote` 對無效商品代號應回拒絕（`is_success=False` 或例外）
   - 結果：通過

## 三、交易流程（Order Lifecycle）驗證

8. **單筆訂單完整生命週期**
   - 驗證項目：
     - 下單（3000）
     - 查單
     - 改量（2000）
     - 改價到跌停
     - 刪單
     - 驗證狀態
   - 結果：通過
   - 證據：
     - `.test/logs/integrated_order_lifecycle_20260127_110637.log`
     - `.test/logs/integrated_order_lifecycle_20260127_112119.log`

9. **跌停以下改價拒絕**
   - 驗證項目：將委託價改到低於跌停一檔，應回失敗
   - 結果：通過

10. **刪單後狀態判讀**
   - 驗證項目：刪單後 `get_order_results` 仍可能查到該筆，且狀態為 `30`
   - 結果：通過
   - 關鍵觀察：`status=30` 代表已刪單，並非資料清單中「完全消失」

11. **雙訂單進階整合流程**
   - 驗證項目：
     - 第一筆完整生命週期
     - 第二筆由跌停改價至漲停
     - 最終刪單並驗證狀態
   - 結果：通過
   - 證據：
     - `.test/logs/test_runner_complex_20260209_132554.log`
     - `.test/logs/test_runner_all_20260209_132527.log`

12. **Callback 覆蓋**
   - 驗證項目：`set_on_order` / `set_on_order_changed` / `set_on_filled` 事件收取
   - 結果：通過
   - 關鍵觀察：下單、改量、改價、刪單均可收到對應 callback

## 四、Runner 測試結果摘要

1. `test_runner_all_20260209_131437`
   - 結果：`16 pass / 0 fail / 0 skip`
   - 商品：`2883`

2. `test_runner_complex_20260209_132554`
   - 結果：`25 pass / 0 fail / 0 skip`
   - 商品：`2883`

3. `test_runner_all_20260209_132527`
   - 結果：`25 pass / 0 fail / 0 skip`
   - 商品：`2881`

## 五、仍建議持續補強的方向

1. **13:30 後行情行為**
   - 補充 `post_1330` 針對 stale snapshot 的固定化驗證腳本與紀錄

2. **更多交易情境**
   - 例如：反向單配對成交、部分成交、不同 `MarketType` 與 `TimeInForce` 行為

3. **錯誤碼知識庫**
   - 累積常見錯誤碼與對應處理建議（如單價輸入錯誤、權限/連線相關）
