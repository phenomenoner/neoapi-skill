<div align="center">

# Fubon NeoAPI Skill

Practical Fubon Neo Python SDK guidance for AI coding agents.

[![Skill version](https://img.shields.io/badge/skill-v1.0.0--beta.31-2563eb)](skills/neoapi-python/VERSION)
[![SDK baseline](https://img.shields.io/badge/Fubon_Neo-v2.2.8-0f766e)](https://www.fbs.com.tw/TradeAPI/en/docs/download/download-sdk)
[![Python](https://img.shields.io/badge/Python-3.8%E2%80%933.13-f59e0b)](https://www.fbs.com.tw/TradeAPI/en/docs/install-compatibility)

[繁體中文](README.md) · [Install guide](skills/neoapi-python/INSTALL.md) · [Changelog](CHANGELOG.md) · [Official docs](https://www.fbs.com.tw/TradeAPI/en/)

</div>

> [!IMPORTANT]
> This is a community-maintained AI skill, not the official Fubon SDK. Before live trading, treat the official documentation, test environment, and broker responses as authoritative.

## What does this skill solve?

It turns NeoAPI documentation, sandbox findings, and production-oriented patterns into workflows an AI agent can follow consistently.

| Capability | Coverage |
| :--- | :--- |
| Trading | Login, account selection, place/modify/cancel, fills, and reconciliation |
| Market data | HTTP snapshots, historical data, WebSocket subscriptions, and envelopes |
| Guardrails | Test/prod separation, valid price sources, share units, and compatibility |
| Migration | Step-by-step help porting existing Shioaji code to Fubon NeoAPI |
| Offline docs | Bundled Traditional Chinese and English `llms*.txt` snapshots |

## Install in 30 seconds

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

The default destination is `~/.codex/skills/public/neoapi-python`. Restart Codex or another local-skill-compatible agent after installation. See [INSTALL.md](skills/neoapi-python/INSTALL.md) for custom destinations and manual installation.

## Safety guardrails the agent follows

| Situation | Correct behavior |
| :--- | :--- |
| Valid test-environment order prices | Use `sdk.stock.query_symbol_quote(account, symbol)` |
| Production limit-up / limit-down | Use `intraday.ticker`; `intraday.quote` is trade-oriented |
| Canceled order remains visible | Status `30` in `get_order_results` means canceled |
| Order quantity | Always use shares, not lots; one board lot is 1,000 shares |
| Live fills | `set_on_filled` is primary; `get_order_results` is the periodic safe-net |
| Python version | Officially supported: 3.8–3.13; 3.14 is unsupported |

## Documentation precedence

```text
User question
  └─ Official llms.txt: locate the right page
      └─ Official page .txt / llms-full.txt: verify parameters and examples
          └─ Bundled llms*.txt: offline fallback
              └─ references/: sandbox and implementation notes
```

Official online documentation always takes precedence. The four bundled `llms*.txt` files are offline snapshots, refreshed on **2026-07-17**; the server reported `Last-Modified: 2026-05-07`.

## Repository map

```text
.
├─ skills/neoapi-python/
│  ├─ SKILL.md                 # Agent entry point and decision rules
│  ├─ references/              # Sandbox, response-shape, and implementation guides
│  ├─ llms*.txt                # Offline official docs snapshots (zh/en)
│  ├─ VERSION                  # Skill version
│  └─ neoapi-python.skill      # Locally built portable ZIP bundle (git ignored)
├─ AGENTS.md / CLAUDE.md / GEMINI.md
├─ update-skill.ps1 / update-skill.sh
└─ .test/                      # Maintainer integration tests; not shipped in bundle
```

## Maintenance and verification

When docs or skill rules change:

1. Sync all four official zh/en `llms*.txt` endpoints.
2. Update `SKILL.md`, `VERSION`, references, and all three adapters.
3. Rebuild `neoapi-python.skill` and verify archive contents and version parity.
4. Run static checks or the `.test/test_runner.py` integration suites at the tier required by the change.

Release `v1.0.0-beta.31` refreshes the official snapshots, corrects the SDK v2.2.8 / Python 3.8–3.13 baseline, and redesigns the README navigation. See [CHANGELOG.md](CHANGELOG.md) for the full history.
