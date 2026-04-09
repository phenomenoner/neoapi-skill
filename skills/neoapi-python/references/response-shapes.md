# 回傳格式參考（Response Shapes）

本文件記錄 SDK 主要方法的回傳結構。已驗證欄位標記 **[verified]**；待測試驗證標記 **[TODO]**。

> 驗證環境：SDK 2.2.8 + Python 3.13 + 測試環境（2026-04-09）

---

## sdk.login()

```python
response = sdk.login(user_id, password, cert_path, cert_password)
```

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `is_success` | `bool` | 登入是否成功 | [verified] |
| `message` | `str` | 失敗時的錯誤訊息 | [verified] |
| `data` | `list` | 帳號清單 | [verified] |
| `data[].account` | `str` | 帳號號碼 | [verified] |
| `data[].account_type` | `str` | `"stock"` 或 `"futopt"` | [verified] |
| `data[].branch_no` | `str` | 分公司代號 | [verified] |
| `data[].name` | `str` | 帳號名稱（注意：欄位為 `name`，非 `account_name`） | [verified] |

---

## sdk.stock.place_order()

```python
response = sdk.stock.place_order(account, order)
```

回傳 `data` 為完整 `OrderResult` 物件（與 `get_order_results` 回傳的單筆結構相同）。

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `is_success` | `bool` | 下單是否成功 | [verified] |
| `message` | `str\|None` | 失敗時的錯誤訊息；成功時為 `None` | [verified] |
| `data` | `OrderResult` | 完整委託結果物件（見 `get_order_results` 欄位表） | [verified] |
| `data.order_no` | `str` | 委託書號 | [verified] |
| `data.price` | `float` | 委託價格（注意：型別為 `float`，非 `str`） | [verified] |
| `data.quantity` | `int` | 委託股數 | [verified] |

> 下單失敗時（`is_success=False`），`data` 為 `None`，`message` 包含錯誤訊息。

---

## sdk.stock.get_order_results()

```python
response = sdk.stock.get_order_results(account)
```

回傳 `data` 為 `OrderResult` 物件清單，每筆包含以下欄位：

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `is_success` | `bool` | 是否成功 | [verified] |
| `data` | `list` | 委託清單 | [verified] |
| `data[].order_no` | `str` | 委託書號 | [verified] |
| `data[].seq_no` | `str` | 序號 | [verified] |
| `data[].stock_no` | `str` | 商品代號（注意：非 `symbol`） | [verified] |
| `data[].status` | `int` | 狀態碼（10=委託成功, 30=已刪單, 90=失敗） | [verified] |
| `data[].buy_sell` | `BSAction` | 買賣方向（`BSAction.Buy` / `BSAction.Sell`） | [verified] |
| `data[].price` | `float` | 委託價格 | [verified] |
| `data[].quantity` | `int` | 委託股數 | [verified] |
| `data[].filled_qty` | `int` | 已成交股數 | [verified] |
| `data[].filled_money` | `int` | 已成交金額 | [verified] |
| `data[].price_type` | `PriceType` | 價格類型 | [verified] |
| `data[].market_type` | `MarketType` | 市場類型 | [verified] |
| `data[].order_type` | `OrderType` | 委託類型 | [verified] |
| `data[].time_in_force` | `TimeInForce` | 有效期別 | [verified] |
| `data[].user_def` | `str` | 自訂標籤 | [verified] |
| `data[].account` | `str` | 帳號 | [verified] |
| `data[].branch_no` | `str` | 分公司代號 | [verified] |
| `data[].market` | `str` | 市場別（如 `"TAIEX"`） | [verified] |
| `data[].date` | `str` | 日期（如 `"2026/04/09"`） | [verified] |
| `data[].last_time` | `str` | 最後更新時間 | [verified] |
| `data[].unit` | `int` | 交易單位 | [verified] |
| `data[].is_pre_order` | `bool` | 是否為預約單 | [verified] |
| `data[].asset_type` | `int` | 資產類型 | [verified] |
| `data[].function_type` | `int` | 功能類型（0=新單, 15=改價, 30=刪單） | [verified] |
| `data[].after_price` | `float` | 改價後價格 | [verified] |
| `data[].after_price_type` | `PriceType` | 改價後價格類型 | [verified] |
| `data[].after_qty` | `int` | 改量後數量 | [verified] |
| `data[].before_price` | `float` | 改價前價格 | [verified] |
| `data[].before_qty` | `int` | 改量前數量 | [verified] |
| `data[].details` | `object\|None` | 明細 | [verified] |
| `data[].error_message` | `str\|None` | 錯誤訊息 | [verified] |

---

## sdk.stock.modify_price()

