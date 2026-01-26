# Implementation Practices (NeoAPI Python)

Production-tested patterns for building low-latency trading systems with the Fubon Neo Python SDK.

---

## 1. SDK Manager Pattern

### Why Use a Manager Class?

Wrapping the SDK in a manager class provides:

- Centralized connection lifecycle management
- Automatic reconnection handling
- Clean separation between infrastructure and trading logic

### Key Components

```python
class SDKManager:
    def __init__(self):
        self.sdk = None
        self.accounts = None
        self.active_account = None

        # Store credentials for auto-reconnect
        self._credentials = {}

        # Thread pool for blocking SDK calls
        self._executor = ThreadPoolExecutor()
```

### Login Flow

1. Create SDK instance
2. Set callbacks **before** login (important for catching early events)
3. Call login and store credentials for reconnection
4. Establish market data connections

```python
def login(self, user_id, password, cert_path, cert_pass):
    self.sdk = FubonSDK()

    # Set callbacks BEFORE login
    self.sdk.set_on_event(self._on_event)
    self.sdk.set_on_filled(self._on_filled)

    response = self.sdk.login(user_id, password, cert_path, cert_pass)

    if response.is_success:
        # Store for reconnection
        self._credentials = {...}
        self.accounts = response.data
        return True
    return False
```

### Graceful Termination

Remove event listeners before disconnecting to prevent reconnection loops:

```python
def terminate(self):
    # 1. Disable callbacks to prevent reconnect attempts
    self.sdk.set_on_event(lambda c, m: None)

    # 2. Disconnect WebSockets
    for ws in self._ws_connections:
        ws.disconnect()

    # 3. Logout
    self.sdk.logout()
    self.sdk = None
```

---

## 2. WebSocket Management

### The 200-Symbol Limit

Each WebSocket connection supports up to **200 subscriptions**. For larger symbol lists, use multiple connections with load balancing.

### Multi-Connection Architecture

```text
┌─────────────┐
│ SDKManager  │
├─────────────┤
│ ws_conn[0]  │──▶ symbols 1-200
│ ws_conn[1]  │──▶ symbols 201-400
│ ws_conn[2]  │──▶ symbols 401-600
│ ...         │
└─────────────┘
```

### Load-Balanced Subscription

Track subscription counts per connection and assign new symbols to the least-loaded connection:

```python
def subscribe(self, symbol):
    # Find connection with fewest subscriptions
    min_idx = self._subscription_counts.index(min(self._subscription_counts))

    if self._subscription_counts[min_idx] >= 200:
        raise RuntimeError("All connections full")

    self._ws_connections[min_idx].subscribe({
        'channel': 'trades',
        'symbol': symbol
    })
    self._subscription_counts[min_idx] += 1
```

### Auto-Reconnect Pattern

On disconnect, reconnect and resubscribe all symbols:

```python
def _on_disconnect(self, code, message):
    # Reconnect
    self._establish_connections()

    # Resubscribe (copy list to avoid mutation during iteration)
    symbols_to_restore = self._subscribed_symbols.copy()
    self._subscribed_symbols.clear()

    for symbol in symbols_to_restore:
        self.subscribe(symbol)
```

---

## 3. Error Handling

### FugleAPIError Compatibility

SDK versions handle rate limits differently:

- **Old SDK (< 2.2.6)**: Returns error info in response object
- **New SDK (>= 2.2.6)**: Raises `FugleAPIError` exception

### Version-Agnostic Pattern

```python
# Version detection at module load
try:
    from fubon_neo.sdk import FugleAPIError
    HAS_FUGLE_ERROR = True
except ImportError:
    HAS_FUGLE_ERROR = False
    class FugleAPIError(Exception):
        status_code = 0  # Placeholder

# Usage
def fetch_with_retry(symbol):
    while True:
        try:
            response = rest_client.intraday.ticker(symbol=symbol)

            # Old SDK check
            if "429" in str(response.get("status", "")):
                time.sleep(60)
                continue

            return response

        except FugleAPIError as e:
            # New SDK check
            if e.status_code == 429:
                time.sleep(60)
                continue
            raise
```

---

## 4. Async Patterns for Low Latency

### Problem: Blocking SDK Calls

