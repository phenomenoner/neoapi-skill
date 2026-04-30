# Shioaji vs NeoAPI：本機 Gateway 與 AI Agent 介面的產品策略對比

Date: 2026-04-30

## Executive summary

rshioaji / shioaji 不只是在重做 Python SDK。它其實把證券 API 包成兩個產品面：

1. **本機 API Gateway**：用 `shioaji server start` 在使用者自己的電腦上開一個 localhost REST/SSE server，解決跨語言整合問題。
2. **CLI / Agent tool surface**：用 `shioaji auth/data/order/portfolio/...` 與 `/openapi.json`，讓 shell scripts、CI、自動化工具、AI Agent 都能更可靠地理解與操作 API。

相對之下，Fubon NeoAPI 目前比較像「每個語言各自發一包 SDK」：Python、Node、Go、C#、C++ 各自下載、各自包裝、各自文件。這個策略乾淨、直覺，但在 AI Agent 與跨語言整合時代會遇到三個問題：

- 每種語言都要重複學一次 SDK。
- 沒有統一的本機 HTTP 介面給非 Python / 非特定 SDK 使用者。
- 沒有足夠 self-describing 的 metadata / stubs / OpenAPI / CLI schema，AI 和 IDE 都比較難可靠操作。

高 ROI 的方向不是立刻複製 rshioaji 全套，而是先補三層：

1. **讓 SDK 更容易被工具理解**：`.pyi` stubs、`py.typed`、SBOM、rich metadata、標準 package index。
2. **提供最小本機 Gateway / OpenAPI**：先讓核心行情、下單、查單、帳務能透過 REST JSON 被呼叫。
3. **把 CLI 當正式產品面**：提供 `doctor/status/version/order/data` 等可機器讀取的 CLI，而不是只靠程式碼範例。

## 一、兩個產品面：rshioaji 真正埋的是什麼

### 1. 本機 server：把 SDK 變成 localhost API gateway

白話說，rshioaji 安裝後不只是：

```python
import shioaji
```

它還附了一個 `shioaji` executable。使用者可以：

```bash
shioaji server start
```

然後在本機得到：

```text
http://127.0.0.1:8080/api/v1/...
```

這代表任何語言都可以改成打 HTTP：

- JavaScript / TypeScript
- Go
- C#
- Java
- curl / Postman
- Low-code / no-code 工具
- AI Agent tool runner

不用每個語言都直接 link native SDK。

目前文件列出的 server 能力包含：

- REST endpoints：auth、market data、order、portfolio、watchlist、apps
- SSE streaming：tick、bidask、quote、order events
- `/openapi.json`：機器可讀 OpenAPI spec
- `/docs`：互動式 API 文件
- dashboard / custom app hosting
- localhost 預設，simulation 預設，production 需要明確啟動

產品含義：**rshioaji 把 Python wheel 變成本機交易 gateway 的配送管道。**

### 2. CLI / Agent surface：把 API 變成工具可以操作的命令面

rshioaji 同時提供 CLI 指令：

```bash
shioaji auth accounts
shioaji data snapshots --codes 2330
shioaji order place --code 2330 --action Buy --price 580 --quantity 1
shioaji portfolio balance
shioaji tree --all
```

這件事對 AI Agent 很重要，因為 Agent 最怕的不是 API 很複雜，而是 API **不可發現、不可檢查、不可 dry-run、輸出不穩定**。

CLI 如果設計得好，可以提供：

- 穩定命令名稱
- `--json` 結構化輸出
- `tree --all` / schema 類能力，讓 Agent 讀懂可用操作
- `server check/status` 讓 Agent 先確認環境和 simulation/production
- `utils api check` / token status / doctor 類診斷能力

產品含義：**CLI 不是附屬工具，而是 API 給人類、自動化腳本、AI Agent 的共同操作面。**

## 二、NeoAPI 現況：各語言 SDK 策略的優點與限制

NeoAPI 現在的策略比較像：

```text
Python SDK + Node SDK + Go SDK + C# SDK + C++ SDK
```

這有明確優點：

- 各語言開發者可以用自己熟悉的語言原生 SDK。
- Python wheel 小很多，封裝相對簡單。
- 交易 core 與 market data 依賴可以分開維護。
- 對傳統 SDK 使用者直覺。

但限制也很明顯：

| 面向 | NeoAPI 現況 | 產品限制 |
|---|---|---|
| 跨語言整合 | 每種語言各自 SDK | 每多支援一種語言，就多一份維護與文件成本 |
| Agent / automation | 沒有統一 CLI / OpenAPI gateway | Agent 需要自行讀文件、寫 wrapper、猜物件 shape |
| Python discoverability | wheel 內沒有 `.pyi` | IDE / type checker / LLM 都不容易看出 native API surface |
| 安裝分發 | 官網 zip + wheel | CI、pinning、自動化安裝比較麻煩 |
| 供應鏈透明度 | 未見 SBOM | 企業導入與安全審查較弱 |
| 版本索引 | 網頁列表為主 | 機器難以自動追蹤各平台版本 |

## 三、AI Agent 需求分析

AI Agent 要可靠使用金融 API，最需要的不是「範例很多」，而是：

1. **機器可讀 API contract**
   - OpenAPI / JSON Schema / typed stubs。
   - 不然 Agent 很容易編出不存在的欄位或 endpoint。

2. **可檢查的操作面**
   - `status`、`check`、`doctor`、`--json`、`dry-run`。
   - 金融 API 尤其需要先確認 production / simulation。

