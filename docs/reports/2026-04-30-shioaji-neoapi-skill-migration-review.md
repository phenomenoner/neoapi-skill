# Shioaji skill vs NeoAPI skill migration review

Date: 2026-04-30

## Scope

Compare SinoTrade `rshioaji` skill/plugin with `neoapi-skill` and identify improvements that would make agent-assisted Shioaji → Fubon Neo API migration safer and easier.

Inputs inspected:

- `Sinotrade/rshioaji` repo at `e02770d48ffe`
- `phenomenoner/neoapi-skill` repo local working tree
- Claude second-brain review artifact: `/root/.openclaw/workspace/.state/neoapi-rshioaji-analysis/artifacts/claude_skill_review.md`

## Verdict

`rshioaji` has the stronger **agent routing shape**: its top-level skill file routes by user task, then points to focused reference files (`ORDERS`, `STREAMING`, `MARKET_DATA`, `ACCOUNTING`, `CLI`, `HTTP_API`, language guides). This lowers context load and makes agents less likely to invent API names.

`neoapi-skill` already has stronger **migration intent**: it contains Neo-specific warnings, response-shape notes, test-environment observations, and a Shioaji migration surface. The improvement is not to copy rshioaji content; it is to make Neo migration references as task-addressable as rshioaji's references.

## What rshioaji skill does well

- Clear `I want to...` routing table in `skills/shioaji/SKILL.md`.
- One domain per reference file: orders, streaming, contracts, accounting, market data, troubleshooting.
- Multiple access layers are clearly separated: Python, CLI, HTTP API/SSE, multi-language clients.
- Simulation vs production safety is prominent.
- Rate limits are summarized in the skill front door.
- CLI and HTTP API are first-class, so non-Python users have a direct path.

## What neoapi-skill already does well

- Explicit NeoAPI version/compatibility posture.
- Records important SDK behavioral findings such as response-shape differences and callback behavior.
- Has migration-oriented material instead of only product documentation.
- Keeps official Fubon docs / `llms-full.txt` as source-of-truth boundary, which reduces fake endpoint risk.

## Gaps for Shioaji → Neo migration

| Gap | Why it matters | Recommended fix |
|---|---|---|
| Missing task-routing table for migration work | Agents need to know which small reference file to load for `place_order`, `subscribe`, `activate_ca`, etc. | Add a routing table near the top of `skills/neoapi-python/SKILL.md`. |
| Migration material is not split by concern | A user porting order lifecycle code should not load all docs. | Add focused references: cookbook, constants mapping, order lifecycle, callbacks, market data, sim/prod. |
| Sim/prod semantics differ dangerously | Shioaji commonly uses `simulation=True`; Neo production/test depends on endpoint/config. | Put a loud warning at the top of migration docs. |
| Quantity unit shift is easy to miss | Shioaji common stock `quantity=1` means 1 lot; Neo stock quantity is shares. | Promote to top-level migration callout and every order example. |
| Auth/CA model differs | Shioaji `login` + `activate_ca`; Neo wraps cert into login flow. | Add auth migration section with before/after snippets. |
| Account auto-selection differs | Shioaji exposes `api.stock_account`; Neo requires selecting account object from login result. | Add account selection section with filtering examples. |
| Modify/cancel lifecycle differs | Neo often requires fetching current order object before modify/cancel. | Add `order-lifecycle.md` with `place -> query -> modify -> cancel -> verify` pattern. |
| Callback model differs | Shioaji decorator callbacks map poorly to Neo callback methods/WebSocket envelope. | Add callback mapping file. |
| Constants/enums differ | `Action.Buy`, `StockPriceType.LMT`, `OrderType.ROD` need deterministic mapping. | Add constants mapping table with verified source anchors. |
| Futures/options/combo scope is unclear | rshioaji has futures/options/combo surfaces; Neo skill may be cash-equity-first. | Add explicit in-scope/out-of-scope rows instead of silence. |

## Recommended file additions

Add these under `skills/neoapi-python/references/`:

