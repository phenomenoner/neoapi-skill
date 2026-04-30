# Migrating from Shioaji to Fubon Neo

This note is for developers who already have working **Shioaji** code and want to port the same trading workflow to **Fubon Neo Python SDK**. Keep the migration mechanical: identify the old Shioaji pattern, map the account/order/quote behavior, then verify against official Fubon docs and the bundled `llms-full.txt` before running live.

> Migration posture: this is a compatibility aid for existing codebases, not a broker comparison. Do not imply equivalent behavior unless it is verified in current Neo SDK docs or in this skill's reference notes.

## First warnings to check

| Topic | Migration rule |
| :--- | :--- |
| Environment | Shioaji often uses `simulation=True`; Neo uses SDK constructor / endpoint configuration. Test and production data can differ. See `test-environment.md`. |
| Quantity | Shioaji examples commonly express regular stock orders in lots; Neo stock `quantity` is **shares**. 1 regular lot = 1000 shares. |
| Account | Shioaji code often uses `api.stock_account`; Neo login returns account objects and you should choose the intended stock account explicitly. |
| Modify / cancel | Do not reuse a stale local object blindly. Query current order results and pass the current order object / modify object. |
| Source of truth | Use official Fubon docs, bundled `llms-full.txt`, `response-shapes.md`, and `implementation-practices.md`; mark uncertain mappings as `TODO verify`. |

## Task routing