The SDK's order placement and query methods are blocking. In an async trading loop, these calls would block the entire event loop.

### Solution: ThreadPoolExecutor

Run blocking SDK calls in a thread pool:

```python
async def place_order_async(self, order):
    loop = asyncio.get_event_loop()

    # Wrap blocking call
    response = await loop.run_in_executor(
        self._executor,
        lambda: self.sdk.stock.place_order(self.account, order)
    )
    return response
```

### Bridging Sync Callbacks to Async

SDK callbacks run in SDK's thread. Bridge to async context:

```python
def _on_filled_sync(self, code, data):
    """Called by SDK in its thread."""
    asyncio.run_coroutine_threadsafe(
        self._on_filled_async(code, data),
        self._event_loop
    )

async def _on_filled_async(self, code, data):
    """Process fill in async context."""
    async with self._locks[data.symbol]:
        # Safe to access shared state
        self._update_position(data)
```

### Per-Symbol Locking

Prevent race conditions when multiple ticks arrive for the same symbol:

```python
# Create lock per symbol
self._locks = {symbol: asyncio.Lock() for symbol in symbols}

# Use in tick processing
async def process_tick(self, symbol, data):
    async with self._locks[symbol]:
        # Only one tick per symbol processed at a time
        self._calculate_indicators(symbol, data)
        self._check_entry_conditions(symbol)
```

---

## 5. Order Management

### Order Creation

```python
from fubon_neo.sdk import Order
from fubon_neo.constant import (
    BSAction, PriceType, OrderType,
    TimeInForce, MarketType
)

order = Order(
    symbol="2330",
    price=580.0,
    quantity=1000,
    action=BSAction.Buy,
    price_type=PriceType.Limit,
    order_type=OrderType.Stock,
    time_in_force=TimeInForce.ROD,
    market_type=MarketType.Common,
    user_def="my_tag"  # Custom identifier
)
```

### Tracking Orders

Use `user_def` field to tag orders for tracking:

```python
# When placing
order.user_def = f"{strategy_name}_{symbol}_{timestamp}"

# When fill arrives
def on_filled(self, code, data):
    if data.user_def.startswith("my_strategy"):
        self._handle_my_fill(data)
```

---

## 6. REST API Best Practices

### Rate Limit Awareness

Market data REST APIs have rate limits. Implement backoff:

```python
async def fetch_all_tickers(self, symbols):
    results = {}
    for symbol in symbols:
        results[symbol] = await self._fetch_with_retry(symbol)
        await asyncio.sleep(0.1)  # Throttle requests
    return results
```

### Useful Endpoints

| Endpoint | Use Case |
|----------|----------|
| `intraday.ticker()` | Reference price, limit prices, stock flags |
| `intraday.quote()` | Current bid/ask, open price |
| `intraday.trades()` | Recent trade history |

---

## 7. Architecture Summary

```text
┌────────────────────────────────────────────────────────┐
│                    Trading System                       │
├─────────────────┬──────────────────┬───────────────────┤
│   SDKManager    │  TradingEngine   │   Strategy Logic  │
├─────────────────┼──────────────────┼───────────────────┤
│ • Login/Logout  │ • Tick Processing│ • Entry/Exit     │
│ • WS Management │ • Order Routing  │   Decisions       │
│ • Reconnection  │ • Position Track │ • Pure Functions  │
│ • Thread Pool   │ • Risk Controls  │ • No Side Effects │
└─────────────────┴──────────────────┴───────────────────┘
         │                  │                  │
         ▼                  ▼                  ▼
    Infrastructure      Execution           Logic
    (Stateful)         (Stateful)        (Stateless)
```

---

## 8. Best Practices Checklist

| Area | Practice |
|------|----------|
| **Initialization** | Set callbacks before login |
| **Credentials** | Store for auto-reconnect |
| **WebSocket** | Use multiple connections for >200 symbols |
| **Reconnection** | Remove listeners before disconnect |
| **Async** | Use ThreadPoolExecutor for blocking calls |
| **Locking** | Per-symbol locks for tick processing |
| **Rate Limits** | Implement retry with backoff |
| **Order Tracking** | Use `user_def` field for identification |
| **Logging** | Guard expensive log formatting |
| **Serialization** | Consider `orjson` for performance |
