# Doc Index (NeoAPI Python)

This reference lists the most relevant docs for trading and market data and the
LLM-friendly outputs generated from the site build.

## Public URLs (preferred)

- Base site: https://www.fbs.com.tw/TradeAPI/
- English locale: https://www.fbs.com.tw/TradeAPI/en/
- Build with LLM (zh):
  - https://www.fbs.com.tw/TradeAPI/docs/welcome/build-with-llm
- Build with LLM (en):
  - https://www.fbs.com.tw/TradeAPI/en/docs/welcome/build-with-llm/
- LLM index:
  - https://www.fbs.com.tw/TradeAPI/llms.txt
  - https://www.fbs.com.tw/TradeAPI/en/llms.txt
- LLM full:
  - https://www.fbs.com.tw/TradeAPI/llms-full.txt
  - https://www.fbs.com.tw/TradeAPI/en/llms-full.txt
- Test environment bundle (zip):
  - https://www.fbs.com.tw/TradeAPI_SDK/sample_code/test_environment.zip
- Python SDK download page:
  - https://www.fbs.com.tw/TradeAPI/docs/sdk/python/download?type=download

Markdown access via `.md` URL is no longer supported. Use `llms.txt` and `llms-full.txt` instead.

## Bundled (offline)

These files live next to `SKILL.md` in the shared bundle:

- `llms.txt`
- `llms-full.txt`
- `llms.en.txt`
- `llms-full.en.txt`

## Local Repo Paths (maintainers)

- `tmp/llms/llms.txt` (index)
- `tmp/llms/llms-full.txt` (full content)

Use `llms.txt` to find the target page fast, then open the linked markdown or
search in `llms-full.txt` for the exact parameters and return types.

## Trading (Python)

- Setup & onboarding:
  - `docs/trading/prepare`
  - `docs/trading/quickstart`
  - `docs/trading/trade-rate-limit`
- Python SDK reference:
  - `docs/trading/library/python/login/`
  - `docs/trading/library/python/trade/`
  - `docs/trading/library/python/accountManagement/`
  - `docs/trading/library/python/logout`

## Market Data

- Overview:
  - `docs/market-data/intro`
- HTTP API:
  - `docs/market-data/http-api/getting-started`
  - `docs/market-data/http-api/rate-limit`
  - `docs/market-data/http-api/intraday/`
  - `docs/market-data/http-api/snapshot/`
  - `docs/market-data/http-api/historical/`
  - `docs/market-data/http-api/technical/`
- WebSocket API:
  - `docs/market-data/websocket-api/getting-started`
  - `docs/market-data/websocket-api/market-data-channels/`

## Implementation Practices

Production-tested patterns from the StrategyExecuter project:

- `references/implementation-practices.md`

Topics covered:

- SDK Manager pattern (connection lifecycle, auto-reconnect)
- WebSocket multi-connection load balancing
- Async patterns for low-latency trading
- FugleAPIError compatibility (old/new SDK)
- Order placement and fill handling

## Examples

- `references/examples-guidance.md` (code reading + modification checklist)

## Test Environment (Sandbox)

- `references/test-environment.md` (summary from official PDF in the test bundle)
- `references/skill-tests.md` (validation checklist for skill consumers)

## Search Hints

- Find a method quickly:
  - `rg -n "<MethodName>" llms-full.txt`
  - `rg -n "<MethodName>" tmp/llms/llms-full.txt`
  - `rg -n "<MethodName>" docs/trading/library/python`
- Find market data endpoints:
  - `rg -n "http-api" docs/market-data`
  - `rg -n "websocket" docs/market-data`