| If the user asks to... | Load / check |
| :--- | :--- |
| Port Shioaji login / CA code | This file → [Auth / CA](#auth--ca) |
| Port stock order placement | This file → [Orders](#orders) + `implementation-practices.md` |
| Map Shioaji constants | [Constant mapping table](#constant-mapping-table) |
| Port modify / cancel logic | [Order lifecycle](#order-lifecycle) + `response-shapes.md` |
| Port quote callbacks / subscriptions | [Market data and callbacks](#market-data-and-callbacks) + `examples-guidance.md` |
| Explain test vs production mismatch | `test-environment.md` |
| Verify exact return fields | `response-shapes.md` |

## Core conceptual differences

| Feature | Shioaji | Fubon Neo |
| :--- | :--- | :--- |
| Entry point | `import shioaji as sj`; `api = sj.Shioaji(...)` | `from fubon_neo.sdk import FubonSDK`; `sdk = FubonSDK(...)` |
| Login / cert | `api.login(...)` then `api.activate_ca(...)` | `sdk.login(id, pwd, cert_path, cert_pwd)` returns accounts |
| Account | Often `api.stock_account` | Select an account object from `accounts.data` |
| Contract / symbol | `api.Contracts.Stocks["2330"]` contract object | Stock orders commonly pass `symbol="2330"` |
| Order object | `api.Order(...)` | `Order(...)` from `fubon_neo.sdk` |
| Place order | `api.place_order(contract, order)` | `sdk.stock.place_order(account, order)` |
| Status tracking | `Trade` object + `api.update_status(...)` | Query order results and match by order number / stock fields |
| Realtime shape | Typed callback objects | WebSocket / callback envelopes; check event/data shape |

## Auth / CA

### Shioaji pattern

```python
import shioaji as sj

api = sj.Shioaji(simulation=True)
api.login("API_KEY", "SECRET")
api.activate_ca("path/to/cert.pfx", "CA_PWD")
account = api.stock_account
```

### Neo pattern

```python
from fubon_neo.sdk import FubonSDK

# SDK 2.2.1+ examples in this skill usually use FubonSDK(30, 2).
# For test environment, pass the documented test URL; see test-environment.md.
sdk = FubonSDK(30, 2)
accounts = sdk.login("ID", "PWD", "path/to/cert.pfx", "CA_PWD")

# Pick the intended stock account explicitly. Do not assume index 0 is always right.
# response-shapes.md verifies account_type is usually "stock" or "futopt".
stock_accounts = [acc for acc in accounts.data if getattr(acc, "account_type", "") == "stock"]
acc = stock_accounts[0] if stock_accounts else accounts.data[0]
```

If account fields are uncertain in a user's SDK version, inspect `accounts.data` and the official account docs instead of inventing field names.

## Orders

### Shioaji regular-stock example

```python
contract = api.Contracts.Stocks["2330"]
order = api.Order(
    price=580,
    quantity=1,  # common Shioaji regular-lot code: 1 lot
    action=sj.constant.Action.Buy,
    price_type=sj.constant.StockPriceType.LMT,
    order_type=sj.constant.OrderType.ROD,
    order_lot=sj.constant.StockOrderLot.Common,
    account=api.stock_account,
)
trade = api.place_order(contract, order)
```

### Neo regular-stock equivalent

```python
from fubon_neo.sdk import Order
from fubon_neo.constant import BSAction, MarketType, PriceType, TimeInForce, OrderType

order = Order(
    buy_sell=BSAction.Buy,
    symbol="2330",
    quantity=1000,                 # Neo uses shares: 1000 shares = 1 regular lot
    market_type=MarketType.Common,
    price_type=PriceType.Limit,
    time_in_force=TimeInForce.ROD,
    order_type=OrderType.Stock,
    price="580",
)
res = sdk.stock.place_order(acc, order)
```

Before placing a test-environment order, prefer `sdk.stock.query_symbol_quote(acc, symbol)` for valid order prices. In production examples, `intraday.ticker` may be useful for display/reference prices, but order validity should still be checked against the trading-side behavior documented for the current environment.

## Constant mapping table

| Intent | Shioaji | Fubon Neo |
| :--- | :--- | :--- |
| Buy | `sj.constant.Action.Buy` | `BSAction.Buy` |
| Sell | `sj.constant.Action.Sell` | `BSAction.Sell` |
| Limit price | `sj.constant.StockPriceType.LMT` | `PriceType.Limit` |
| Market price | `sj.constant.StockPriceType.MKT` | `PriceType.Market` |
| ROD | `sj.constant.OrderType.ROD` | `TimeInForce.ROD` |
| IOC | `sj.constant.OrderType.IOC` | `TimeInForce.IOC` |
| FOK | `sj.constant.OrderType.FOK` | `TimeInForce.FOK` |
| Regular lot | `sj.constant.StockOrderLot.Common` | `MarketType.Common` with quantity in shares |
| Intraday odd lot | `sj.constant.StockOrderLot.IntradayOdd` | `MarketType.IntradayOdd` |
| Cash stock | commonly implicit in stock order | `OrderType.Stock` |
| Margin / short | Shioaji constants vary by order intent | Check Neo `OrderType.MarginTrading` / `OrderType.ShortSelling` examples before use |

## Order lifecycle

Shioaji code often keeps a `trade` object and calls `api.update_status(trade)`. Neo examples should prefer a query-before-action pattern.

```python
def find_order(sdk, acc, order_no: str):
    results = sdk.stock.get_order_results(acc)
    if not results.data:
        return None
    return next((o for o in results.data if getattr(o, "order_no", None) == order_no), None)

# Place
place_res = sdk.stock.place_order(acc, order)
order_no = place_res.data.order_no

# Query current state before modify/cancel
current = find_order(sdk, acc, order_no)
if current is None:
    raise RuntimeError(f"order_not_found:{order_no}")

# Modify price / quantity: build the SDK modify object first.
modify_price_obj = sdk.stock.make_modify_price_obj(current, "579")
modify_res = sdk.stock.modify_price(acc, modify_price_obj)

# Re-query before cancel to avoid stale local state.
current = find_order(sdk, acc, order_no)
if current is not None:
    cancel_res = sdk.stock.cancel_order(acc, current)
```

For exact fields and return shapes, use `response-shapes.md`; do not assume Shioaji `Trade.status` names carry over.

## Market data and callbacks

### Shioaji callback style

```python
@api.on_quote
def quote_callback(topic, quote):
    print(topic, quote)

api.quote.subscribe(api.Contracts.Stocks["2330"])
```

### Neo callback / market-data posture

```python
sdk.init_realtime()

# Trading callbacks are set on the SDK; see implementation-practices.md / examples-guidance.md.
def on_filled(code, content):
    print(code, content)

sdk.set_on_filled(on_filled)

# Market data examples often use REST client snapshots or WebSocket envelopes.
quote = sdk.marketdata.rest_client.stock.intraday.quote(symbol="2330")
```

For WebSocket message parsing, do not read trade fields from the top-level envelope. Check event type first and read payload fields from `message["data"]` when applicable. If porting Shioaji's `on_tick` / `on_bidask` style code, verify the Neo market-data channel and message schema from official docs before writing production logic.

## Scope notes

- This file is stock/cash-equity focused unless another reference has verified futures/options behavior.
- Do not port futures/options/combo Shioaji examples by analogy alone.
- For every migration row, prefer `[verified]` examples from existing references; if not verified, label it `TODO verify`.
