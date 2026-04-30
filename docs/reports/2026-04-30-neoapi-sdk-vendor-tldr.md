# 給 NeoAPI SDK 開發商的 TL;DR：從 rshioaji / shioaji 學什麼

Date: 2026-04-30

## 一句話結論

rshioaji 示範的是：證券 SDK 可以從「每個語言一包函式庫」進化成「本機 API Gateway + CLI + OpenAPI 的工具友善產品面」。NeoAPI 不一定要照抄，但應該優先補強 SDK 的 self-describing 能力與 Agent-friendly 操作面。

## 為什麼重要

現在 SDK 不能只做到「人看文件後能寫程式」。它還要做到：

- IDE 能自動補完。
- CI 能穩定安裝。
- 企業能審供應鏈。
- AI Agent 能讀 schema、不亂猜欄位。
- 非 Python 使用者能用 HTTP / CLI 快速試錯。

NeoAPI 目前各語言分開 SDK 的策略是可行的，但在跨語言整合與 AI Agent 使用場景下，會出現可發現性不足、工具不易理解、文件/版本容易漂移的問題。

## 最高 ROI 的三件事

### 1. 先讓 Python wheel 變得「看得懂」

優先補：

- `.pyi` stubs
- `py.typed`
- rich `METADATA`
- SBOM
- package-index-compatible 安裝路徑
- machine-readable download manifest

這些不用重寫交易 core，但會立刻改善 IDE、LLM、CI、企業導入體驗。

### 2. 把 CLI 當正式產品面

先做最小 CLI，不必一開始就做完整 server：

```bash
neoapi version --verbose
neoapi doctor
neoapi status
neoapi data snapshot --symbol 2330 --json
neoapi order validate --json
```

CLI 的價值不是炫技，而是讓人類、腳本、CI、AI Agent 都有一個穩定、可檢查、可自動化的操作入口。

### 3. 規劃最小本機 Gateway / OpenAPI

中期可以做：

```bash
neoapi server start
```

提供：

- `http://127.0.0.1:8080/health`
- `/openapi.json`
- `/docs`
- 核心 REST endpoints：行情、下單驗證、查單、帳戶

這會讓 NeoAPI 不只服務 Python / Node / Go SDK 使用者，也能服務 curl、Postman、Excel、內部系統、AI tool runner。

## 不要做的事

- 不要一開始就複製完整 dashboard / custom app hosting。
- 不要把 OpenAPI 手寫在文件裡，應該由程式碼或 schema source 產生。
- 不要讓 server 預設暴露到非 localhost。
- 不要讓下單 endpoint 沒有明確 production/test/dry-run 標示。
- 不要用新 CLI / server 破壞既有 SDK 介面；它應該是補充產品面，不是替代品。

## 最小可行下一步

三週 MVP：

1. **Week 1**：補 `.pyi`、`py.typed`、metadata、SBOM、download manifest。
2. **Week 2**：做 `neoapi doctor`、`neoapi version --verbose`、核心 CLI `--json` 輸出。
3. **Week 3**：產出核心 OpenAPI v1，先覆蓋行情查詢、帳戶、查單、下單驗證。

成功指標：

> 一位不寫 Python 的工程師，可以在 5 分鐘內用 curl / Postman 或 CLI 完成第一筆行情查詢，並能明確知道目前是 test 還是 production 環境。

## 最短版建議

NeoAPI 的下一步不是把 SDK 做得更厚，而是讓 SDK **更容易被機器理解**：先補 stubs、metadata、SBOM、manifest、diagnostic CLI，再用 OpenAPI / localhost Gateway 打開跨語言與 AI Agent 場景。