1. `migration-shioaji-cookbook.md`
   - Per-call translations.
   - Triggers: `migrate from shioaji`, `port shioaji code`, `api.Contracts`, `api.place_order`, `activate_ca`, `update_order`, `cancel_order`.

2. `constants-mapping.md`
   - Shioaji enum/constant → Neo enum/constant cross-reference.
   - Triggers: `Action.Buy`, `StockPriceType`, `OrderType.ROD`, `StockOrderLot`, `StockOrderCond`.

3. `order-lifecycle.md`
   - Place / query / modify / cancel / status verification.
   - Must include the re-fetch-current-order-object rule.

4. `callback-mapping.md`
   - Shioaji decorators/callbacks → Neo callbacks/WebSocket envelope.
   - Include `on_tick_stk_v1`, `on_bidask`, `on_quote`, `on_event`, `set_on_order`, `set_on_filled`, `set_on_message`.

5. `quote-source-mapping.md`
   - Snapshot/ticks/kbars/subscribe equivalents.
   - Include REST vs WebSocket split and speed/normal mode caveats.

6. `sim-vs-prod.md`
   - Shioaji simulation flag vs Neo test/prod endpoint behavior.
   - Include what returns fake/empty/different data in test environment.

7. `account-and-positions.md`
   - Account selection, inventories, bank balance, realized/unrealized P&L.

## Suggested SKILL.md routing table

```md
| Task | Load file |
|---|---|
| Port Shioaji code to NeoAPI | references/migration-shioaji-cookbook.md |
| Map Shioaji constants/enums | references/constants-mapping.md |
| Place/modify/cancel/query stock orders | references/order-lifecycle.md |
| Translate quote callbacks/subscriptions | references/callback-mapping.md + references/quote-source-mapping.md |
| Understand test vs production behavior | references/sim-vs-prod.md |
| Translate account/position/P&L calls | references/account-and-positions.md |
```

## Migration mapping checklist

### Auth / CA

- Shioaji pattern: `api = sj.Shioaji(simulation=True)` → `api.login(api_key, secret_key)` → `api.activate_ca(...)`.
- Neo pattern: construct `FubonSDK(...)`, then login with account credentials and cert path/password according to official docs.
- Documentation rule: do not invent exact method signatures; every row must cite `llms-full.txt` or official Fubon docs.

### Contracts / instruments

- Shioaji code often relies on `api.Contracts.Stocks["2330"]` rich contract objects.
- Neo stock order examples generally pass symbol/code directly and query metadata separately.
- Add mapping for `limit_up`, `limit_down`, reference price, and day-trade flags.

### Orders

- Shioaji common stock quantity is lots; Neo stock order quantity is shares. This is a must-fix warning.
- Shioaji uses local `Trade` objects heavily; Neo workflows should query current order results before modify/cancel.
- Add status-code mapping table and include verified semantics.

### Market data / streaming

- Shioaji returns typed Python objects from native callbacks.
- Neo market data uses REST/WebSocket client surfaces and message envelopes; examples should show extracting `message["data"]` only after checking event type.
- Document speed mode restrictions if using Neo WebSocket `Mode.Speed`.

### Errors / response shapes

- NeoAPI has version-sensitive error/response behavior. Keep `[verified]` and `[TODO verify]` markers per row.
- Do not promise exceptions or fields that are not verified against current docs / SDK.

## Priority

### Must-fix

1. Add sim/prod migration warning.
2. Promote lot-to-share quantity warning.
3. Document re-fetch-before-modify/cancel lifecycle.
4. Add account selection rules.
5. Add auth/CA migration section.

### Should-fix

1. Add top-level routing table.
2. Split migration docs into focused references.
3. Add constants and callback mapping files.
4. Add explicit out-of-scope rows for futures/options/combo features if not supported by current Neo skill.
5. Add source-anchor verification tags to every mapping table.

## Guardrails

- Treat Fubon official docs and bundled `llms-full.txt` as source of truth.
- Mark unverified API names as `TODO verify`, not as examples to copy.
- Keep migration examples stock/cash-equity scoped unless futures/options support is explicitly verified.
- Prefer small references and routing tables over one giant migration document.
