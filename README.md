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

Skill 版本存放於 `skills/neoapi-python/VERSION`（semver）。目前版本：`1.0.0-beta.23`（Beta 1.0.0）。

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

- 2026-01-26: 1.0.0-beta.1 - 初始 beta，加入更新腳本、VERSION 與專案基礎檔。
- 2026-01-26: 1.0.0-beta.1 - 補充安裝路徑與跨平台相容性說明。
- 2026-01-26: 1.0.0-beta.1 - 初始化 GitHub repo，更新預設更新來源。
- 2026-01-26: 1.0.0-beta.2 - 新增測試環境說明文件與 sandbox 備註。
- 2026-01-26: 1.0.0-beta.2 - 新增本地 smoke 測試腳本（`.test`，不納入發布）。
- 2026-01-26: 1.0.0-beta.3 - 補充 SDK wheel 下載/安裝與測試包資訊。
- 2026-01-26: 1.0.0-beta.4 - 紀錄本地測試驗證結果。
- 2026-01-26: 1.0.0-beta.5 - 新增 SDK 安裝片段與 Python 版本建議。
- 2026-01-26: 1.0.0-beta.6 - 在 `SKILL.md` 增加 SDK install 快速提示。
- 2026-01-26: 1.0.0-beta.7 - 新增 skill 驗證測試案例與投稿格式。
- 2026-01-26: 1.0.0-beta.8 - 紀錄 skill 測試結果。
- 2026-01-26: 1.0.0-beta.9 - 補充下單 + callback 測試結果。
- 2026-01-26: 1.0.0-beta.10 - 新增 examples-guidance 並更新索引/TODO。
- 2026-01-26: 1.0.0-beta.11 - 標註 `.md` URL 技巧失效，改以 `llms.txt/llms-full.txt` 為主。
- 2026-01-27: 1.0.0-beta.12 - 釐清行情初始化與測試/正式環境價位差異。
- 2026-01-27: 1.0.0-beta.13 - 釐清 `intraday.ticker` 用法與訂單狀態判讀。
- 2026-01-27: 1.0.0-beta.14 - 更新無副檔名路徑寫法，補充整合測試紀錄。
- 2026-02-03: 1.0.0-beta.15 - `SKILL.md` 新增快速用法（Quickstart/Enums）與 Shioaji 遷移指南。
- 2026-02-03: 1.0.0-beta.16 - 新增遷移實作紀錄與代理操作指南。
- 2026-02-03: 1.0.0-beta.17 - 新增本地化與中英術語對照。
- 2026-02-09: 1.0.0-beta.18 - 補充 Build-with-LLM 連結並提高線上 `llms*.txt` 優先序。
- 2026-02-09: 1.0.0-beta.19 - 更新內建 `llms*.txt` 並統一路徑為無副檔名。
- 2026-02-09: 1.0.0-beta.20 - 新增多代理 root adapters（`CLAUDE.md`/`GEMINI.md`/`AGENTS.md`）。
- 2026-02-09: 1.0.0-beta.21 - 補充本地回歸測試文件與完整跑測紀錄。
- 2026-02-09: 1.0.0-beta.22 - 新增進階整合測試文件（雙訂單生命週期、多標的行情矩陣、無效代號拒絕）並紀錄 2883/2881 成功結果。
- 2026-02-18: 1.0.0-beta.23 - 精簡 SKILL.md 結構（TL;DR、常見錯誤表、具體決策樹、版本相容性矩陣）；統一 Order 建構為 keyword 形式；新增回傳格式參考（response-shapes.md）、當沖工作流程、策略模式參考、錯誤與狀態碼表；本地化規則移至各 adapter 檔；標註期貨/選擇權範圍。
