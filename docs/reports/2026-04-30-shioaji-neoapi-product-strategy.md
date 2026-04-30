# Shioaji vs NeoAPI：從「SDK」到「本機交易入口」的產品策略差異

Date: 2026-04-30

## 先講結論

rshioaji / shioaji 比較有意思的地方，不是它用 Rust 重寫了 Shioaji，而是它把券商 API 包成了兩種更容易被使用的產品面：

1. **本機 Gateway**：使用者在自己電腦上跑 `shioaji server start`，就得到一個 localhost REST/SSE server。其他語言不用直接接 Python/Rust binding，打 HTTP 就能用。
2. **CLI / Agent 操作面**：`shioaji auth/data/order/portfolio/...` 這些命令，讓人、shell script、CI、AI Agent 都能用同一組穩定指令操作 API。

NeoAPI 目前比較像傳統 SDK 策略：Python、Node、Go、C#、C++ 各自提供一包。這條路乾淨，也符合既有開發者習慣；但缺點是每個語言都要各自學一次、各自維護文件，AI Agent 也很難直接「看懂」整個 API。

所以 NeoAPI 最值得吸收的，不是立刻複製 rshioaji 的完整 server / dashboard，而是先補三件事：

- 讓 SDK 變得更自我描述：`.pyi`、`py.typed`、metadata、SBOM、下載 manifest。
- 做一個可機器讀取的操作面：CLI `--json`、`doctor/status/version`、OpenAPI schema。
- 中期再考慮最小本機 Gateway，先支援行情、帳戶、查單、下單驗證這幾個高頻場景。

簡單說：**rshioaji 在賣的不只是 SDK，而是一個本機交易入口。NeoAPI 現在還比較像一組語言 SDK。**

## 一、rshioaji 做了哪兩個產品面

### 1. 本機 server：把交易 API 包成 localhost gateway

一般 Python SDK 是這樣用：

```python
import shioaji
api = shioaji.Shioaji()
api.login(...)
```

rshioaji 多做了一步：wheel 裡還放了一個 `shioaji` executable。使用者可以直接跑：

```bash
shioaji server start
```

跑起來後，本機會有一個 HTTP API：

```text
http://127.0.0.1:8080/api/v1/...
```

這件事的產品意義很大。它等於把「只有 Python/Rust binding 能用」改成「任何會打 HTTP 的東西都能用」。

可以接的就不只 Python，而是：

- JavaScript / TypeScript
- Go
- C#
- Java
- curl / Postman
- Low-code 工具
- 內部後台
- AI Agent tool runner

文件裡列出的 server 能力也不只是 health check，而是已經做到相當完整：

- REST：auth、market data、order、portfolio、watchlist、apps
- SSE：tick、bidask、quote、order events
- `/openapi.json`：機器可讀 API 規格
- `/docs`：互動式 API 文件
- dashboard / custom app hosting
- 預設 localhost、預設 simulation；production 需要明確開啟

這個設計的本質是：**用 Python wheel 配送一個本機 trading gateway**。

它的好處是跨語言整合變簡單；代價是 wheel 變大，部署和安全審查範圍也變大。

### 2. CLI：把交易 API 變成工具可以操作的命令

rshioaji 也把常用操作做成 CLI：

```bash
shioaji auth accounts
shioaji data snapshots --codes 2330
shioaji order place --code 2330 --action Buy --price 580 --quantity 1
shioaji portfolio balance
shioaji tree --all
```

這對 AI Agent 特別重要。

Agent 最怕的不是 API 複雜，而是沒有穩定入口：文件散、欄位不明、輸出 shape 不固定、環境狀態查不到、production/test 不清楚。金融 API 又更敏感，因為錯一次可能是真錢。

好的 CLI 可以先解掉很多問題：

- 用 `server check/status` 確認現在是 simulation 還是 production。
- 用 `--json` 讓腳本和 Agent 穩定解析結果。
- 用 `tree --all` 或 schema 類輸出，讓工具知道有哪些命令可以用。
- 用 `utils api check`、token status、doctor 類命令降低除錯成本。

所以 CLI 不是附屬品。它是 API 給人、腳本、CI、Agent 共用的操作面。

## 二、NeoAPI 現在的路線：各語言 SDK

NeoAPI 目前比較像這樣：

```text
Python SDK + Node SDK + Go SDK + C# SDK + C++ SDK
```

這條路有好處：

- 各語言開發者可以用原生 SDK。
- Python wheel 比 rshioaji 小很多。
- 交易 core 和 market data client 可以分開維護。
- 對傳統程式開發者來說很直覺。

但如果從「跨語言」和「AI Agent」看，就會出現幾個洞：

| 面向 | NeoAPI 現況 | 實際影響 |
|---|---|---|
| 跨語言整合 | 各語言各自 SDK | 每個語言都要各自學、各自維護、各自踩坑 |
| Agent / automation | 沒有統一 CLI / Gateway | Agent 要讀文件、猜 API、自己包 wrapper |
| Python 可發現性 | wheel 內沒有 `.pyi` | IDE、type checker、LLM 都看不清 native API surface |
| 安裝分發 | 官網 zip + wheel | CI pinning、自動化安裝比較不順 |
| 供應鏈透明度 | 未見 SBOM | 企業導入和資安審查比較吃力 |
| 版本索引 | 網頁列表為主 | 機器不容易追蹤各平台最新版本 |

這不是說 NeoAPI 現在做錯，而是它還停在「SDK 交付」視角。rshioaji 已經往「本機 API 產品」移動了。