3. **穩定輸入輸出**
   - REST JSON、CLI JSON，比 SDK object 更容易被工具鏈解析。

4. **短 feedback loop**
   - 最好的體驗是：start server → curl → 看 JSON → 修正。
   - 最差的體驗是：讀文件 → 猜 SDK object → 寫腳本 → crash → 再猜。

5. **事件流標準化**
   - SSE / WebSocket schema 要明確。
   - callback-only 對人寫程式可接受，對 Agent 生成工具比較難。

rshioaji 的 server + CLI + OpenAPI 剛好把這些面補起來。NeoAPI 若要在 Agent 時代更好用，重點就是補足這些 self-describing surfaces。

## 四、產品策略對比

| 策略問題 | rshioaji / shioaji | NeoAPI 現況 | NeoAPI 可吸收方向 |
|---|---|---|---|
| 非 Python 使用者怎麼接？ | 開 localhost REST/SSE server | 各語言各自 SDK | 先做核心 REST Gateway MVP |
| Agent 怎麼知道有哪些 API？ | `/openapi.json` + `/docs` + CLI tree | 主要靠文件與範例 | 提供 OpenAPI / schema / CLI `--json` |
| Shell/CI 怎麼操作？ | `shioaji order place ...` | 需要寫程式 | 提供 `neoapi doctor/status/data/order` CLI |
| Python IDE/LLM 怎麼理解 native API？ | `_core.pyi` | 無 `.pyi` | 先補 stubs 和 `py.typed` |
| 企業怎麼審供應鏈？ | wheel 內含 SBOM | 未見 SBOM | 加 CycloneDX SBOM |
| 發行怎麼自動化？ | PyPI | 官網 zip | PyPI 或至少 package-index-compatible mirror |

## 五、NeoAPI 高 ROI 路線圖

### P0：封裝與可發現性，最快見效

這些不需要改交易 core，ROI 最高：

1. **`.pyi` stubs for native extension**
   - 讓 IDE、type checker、LLM 都能看懂 `FubonSDK`、`Order`、callback、回傳物件。

2. **`py.typed`**
   - 宣告 Python package 支援型別資訊。

3. **rich `METADATA`**
   - 補 summary、license、homepage、docs URL、project URLs、platform info。

4. **SBOM**
   - 在 wheel `dist-info/sboms/` 放 CycloneDX。

5. **標準 package index 或 mirror**
   - 至少讓 CI 可以穩定 pin：`pip install fubon-neo==2.2.8` 類體驗。

6. **machine-readable download manifest**
   - JSON 列出各平台、語言、版本、checksum、下載 URL。

### P1：Agent-friendly CLI MVP

先不做完整 server，也可以先做 CLI：

```bash
neoapi version --verbose
neoapi doctor
neoapi status
neoapi data snapshot --symbol 2330 --json
neoapi order validate --json
```

高價值原因：

- 降低客服與安裝除錯成本。
- 讓 Agent 可以先確認環境、版本、憑證、連線模式。
- 給自動化腳本一個穩定入口。

### P2：OpenAPI / 本機 Gateway MVP

不要一開始做大 dashboard。先做最小可用：

- `/health`
- `/info`
- `/openapi.json`
- `/docs`
- `/api/v1/data/snapshot`
- `/api/v1/order/place`
- `/api/v1/order/results`
- `/api/v1/account/accounts`

先服務：

- 非 Python 使用者
- Agent / tool runner
- Postman / curl / internal automation

等有採用證據，再加 SSE、dashboard、custom app hosting。

## 六、風險與取捨

### 不要一開始就複製 rshioaji 全套

rshioaji 的方向值得學，但 NeoAPI 不需要馬上做：

- 完整 dashboard
- custom app hosting
- 全 endpoint REST server
- 跨語言 server 大重構

這些都會增加維護與安全面。

### 先補 self-describing，再補 gateway

對 NeoAPI 來說，最低風險順序是：

1. 補 stubs / metadata / SBOM / manifest。
2. 補 CLI doctor/status/version。
3. 補 OpenAPI schema。
4. 補最小本機 gateway。
5. 最後才考慮 SSE / dashboard / apps。

### 安全預設要保守

如果做本機 server：

- 預設只綁 `127.0.0.1`。
- production / test mode 必須明確可見。
- 下單 endpoint 要能 dry-run / validate。
- OpenAPI docs 裡要明確標示會造成真實交易的 endpoint。

## 七、建議優先順序

### 立即做

1. `.pyi` stubs + `py.typed`
2. rich wheel metadata
3. SBOM
4. machine-readable download manifest
5. `neoapi version --verbose` / `neoapi doctor`

### 短期做

1. CLI `--json` output contract
2. core OpenAPI spec
3. official examples generated from the same schema
4. package-index-compatible distribution path

### 中期做

1. localhost REST gateway MVP
2. SSE / event stream schema
3. `/docs` interactive UI
4. Agent tool schema generation

## 八、一句話結論

rshioaji 的關鍵啟示不是「SDK 要變很肥」，而是：**金融 API 在 AI Agent 時代需要從語言函式庫升級成可被工具理解、可被命令列操作、可被 HTTP 調用的產品面。**

NeoAPI 最值得先吸收的是 self-describing package、diagnostic CLI、OpenAPI contract、最小本機 Gateway，而不是一口氣複製完整 dashboard/server。
