# 給 NeoAPI SDK 開發商的 TL;DR：從 rshioaji / shioaji 學什麼

Date: 2026-04-30

rshioaji 最值得參考的地方，不是它把 SDK 做得很肥，而是它把券商 API 從「某個語言的函式庫」往「本機交易入口」推了一步：同一個安裝包裡有 Python SDK、CLI、localhost REST/SSE server、`/openapi.json` 和 `/docs`。這讓非 Python 使用者可以打 HTTP，讓自動化腳本可以跑 CLI，也讓 AI Agent 有機器可讀的 API contract，不必靠讀文件和猜欄位工作。NeoAPI 目前各語言各自 SDK 的策略仍然可行，但在跨語言整合和 Agent 使用場景下，會比較缺一個統一、可檢查、可被工具理解的操作面。

NeoAPI 最高 ROI 的下一步，不是立刻複製完整 server 或 dashboard，而是先把 SDK 做得更 self-describing：補 `.pyi` stubs、`py.typed`、rich metadata、SBOM、machine-readable download manifest，並提供標準 package-index-compatible 的安裝路徑。接著補一個很小但穩定的 CLI surface，例如 `neoapi doctor`、`neoapi version --verbose`、`neoapi status`、`neoapi data snapshot --json`、`neoapi order validate --json`。這些不需要重寫交易 core，但會立刻改善 IDE、CI、企業審查、客服除錯和 AI Agent 操作體驗。

中期再考慮最小 localhost Gateway：先提供 `/health`、`/info`、`/openapi.json`、`/docs`，以及行情查詢、帳戶、查單、下單驗證等少數核心 REST endpoints。安全預設要保守：只綁 `127.0.0.1`，明確標示 test / production，交易 endpoint 先支援 validate / dry-run。簡單說，NeoAPI 不需要一口氣變成 rshioaji；先讓 SDK「看得懂、查得到、可診斷、可機器調用」，就已經是很高 ROI 的升級。
