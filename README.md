# Fubon NeoAPI Skill 精煉專案

此儲存庫用於測試與持續優化 `neoapi-python` skill bundle，供 AI 編碼代理（如 Codex、Claude Code、Gemini）正確使用富邦新一代（Fubon Neo）Python SDK，涵蓋交易與行情工作流程。

- English supplementary README: [README.en.md](README.en.md)

## Repo 結構

- `skills/neoapi-python/` - Skill 主體（`SKILL.md`、`references/`、`llms*.txt`、`VERSION`、`INSTALL.md`）
- `update-skill.ps1` - Windows 更新腳本（從 GitHub 下載後安裝到 `~/.codex/skills/public/`）
- `update-skill.sh` - macOS/Linux 更新腳本

## 相容性

本 skill 以純檔案形式（入口為 `SKILL.md`）發佈，方便跨平台與跨代理使用。若非 Codex 平台，請將安裝路徑改為目標代理的 skill/instruction 目錄（可透過更新腳本的 `INSTALL_DIR` 參數或環境變數調整）。

## GitHub Repo

- `https://github.com/phenomenoner/neoapi-skill`

## 安裝

完整安裝方式請見 `skills/neoapi-python/INSTALL.md`。本 repo 採用 `skills/`（非 `.skills/`）目錄。一般使用者建議安裝到：

- Windows: `%USERPROFILE%\.codex\skills\public\neoapi-python`
- macOS/Linux: `~/.codex/skills/public/neoapi-python`

## 版本管理

Skill 版本存放於 `skills/neoapi-python/VERSION`（semver）。目前版本：`1.0.0-beta.29`（Beta 1.0.0）。

## 多代理 Adapter

根目錄提供主要代理平台的 adapter（中文優先、英文補充）：

- `CLAUDE.md`
- `GEMINI.md`
- `AGENTS.md`

以上 adapter 皆以 `skills/neoapi-python/` 為單一真實來源（source of truth）。

## LLM 文件（線上）

以下官方頁面與 `llms*.txt` 為優先參考來源：

- `https://www.fbs.com.tw/TradeAPI/docs/welcome/build-with-llm`
- `https://www.fbs.com.tw/TradeAPI/en/docs/welcome/build-with-llm/`
- `https://www.fbs.com.tw/TradeAPI/llms.txt`
- `https://www.fbs.com.tw/TradeAPI/llms-full.txt`
- `https://www.fbs.com.tw/TradeAPI/en/llms.txt`
- `https://www.fbs.com.tw/TradeAPI/en/llms-full.txt`

內建於 skill bundle 的 `llms*.txt` 為離線快照；當官方端點更新時，應同步刷新 repo 內副本並 bump `VERSION`，否則更新腳本不會抓到這次變更。

## 從 GitHub 更新

更新腳本會下載 repo zip，複製 `skills/neoapi-python` 到本機安裝路徑，並比較 `VERSION`，若已是最新版則跳過。

範例：

```powershell
.\update-skill.ps1 -Repo phenomenoner/neoapi-skill
```

```bash
./update-skill.sh phenomenoner/neoapi-skill
```

## 本地回歸測試

- 本地整合測試 runner：`.test/test_runner.py`（不包含於對外發佈 skill 包）
- 測試輸出：`.test/logs/`（文字 log + JSON summary）
- Suites：
  - `smoke`：基本登入與交易/行情健檢
  - `complex`：多標的行情矩陣 + 雙訂單生命週期整合測試
  - `all`：完整覆蓋（包含 complex）

## 變更紀錄

完整版本歷程統一維護於 [CHANGELOG.md](CHANGELOG.md)。

目前最新版本為 `1.0.0-beta.29`，重點更新為補充 WebSocket 訊息 envelope 與 `on_message` 解析指引，明確說明實際交易資料位於 `message["data"]`。