改價需要兩步驟：先建立 `ModifyPrice` 物件，再送出改價請求。

```python
modify_obj = sdk.stock.make_modify_price_obj(order_result, new_price)
# modify_obj = sdk.stock.make_modify_price_obj(order_result, new_price, new_price_type)
response = sdk.stock.modify_price(account, modify_obj)
```

### make_modify_price_obj 回傳

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `order_no` | `str` | 委託書號 | [verified] |
| `stock_no` | `str` | 商品代號 | [verified] |
| `date` | `str` | 日期 | [verified] |
| `new_price` | `str` | 新價格 | [verified] |
| `new_price_type` | `PriceType` | 新價格類型 | [verified] |
| `price_type` | `PriceType` | 原價格類型 | [verified] |
| `market_type` | `MarketType` | 市場類型 | [verified] |
| `txse` | `str` | 序號（同 `seq_no`） | [verified] |
| `asty` | `str` | 資產類型 | [verified] |

### modify_price 回傳

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `is_success` | `bool` | 改價是否成功 | [verified] |
| `message` | `str\|None` | 失敗時的錯誤訊息；成功時為 `None` | [verified] |
| `data` | `OrderResult` | 改價後的完整 `OrderResult`（`function_type=15`） | [verified] |
| `data.order_no` | `str` | 原委託書號 | [verified] |
| `data.after_price` | `float` | 改價後價格 | [verified] |
| `data.before_price` | `float` | 改價前價格 | [verified] |

---

## sdk.stock.modify_quantity()

改量需要兩步驟：先建立 `ModifyQuantity` 物件，再送出改量請求。

```python
modify_obj = sdk.stock.make_modify_quantity_obj(order_result, new_qty)
response = sdk.stock.modify_quantity(account, modify_obj)
```

### make_modify_quantity_obj 回傳

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `order_no` | `str` | 委託書號 | [verified] |
| `stock_no` | `str` | 商品代號 | [verified] |
| `date` | `str` | 日期 | [verified] |
| `new_quantity` | `int` | 新數量 | [verified] |
| `market_type` | `MarketType` | 市場類型 | [verified] |
| `txse` | `str` | 序號（同 `seq_no`） | [verified] |
| `asty` | `str` | 資產類型 | [verified] |

### modify_quantity 回傳

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `is_success` | `bool` | 改量是否成功 | [verified] |
| `message` | `str\|None` | 失敗時的錯誤訊息（如 `"Quantity must be multiply of 1000, input is 500"`）；成功時為 `None` | [verified] |
| `data` | `OrderResult\|None` | 成功時為改量後的完整 `OrderResult`；失敗時為 `None` | [verified] |

---

## sdk.stock.cancel_order()

```python
response = sdk.stock.cancel_order(account, order_result)
```

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `is_success` | `bool` | 刪單是否成功 | [verified] |
| `message` | `str\|None` | 失敗時的錯誤訊息（如 `"證券委託目前狀態取消單已不允許取消交易"`）；成功時為 `None` | [verified] |
| `data` | `OrderResult\|None` | 成功時為刪單後的完整 `OrderResult`（`function_type=30`, `status=30`）；失敗時為 `None` | [verified] |

> 刪單後該筆委託仍會出現在 `get_order_results` 中，status = `30`。

---

## sdk.stock.query_symbol_quote()

```python
response = sdk.stock.query_symbol_quote(account, symbol)
```

回傳 `data` 為 `SymbolQuote` 物件，欄位遠比原本文件記錄的多：

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `is_success` | `bool` | 是否成功 | [verified] |
| `message` | `str\|None` | 失敗時的錯誤訊息；成功時為 `None` | [verified] |
| `data.symbol` | `str` | 商品代號 | [verified] |
| `data.market` | `str` | 市場別（如 `"TAIEX"`） | [verified] |
| `data.market_type` | `MarketType` | 市場類型 | [verified] |
| `data.reference_price` | `float` | 參考價（確認欄位名為 `reference_price`） | [verified] |
| `data.limitup_price` | `float` | 漲停價（order system 端） | [verified] |
| `data.limitdown_price` | `float` | 跌停價（order system 端） | [verified] |
| `data.open_price` | `float` | 開盤價 | [verified] |
| `data.high_price` | `float` | 最高價 | [verified] |
| `data.low_price` | `float` | 最低價 | [verified] |
| `data.last_price` | `float` | 最新成交價 | [verified] |
| `data.last_size` | `int` | 最新成交量 | [verified] |
| `data.total_volume` | `int` | 累計成交量 | [verified] |
| `data.total_value` | `int` | 累計成交金額 | [verified] |
| `data.total_transaction` | `int` | 累計成交筆數 | [verified] |
| `data.last_transaction` | `int` | 最新成交筆數 | [verified] |
| `data.last_value` | `int` | 最新成交金額 | [verified] |
| `data.bid_price` | `float` | 最佳買價 | [verified] |
| `data.bid_volume` | `int` | 最佳買量 | [verified] |
| `data.ask_price` | `float` | 最佳賣價 | [verified] |
| `data.ask_volume` | `int` | 最佳賣量 | [verified] |
| `data.unit` | `int` | 交易單位 | [verified] |
| `data.status` | `int` | 狀態 | [verified] |
| `data.istib_or_psb` | `bool` | 是否為 TIB/PSB | [verified] |
| `data.update_time` | `str` | 更新時間 | [verified] |

