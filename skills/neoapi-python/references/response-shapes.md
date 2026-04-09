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
| `data[].account_name` | `str` | 帳號名稱 | [TODO] |

---

## sdk.stock.place_order()

```python
response = sdk.stock.place_order(account, order)
```

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `is_success` | `bool` | 下單是否成功 | [verified] |
| `message` | `str` | 失敗時的錯誤訊息 | [verified] |
| `data.order_no` | `str` | 委託書號 | [verified] |
| `data.price` | `str` | 委託價格 | [TODO: verify format] |
| `data.quantity` | `int` | 委託股數 | [TODO] |

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
| `data[].price` | `str` | 委託價格 | [verified] |
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
| `data[].function_type` | `str\|None` | 功能類型 | [verified] |
| `data[].after_price` | `str\|None` | 改價後價格 | [verified] |
| `data[].after_price_type` | `str\|None` | 改價後價格類型 | [verified] |
| `data[].after_qty` | `int` | 改量後數量 | [verified] |
| `data[].before_price` | `str\|None` | 改價前價格 | [verified] |
| `data[].before_qty` | `str\|None` | 改量前數量 | [verified] |
| `data[].details` | `object\|None` | 明細 | [verified] |
| `data[].error_message` | `str\|None` | 錯誤訊息 | [verified] |

---

## sdk.stock.modify_price()

```python
response = sdk.stock.modify_price(account, order_result, new_price)
```

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `is_success` | `bool` | 改價是否成功 | [verified] |
| `message` | `str` | 失敗時的錯誤訊息（如超出漲跌停） | [verified] |
| `data.order_no` | `str` | 原委託書號 | [TODO] |

---

## sdk.stock.modify_quantity()

```python
response = sdk.stock.modify_quantity(account, order_result, new_qty)
```

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `is_success` | `bool` | 改量是否成功 | [verified] |
| `message` | `str` | 失敗時的錯誤訊息 | [TODO] |

---

## sdk.stock.cancel_order()

```python
response = sdk.stock.cancel_order(account, order_result)
```

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `is_success` | `bool` | 刪單是否成功 | [verified] |
| `message` | `str` | 失敗時的錯誤訊息 | [TODO] |

> 刪單後該筆委託仍會出現在 `get_order_results` 中，status = `30`。

---

## sdk.stock.query_symbol_quote()

```python
response = sdk.stock.query_symbol_quote(account, symbol)
```

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `is_success` | `bool` | 是否成功 | [verified] |
| `data.limitup_price` | `float` | 漲停價（order system 端） | [verified] |
| `data.limitdown_price` | `float` | 跌停價（order system 端） | [verified] |
| `data.reference_price` | `float` | 參考價 | [TODO: verify field name] |

> 測試環境中此為判斷可下單價格區間的權威來源。

---

## sdk.marketdata.rest_client.stock.intraday.quote()

```python
sdk.init_realtime()
result = sdk.marketdata.rest_client.stock.intraday.quote(symbol=symbol)
```

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `date` | `str` | 日期 | [TODO] |
| `type` | `str` | 資料類型 | [TODO] |
| `exchange` | `str` | 交易所 | [TODO] |
| `symbol` | `str` | 商品代號 | [TODO] |
| `name` | `str` | 商品名稱 | [TODO] |
| `referencePrice` | `float` | 參考價 | [TODO] |
| `previousClose` | `float` | 前收盤價 | [TODO] |
| `openPrice` | `float` | 開盤價 | [TODO] |
| `highPrice` | `float` | 最高價 | [TODO] |
| `lowPrice` | `float` | 最低價 | [TODO] |
| `closePrice` | `float` | 收盤價（或最新成交價） | [TODO] |
| `lastPrice` | `float` | 最新成交價 | [TODO] |
| `lastSize` | `int` | 最新成交量 | [TODO] |
| `totalVolume` | `int` | 累計成交量 | [TODO] |
| `bids` | `list` | 買方五檔 | [TODO] |
| `asks` | `list` | 賣方五檔 | [TODO] |

> 注意：此為**成交行情**資料（prod market data）。測試環境下此資料來自正式行情，不代表測試環境的可下單價格範圍。

---

## sdk.marketdata.rest_client.stock.intraday.ticker()

```python
result = sdk.marketdata.rest_client.stock.intraday.ticker(symbol=symbol)
```

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `symbol` | `str` | 商品代號 | [TODO] |
| `referencePrice` | `float` | 參考價 | [verified] |
| `limitUpPrice` | `float` | 漲停價（market data 端） | [verified] |
| `limitDownPrice` | `float` | 跌停價（market data 端） | [verified] |
| `canDayTrade` | `bool` | 是否可當沖 | [TODO: verify] |
| `canBuyDayTrade` | `bool` | 是否可現股當沖-買 | [TODO: verify] |

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
| `code` | `None\|int` | 回報代碼（實測為 `None`） | [verified] |
| `content.order_no` | `str` | 委託書號 | [verified] |
| `content.stock_no` | `str` | 商品代號（注意：非 `symbol`） | [verified] |
| `content.status` | `int` | 狀態碼（10=成功, 30=已刪單） | [verified] |
| `content.buy_sell` | `BSAction` | 買賣方向 | [verified] |
| `content.price` | `str` | 委託價格 | [verified] |
| `content.quantity` | `int` | 委託股數 | [verified] |
| `content.user_def` | `str` | 自訂標籤 | [verified] |
| `content.after_price` | `str\|None` | 改價後價格（on_order_changed） | [verified] |
| `content.after_qty` | `int` | 改量後數量（on_order_changed） | [verified] |

---

## Callback: on_filled

```python
def on_filled(code, content):
    # code: int, content: object
```

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `code` | `int` | 回報代碼 | [TODO] |
| `content.order_no` | `str` | 委託書號 | [TODO] |
| `content.stock_no` | `str` | 商品代號（注意：非 `symbol`） | [TODO: inferred from OrderResult pattern] |
| `content.filled_price` | `float` | 成交價 | [TODO] |
| `content.filled_qty` | `int` | 成交數量 | [TODO] |
| `content.user_def` | `str` | 自訂標籤 | [TODO] |

---

## Callback: on_event

```python
def on_event(code, content):
    # code: int, content: str
```

| 欄位 | 型別 | 說明 | 狀態 |
| :--- | :--- | :--- | :--- |
| `code` | `int` | 事件代碼 | [verified] |
| `content` | `str` | 事件訊息 | [verified] |

常見事件代碼：

| code | 說明 |
| :--- | :--- |
| 100 | connected |
| 200 | logged in |
| 201 | 登入警告（如密碼過期提醒） |
| 300 | disconnected |

---

## 貢獻指南

如果你透過測試環境或正式環境驗證了 `[TODO]` 欄位：

1. 將狀態改為 `[verified]`
2. 修正欄位名稱、型別、說明（如有出入）
3. 在 PR 或 commit message 中註明驗證環境（SDK 版本、Python 版本、日期）
