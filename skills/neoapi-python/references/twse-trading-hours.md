# TWSE/TPEx cash equities — trading hours (Asia/Taipei)

> Purpose: quick reference for **Taiwan cash equities** session timing when designing market-data WebSocket subscriptions.
> 
> Note: exact WebSocket push windows depend on your provider (broker/marketdata service). Use this as the exchange schedule baseline; code should still handle "session closed" / stale snapshots gracefully.

## Core auction / matching sessions

- **Pre-open call auction (盤前集合競價)**: 08:30–09:00
- **Continuous trading (盤中)**: 09:00–13:25
- **Close call auction (收盤集合競價)**: 13:25–13:30

## Other common sessions (if needed)

- **After-hours fixed-price (盤後定價)**: 14:00–14:30
- **Odd-lot (零股)**: commonly 13:40–14:30

## Engineering notes

- Don’t hard-cut sockets exactly at 13:30; allow a buffer and rely on server status / heartbeat.
- For research pipelines, historical bars and instrument metadata are usually available outside trading hours.