> 測試環境中此為判斷可下單價格區間的權威來源。

---

## sdk.marketdata.rest_client.stock.intraday.quote()

```python
sdk.init_realtime()
result = sdk.marketdata.rest_client.stock.intraday.quote(symbol=symbol)
```

回傳為 `dict`。

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `date` | `str` | 日期（如 `"2026-04-09"`） | [verified] |
| `type` | `str` | 資料類型（如 `"EQUITY"`） | [verified] |
| `exchange` | `str` | 交易所（如 `"TWSE"`） | [verified] |
| `market` | `str` | 市場別（如 `"TSE"`） | [verified] |
| `symbol` | `str` | 商品代號 | [verified] |
| `name` | `str` | 商品名稱 | [verified] |
| `referencePrice` | `float` | 參考價 | [verified] |
| `previousClose` | `float` | 前收盤價 | [verified] |
| `openPrice` | `float` | 開盤價 | [verified] |
| `highPrice` | `float` | 最高價 | [verified] |
| `lowPrice` | `float` | 最低價 | [verified] |
| `closePrice` | `float` | 收盤價 | [verified] |
| `lastPrice` | `float` | 最新成交價 | [verified] |
| `lastSize` | `int` | 最新成交量 | [verified] |
| `bids` | `list` | 買方五檔（`[{price, size}, ...]`） | [verified] |
| `asks` | `list` | 賣方五檔（`[{price, size}, ...]`） | [verified] |
| `total` | `dict` | 累計統計（`tradeValue`, `tradeVolume`, `tradeVolumeAtBid`, `tradeVolumeAtAsk`, `transaction`, `time`） | [verified] |
| `lastTrade` | `dict` | 最後成交明細（`bid`, `ask`, `price`, `size`, `time`, `serial`） | [verified] |
| `lastTrial` | `dict` | 最後試撮明細（結構同 `lastTrade`） | [verified] |
| `change` | `float` | 漲跌 | [verified] |
| `changePercent` | `float` | 漲跌幅 | [verified] |
| `amplitude` | `float` | 振幅 | [verified] |
| `avgPrice` | `float` | 均價 | [verified] |
| `isClose` | `bool` | 是否已收盤 | [verified] |
| `serial` | `int` | 序號 | [verified] |
| `lastUpdated` | `int` | 最後更新時間（microseconds） | [verified] |

> 注意：此為**成交行情**資料（prod market data）。測試環境下此資料來自正式行情，不代表測試環境的可下單價格範圍。

---

## sdk.marketdata.rest_client.stock.intraday.ticker()

```python
result = sdk.marketdata.rest_client.stock.intraday.ticker(symbol=symbol)
```

回傳為 `dict`。

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `date` | `str` | 日期 | [verified] |
| `type` | `str` | 資料類型（如 `"EQUITY"`） | [verified] |
| `exchange` | `str` | 交易所（如 `"TWSE"`） | [verified] |
| `market` | `str` | 市場別（如 `"TSE"`） | [verified] |
| `symbol` | `str` | 商品代號 | [verified] |
| `name` | `str` | 商品名稱 | [verified] |
| `industry` | `str` | 產業代號 | [verified] |
| `securityType` | `str` | 證券類型代號 | [verified] |
| `previousClose` | `float` | 前收盤價 | [verified] |
| `referencePrice` | `float` | 參考價 | [verified] |
| `limitUpPrice` | `float` | 漲停價（market data 端） | [verified] |
| `limitDownPrice` | `float` | 跌停價（market data 端） | [verified] |
| `canDayTrade` | `bool` | 是否可當沖（現股當沖-賣） | [verified] |
| `canBuyDayTrade` | `bool` | 是否可現股當沖-買 | [verified] |
| `canBelowFlatMarginShortSell` | `bool` | 是否可平盤下融券賣出 | [verified] |
| `canBelowFlatSBLShortSell` | `bool` | 是否可平盤下借券賣出 | [verified] |
| `isAttention` | `bool` | 是否為注意股 | [verified] |
| `isDisposition` | `bool` | 是否為處置股 | [verified] |
| `isUnusuallyRecommended` | `bool` | 是否為異常推介股 | [verified] |
| `isSpecificAbnormally` | `bool` | 是否為特定異常標的 | [verified] |
| `matchingInterval` | `int` | 撮合間隔（秒） | [verified] |
| `securityStatus` | `str` | 證券狀態（如 `"NORMAL"`） | [verified] |
| `boardLot` | `int` | 交易單位（如 `1000`） | [verified] |
| `tradingCurrency` | `str` | 交易幣別（如 `"TWD"`） | [verified] |

