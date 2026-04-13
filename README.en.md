# Fubon NeoAPI Skill Refinement

Primary README (Chinese): [README.md](README.md)

This repository is used to test and refine the `neoapi-python` skill bundle for AI coding assistants (Codex, Claude Code). The skill provides guidance for the Fubon Neo Python SDK, including trading and market data workflows.

## Repo Layout

- `skills/neoapi-python/` - The skill bundle (SKILL.md, references, llms*.txt, VERSION, INSTALL.md)
- `update-skill.ps1` - Windows update helper (pulls from GitHub and installs to `~/.codex/skills/public/`)
- `update-skill.sh` - macOS/Linux update helper

## Compatibility

The skill is packaged as plain files with a `SKILL.md` entry point. This keeps the bundle portable across AI platforms that accept local skill bundles or custom instruction folders. For non-Codex platforms, set the install destination to that platform’s skill/instruction folder (use the `INSTALL_DIR` parameter or env var in the update scripts).

## GitHub Repo

- `https://github.com/phenomenoner/neoapi-skill`

## Install

See `skills/neoapi-python/INSTALL.md` for full instructions. This repo uses `skills/` (no leading dot). End users install to:

- Windows: `%USERPROFILE%\.codex\skills\public\neoapi-python`
- macOS/Linux: `~/.codex/skills/public/neoapi-python`

## Versioning

The skill version is stored in `skills/neoapi-python/VERSION` using semver. Current version: `1.0.0-beta.29` (Beta 1.0.0).

## Multi-Agent Adapters

Root-level adapter files are provided for major agents, with Chinese-first guidance and English supplement:

- `CLAUDE.md`
- `GEMINI.md`
- `AGENTS.md`

These adapters point to `skills/neoapi-python/` as the canonical source.

## LLM Docs (Online)

The official LLM-oriented pages and `llms*.txt` endpoints are available online and should be treated as primary references:

- `https://www.fbs.com.tw/TradeAPI/docs/welcome/build-with-llm`
- `https://www.fbs.com.tw/TradeAPI/en/docs/welcome/build-with-llm/`
- `https://www.fbs.com.tw/TradeAPI/llms.txt`
- `https://www.fbs.com.tw/TradeAPI/llms-full.txt`
- `https://www.fbs.com.tw/TradeAPI/en/llms.txt`
- `https://www.fbs.com.tw/TradeAPI/en/llms-full.txt`

The bundled `llms*.txt` files are offline snapshots. When the official endpoints change, refresh the repo copies and bump `VERSION`; otherwise the update scripts will treat the installed bundle as unchanged.

## Updating from GitHub

The update scripts download the repo zip from GitHub, copy `skills/neoapi-python` into the install location, and compare `VERSION` to skip if already up to date.

Example:

```powershell
.\update-skill.ps1 -Repo phenomenoner/neoapi-skill
```

```bash
./update-skill.sh phenomenoner/neoapi-skill
```

## Local Regression Testing

- Local integrated runner: `.test/test_runner.py` (not included in published skill bundle).
- Logs are written to `.test/logs/` as both text and JSON summaries.
- Suites:
  - `smoke`: basic login + market/trade sanity checks
  - `complex`: multi-symbol marketdata matrix + dual-order lifecycle
  - `all`: full coverage (includes complex checks)

## Changelog

The full release history is maintained in [CHANGELOG.md](CHANGELOG.md).

The current latest version is `1.0.0-beta.29`, with the main update being WebSocket message-envelope and `on_message` parsing guidance, clarifying that the actual trade payload lives under `message["data"]`.