## 三、AI Agent 真正在意什麼

Agent 要用金融 API，最需要的不是更多範例，而是更清楚的 contract。

幾個關鍵需求：

1. **機器可讀的 API 規格**
   - OpenAPI、JSON Schema、`.pyi` stubs 都算。
   - 沒有這些，Agent 很容易編出不存在的 endpoint 或欄位。

2. **可檢查的環境狀態**
   - `status`、`check`、`doctor`、`version --verbose`。
   - 尤其要清楚標出 test / production。

3. **穩定輸出**
   - REST JSON、CLI `--json` 比 SDK object 更容易被工具鏈解析。

4. **短 feedback loop**
   - 好體驗：start server → curl → 看 JSON → 修正。
   - 壞體驗：讀文件 → 猜 SDK object → 寫腳本 → crash → 再猜。

5. **事件流要有 schema**
   - SSE / WebSocket message shape 要清楚。
   - callback-only 對人寫程式還可以，對 Agent 生成工具比較麻煩。

rshioaji 的 server + CLI + OpenAPI，剛好把這幾個洞補起來。NeoAPI 如果要對 Agent 更友善，應該先補 self-describing surface。

## 四、策略對比

| 問題 | rshioaji / shioaji | NeoAPI 現況 | NeoAPI 可以怎麼吸收 |
|---|---|---|---|
| 非 Python 使用者怎麼接？ | localhost REST/SSE server | 各語言各自 SDK | 做最小 REST Gateway MVP |
| Agent 怎麼知道 API 長什麼樣？ | `/openapi.json`、`/docs`、CLI tree | 主要靠文件和範例 | 補 OpenAPI / schema / CLI `--json` |
| Shell / CI 怎麼操作？ | `shioaji ...` 命令 | 通常要寫程式 | 補 `neoapi doctor/status/data/order` CLI |
| IDE / LLM 怎麼看 native API？ | `_core.pyi` | 無 `.pyi` | 先補 stubs 和 `py.typed` |
| 企業怎麼審供應鏈？ | wheel 內含 SBOM | 未見 SBOM | 加 CycloneDX SBOM |
| 發行怎麼自動化？ | PyPI | 官網 zip | PyPI 或 package-index-compatible mirror |

## 五、NeoAPI 高 ROI 路線圖

### P0：先讓 package 變得「看得懂」

這層最值得先做，因為不用改交易 core：

1. **`.pyi` stubs**
   - 讓 IDE、type checker、LLM 看懂 `FubonSDK`、`Order`、callback、回傳物件。

2. **`py.typed`**
   - 宣告 package 支援型別資訊。

3. **rich metadata**
   - 補 summary、license、homepage、docs URL、project URLs、platform info。

4. **SBOM**
   - 在 wheel `dist-info/sboms/` 放 CycloneDX。

5. **標準 package index 或 mirror**
   - 至少做到 CI 能穩定 pin 版本。

6. **machine-readable download manifest**
   - 用 JSON 列出平台、語言、版本、checksum、下載 URL。

### P1：先做診斷型 CLI，不急著做完整 server

最小 CLI 可以先長這樣：

```bash
neoapi version --verbose
neoapi doctor
neoapi status
neoapi data snapshot --symbol 2330 --json
neoapi order validate --json
```

這種 CLI 馬上有價值：

- 客服和使用者都比較容易除錯。
- Agent 可以先確認版本、憑證、連線模式。
- 自動化腳本有穩定入口。

### P2：再做最小 OpenAPI / Gateway

不要一開始做 dashboard。先做最小可用：

- `/health`
- `/info`
- `/openapi.json`
- `/docs`
- `/api/v1/data/snapshot`
- `/api/v1/order/validate`
- `/api/v1/order/results`
- `/api/v1/account/accounts`

先服務幾種人：

- 非 Python 使用者
- Agent / tool runner
- Postman / curl / 內部 automation

等真的有人用，再加 SSE、dashboard、custom app hosting。

## 六、風險和取捨

### 不要一開始就照抄 rshioaji 全套

rshioaji 的方向值得學，但 NeoAPI 不需要馬上做完整版本：

- dashboard
- custom app hosting
- 全 endpoint REST server
- 跨語言 server 大重構

這些會放大維護成本，也會增加安全面。

### 比較安全的順序

1. 補 stubs / metadata / SBOM / manifest。
2. 補 CLI doctor / status / version。
3. 補 OpenAPI schema。
4. 補最小本機 Gateway。
5. 最後才考慮 SSE / dashboard / apps。

### 安全預設要保守

如果做本機 server：

- 預設只綁 `127.0.0.1`。
- test / production 要非常明顯。
- 下單相關 endpoint 先提供 validate / dry-run。
- OpenAPI docs 裡要標示哪些 endpoint 會造成真實交易。

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
3. 從 schema 產生 official examples
4. package-index-compatible distribution path

### 中期做

1. localhost REST gateway MVP
2. SSE / event stream schema
3. `/docs` interactive UI
4. Agent tool schema generation

## 最後一句

rshioaji 的啟示不是「SDK 要塞越多東西越好」。真正值得學的是：**金融 API 在 AI Agent 時代，不能只是一包語言函式庫；它要能被工具理解、被命令列操作、被 HTTP 呼叫，而且要有安全可檢查的邊界。**

NeoAPI 最好的下一步，是先把 package 做得更 self-describing，再補診斷 CLI 和 OpenAPI。Gateway 可以做，但要從小做，不要一開始就把整台 dashboard/server 搬進來。