> 注意：`limitUpPrice` / `limitDownPrice` 為 market data 端的值。在測試環境中可能與 `query_symbol_quote` 的結果不同。

---

## Callback: on_order / on_order_changed

```python
def on_order(code, content):
    # Triggered on new order placement
def on_order_changed(code, content):
    # Triggered on order modification or cancellation
```

callback 的 `content` 為 `OrderResult` 物件，與 `get_order_results` 回傳的結構相同。

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `code` | `None\|str` | 正常為 `None`；異常時為錯誤訊息字串（如 `"[115]證券委託目前狀態取消單已不允許取消交易"`） | [verified] |
| `content.order_no` | `str` | 委託書號 | [verified] |
| `content.stock_no` | `str` | 商品代號（注意：非 `symbol`） | [verified] |
| `content.status` | `int` | 狀態碼（10=成功, 30=已刪單） | [verified] |
| `content.buy_sell` | `BSAction` | 買賣方向 | [verified] |
| `content.price` | `float` | 委託價格 | [verified] |
| `content.quantity` | `int` | 委託股數 | [verified] |
| `content.user_def` | `str` | 自訂標籤 | [verified] |
| `content.after_price` | `float` | 改價後價格（on_order_changed） | [verified] |
| `content.after_qty` | `int` | 改量後數量（on_order_changed） | [verified] |

---

## Callback: on_filled

```python
def on_filled(code, content):
    # code: None, content: FillResult object
```

`content` 為 `FillResult` 物件（**非** `OrderResult`），結構與委託回報不同。

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `code` | `None` | 回報代碼（實測固定為 `None`） | [verified] |
| `content.order_no` | `str` | 委託書號 | [verified] |
| `content.stock_no` | `str` | 商品代號（注意：非 `symbol`） | [verified] |
| `content.buy_sell` | `BSAction` | 買賣方向 | [verified] |
| `content.filled_no` | `str` | 成交編號 | [verified] |
| `content.filled_price` | `float` | 成交價 | [verified] |
| `content.filled_qty` | `int` | 成交數量 | [verified] |
| `content.filled_avg_price` | `float` | 成交均價 | [verified] |
| `content.filled_time` | `str` | 成交時間（如 `"15:28:33.602"`） | [verified] |
| `content.order_type` | `OrderType` | 委託類型 | [verified] |
| `content.user_def` | `str` | 自訂標籤 | [verified] |
| `content.account` | `str` | 帳號 | [verified] |
| `content.branch_no` | `str` | 分公司代號 | [verified] |
| `content.seq_no` | `str` | 序號 | [verified] |
| `content.date` | `str` | 日期 | [verified] |

---

## Callback: on_event

```python
def on_event(code, content):
    # code: str, content: str
```

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `code` | `str` | 事件代碼（注意：型別為 `str`，非 `int`） | [verified] |
| `content` | `str` | 事件訊息 | [verified] |

常見事件代碼：

| code | 說明 |
| :--- | :--- |
| `"100"` | connected |
| `"200"` | logged in |
| `"201"` | 登入警告（如密碼過期提醒） |
| `"300"` | disconnected |

---

## 常見錯誤訊息

| 情境 | `is_success` | `message` |
| :--- | :--- | :--- |
| 數量非 1000 倍數 | `False` | `"Quantity must be multiply of 1000, input is {n}"` |
| 價格超出漲跌停 | `False` | `"單價輸入錯誤[4385715]"` |
| 重複刪單 | `False` | `"證券委託目前狀態取消單已不允許取消交易"` |

> 錯誤時 `data` 為 `None`。callback 中的 `code` 會包含錯誤代碼（如 `"[4385715]單價輸入錯誤[4385715]"`、`"[115]證券委託目前狀態取消單已不允許取消交易"`）。

---

## 貢獻指南

如果你透過測試環境或正式環境驗證了 `[TODO]` 欄位：

1. 將狀態改為 `[verified]`
2. 修正欄位名稱、型別、說明（如有出入）
3. 在 PR 或 commit message 中註明驗證環境（SDK 版本、Python 版本、日期）
