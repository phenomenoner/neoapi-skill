<div align="center">

# Fubon NeoAPI Skill

給 AI 編碼代理使用的富邦新一代（Fubon Neo）Python SDK 實戰指南。

[![Skill version](https://img.shields.io/badge/skill-v1.0.0--beta.32-2563eb)](skills/neoapi-python/VERSION)
[![SDK baseline](https://img.shields.io/badge/Fubon_Neo-v2.2.8-0f766e)](https://www.fbs.com.tw/TradeAPI/docs/download/download-sdk)
[![Python](https://img.shields.io/badge/Python-3.8%E2%80%933.13-f59e0b)](https://www.fbs.com.tw/TradeAPI/docs/install-compatibility)

[English](README.en.md) · [安裝指南](skills/neoapi-python/INSTALL.md) · [版本紀錄](CHANGELOG.md) · [官方文件](https://www.fbs.com.tw/TradeAPI/)

</div>

> [!IMPORTANT]
> 這是社群維護的 AI skill，不是富邦官方 SDK。交易程式上線前，請以官方文件、測試環境與券商回報為最終依據。

## 這個 skill 解決什麼？

它把散落在官方文件、測試環境經驗與實務專案裡的 NeoAPI 知識，整理成 AI 可以穩定遵循的工作流程。

| 能力 | 內容 |
| :--- | :--- |
| 交易流程 | 登入、選帳號、下單、改單、刪單、成交回報與對帳 |
| 行情資料 | HTTP 快照、歷史行情、WebSocket 訂閱與訊息 envelope |
| 安全護欄 | 測試／正式環境分流、價格來源、股數單位、版本相容性 |
| 遷移協助 | 將既有 Shioaji 程式逐步移植到 Fubon NeoAPI |
| 離線文件 | 內建繁中／英文 `llms*.txt` 快照，斷線時仍可查詢 |

## 30 秒安裝

### Windows / PowerShell

```powershell
git clone https://github.com/phenomenoner/neoapi-skill.git
cd neoapi-skill
.\update-skill.ps1
```

### macOS / Linux

```bash
git clone https://github.com/phenomenoner/neoapi-skill.git
cd neoapi-skill
bash ./update-skill.sh
```

預設會安裝到 `~/.codex/skills/public/neoapi-python`。完成後重啟 Codex 或其他支援本地 skill 的代理；自訂路徑與手動安裝方式請見 [INSTALL.md](skills/neoapi-python/INSTALL.md)。

## AI 會遵守的關鍵護欄

| 情境 | 正確做法 |
| :--- | :--- |
| 測試環境判斷可下單價格 | 使用 `sdk.stock.query_symbol_quote(account, symbol)` |
| 正式行情查漲跌停 | 使用 `intraday.ticker`；`intraday.quote` 偏成交行情 |
| 取消單仍出現在查詢結果 | `get_order_results` 的 status `30` 代表已刪單 |
| 訂單數量 | 一律填「股數」，不是張數；1 張 = 1000 股 |
| 即時成交 | `set_on_filled` 為主路徑，`get_order_results` 作週期性 safe-net |
| 預設憑證密碼 | SDK >= 1.3.2 省略 `login` 第 4 參數，不傳空字串 |
| WebSocket 零價格 | 搭配 `isLimitUp*` / `isLimitDown*` 旗標解碼，不比對 `"市價"` |
| Python 版本 | 官方目前支援 3.8–3.13；不支援 3.14 |

## 文件來源策略

```text
使用者問題
  └─ 官方 llms.txt：快速找到正確頁面
      └─ 官方頁面 .txt / llms-full.txt：核對參數與範例
          └─ bundled llms*.txt：離線 fallback
              └─ references/：測試環境與實務補充
```

線上官方文件永遠優先；bundle 內的四份 `llms*.txt` 是離線快照。本版於 **2026-07-17** 重新抓取，官方伺服器回報 `Last-Modified: 2026-05-07`。

## Repo 地圖

```text
.
├─ skills/neoapi-python/
│  ├─ SKILL.md                 # AI 的主入口與決策規則
│  ├─ references/              # 測試環境、回傳格式、實作指南
│  ├─ llms*.txt                # 官方文件離線快照（zh/en）
│  ├─ VERSION                  # skill 版本
│  └─ neoapi-python.skill      # 本地建立的可攜式 ZIP bundle（git ignored）
├─ AGENTS.md / CLAUDE.md / GEMINI.md
├─ update-skill.ps1 / update-skill.sh
└─ .test/                      # 維護者本地整合測試（不隨 bundle 發佈）
```

## 維護與驗證

文件或 skill 規則更新時：

1. 同步四個官方 zh/en `llms*.txt` 端點。
2. 更新 `SKILL.md`、`VERSION`、references 與三份 adapter。
3. 重建 `neoapi-python.skill`，檢查封裝內容與版本一致。
4. 依變更風險執行靜態檢查或 `.test/test_runner.py` 整合套件。

本次 `v1.0.0-beta.32` 修正預設憑證登入與 WebSocket 零價格／漲跌停旗標判讀，對應 Issues #1、#2。完整歷程請見 [CHANGELOG.md](CHANGELOG.md)。
