# Migrating from Shioaji to FubonNeo

This guide helps developers migrate trading logic from **Sinotrade Shioaji (Shioaji)** to **Fubon Neo (fubon_neo)**.

## Core Conceptual Differences

| Feature | Shioaji (SinoPac) | FubonNeo (Fubon) |
| :--- | :--- | :--- |
| **Entry Point** | `import shioaji as sj` `api = sj.Shioaji()` | `from fubon_neo.sdk import FubonSDK` `sdk = FubonSDK()` |
| **Login** | `api.login(key, secret)` Separate `api.activate_ca(...)` | `sdk.login(id, pwd, cert_path, cert_pwd)` All-in-one authentication. |
| **Order Object** | `api.Order(...)` | `sdk.stock.Order(...)` |
| **Place Order** | `api.place_order(contract, order)` | `sdk.stock.place_order(account, order)` |
| **Contracts** | `api.Contracts.Stocks["2330"]` | Pass raw string `"2330"` directly. |

## Quick Translation

### 1. Initialization & Login

#### Shioaji (Init)

```python
import shioaji as sj
api = sj.Shioaji()
api.login("API_KEY", "SECRET")
api.activate_ca("path/to/cert.pfx", "CA_PWD")
```

#### FubonNeo (Init)

```python
from fubon_neo.sdk import FubonSDK
sdk = FubonSDK()
# Login returns all accounts immediately
accounts = sdk.login("ID", "PWD", "path/to/cert.pfx", "CA_PWD")
active_acc = accounts.data[0]
```

### 2. Placing a Limit Buy Order

#### Shioaji (Order)

```python
contract = api.Contracts.Stocks["2330"]
order = api.Order(
    price=580,
    quantity=1, # 1 unit = 1 share or 1 lot depending on config? 
                # Shioaji uses 1 = 1 share for IntradayOdd?
    action=sj.constant.Action.Buy,
    price_type=sj.constant.StockPriceType.LMT,
    order_type=sj.constant.OrderType.ROD,
    order_lot=sj.constant.StockOrderLot.Common, 
    account=api.stock_account
)
api.place_order(contract, order)
```

#### FubonNeo (Order)

```python
from fubon_neo.sdk import Order
from fubon_neo.constant import BSAction, PriceType, TimeInForce, MarketType, OrderType

order = Order(
    BSAction.Buy,
    "2330",
    1000,              # FubonNeo quantity is always SHARES. 3000 = 3 lots.
    MarketType.Common, # Specify lot type here
    PriceType.Limit,
    TimeInForce.ROD,
    OrderType.Stock,
    price="580"
)
sdk.stock.place_order(active_acc, order)
```

> **Important**: FubonNeo `quantity` is always in **shares**. Shioaji may vary by `order_lot` context, but Fubon is explicit.
>
> - 1 Lot (MarketType.Common) = 1000 shares.
> - 1 Share (MarketType.IntradayOdd) = 1 share.
> In FubonNeo `Order(..., 1000, MarketType.Common)` means 1000 shares (1 lot).

## Constant Mapping Table

| Value Type | Shioaji (`sj.constant`) | FubonNeo (`fubon_neo.constant`) |
| :--- | :--- | :--- |
| **Buy** | `Action.Buy` | `BSAction.Buy` |
| **Sell** | `Action.Sell` | `BSAction.Sell` |
| **ROD** | `OrderType.ROD` | `TimeInForce.ROD` |
| **IOC** | `OrderType.IOC` | `TimeInForce.IOC` |
| **FOK** | `OrderType.FOK` | `TimeInForce.FOK` |
| **Limit** | `StockPriceType.LMT` | `PriceType.Limit` |
| **Market** | `StockPriceType.MKT` | `PriceType.Market` |
| **Common/Lot** | `StockOrderLot.Common` | `MarketType.Common` |
| **Odd** | `StockOrderLot.IntradayOdd` | `MarketType.IntradayOdd` |

## Market Data (WebSocket)

### Shioaji (Callback Style)

```python
@api.on_quote
def quote_callback(topic, quote):
    print(quote)

api.quote.subscribe(contract)
```

### FubonNeo (Callback Style)

```python
def on_message(code, content):
    print(content)

sdk.init_realtime() # Connect WS
sdk.set_on_quote(on_message) # Set global handler

rest_client = sdk.marketdata.rest_client
rest_client.stock.intraday.ticker(symbol="2330") # triggers auto-subscription if configured
# OR explicitly subscribe if using raw notification channels
```

## Advanced Patterns

### Checking Order Status

**Shioaji (In-Place Mutation)**
Shioaji updates the local `trade` object directly.

```python
api.update_status(trade)
print(trade.status.status) # e.g. Filled
```

**FubonNeo (Poll & Search)**
FubonNeo returns a fresh list of orders. You must find your order by `order_no`.

```python
results = sdk.stock.get_order_results(acc)
my_order = next((o for o in results.data if o.order_no == "ORDER123"), None)
if my_order:
    print(my_order.status)
```

### Connection Health & Reconnection

**Shioaji**
Manual handling of `TokenError` and event codes (0=Up, 12=Reconnecting).

```python
@api.quote.on_event
def event_callback(code, event):
    if code == 12: print("Reconnecting...")
```

**FubonNeo**
The SDK manages token lifecycle internally for the most part. Monitor via `on_event`.

```python
def on_event(code, content):
    print(f"Event: {code}, Msg: {content}")

sdk.set_on_event(on_event)
```

## Migration Recipe: The "Worker" Wrapper

Shioaji users often create a `TradingWorker` class. Here is the equivalent pattern in FubonNeo, handling the valid "Polling" strategy for order status.

```python
import time
from fubon_neo.sdk import FubonSDK, Order
from fubon_neo.constant import BSAction, MarketType, PriceType, TimeInForce, OrderType

class FubonWorker:
    def __init__(self):
        self.sdk = FubonSDK()
        self.account = None

    def login(self, user_id, pwd, cert_path, cert_pwd):
        accounts = self.sdk.login(user_id, pwd, cert_path, cert_pwd)
        self.account = accounts.data[0]
        self.sdk.init_realtime() # Connect WS

    def place_order(self, symbol, price, qty):
        order = Order(
            BSAction.Buy, symbol, qty,
            MarketType.Common, PriceType.Limit, TimeInForce.ROD, OrderType.Stock,
            price=price
        )
        res = self.sdk.stock.place_order(self.account, order)
        return res.data.order_no if res.data else None

    def get_order(self, order_no):
        """Replacement for shioaji's trade update mechanism"""
        results = self.sdk.stock.get_order_results(self.account)
        if results.data:
            return next((o for o in results.data if o.order_no == order_no), None)
        return None

    def cancel(self, order_no):
        order = self.get_order(order_no)
        if order:
            self.sdk.stock.cancel_order(self.account, order)
```
