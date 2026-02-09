# Fubon NeoAPI Skill Refinement

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

The skill version is stored in `skills/neoapi-python/VERSION` using semver. Current version: `1.0.0-beta.21` (Beta 1.0.0).

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

## Changelog

- 2026-01-26: 1.0.0-beta.1 - Initial beta version, add update scripts, VERSION, and repo metadata.
- 2026-01-26: 1.0.0-beta.1 - Clarify install paths and cross-platform compatibility notes.
- 2026-01-26: 1.0.0-beta.1 - Initialize GitHub repo and set default update script repo.
- 2026-01-26: 1.0.0-beta.2 - Add test environment reference doc and sandbox setup notes.
- 2026-01-26: 1.0.0-beta.2 - Add local smoke test script under `.test` (ignored).
- 2026-01-26: 1.0.0-beta.3 - Document SDK download/install (wheel) and test bundle details.
- 2026-01-26: 1.0.0-beta.4 - Record local test validation results.
- 2026-01-26: 1.0.0-beta.5 - Add SDK install snippet and Python version guidance.
- 2026-01-26: 1.0.0-beta.6 - Add SDK install quick note to SKILL.md.
- 2026-01-26: 1.0.0-beta.7 - Add skill validation test cases and contribution guidance.
- 2026-01-26: 1.0.0-beta.8 - Record skill test run results.
- 2026-01-26: 1.0.0-beta.9 - Add order placement test results to skill tests.
- 2026-01-26: 1.0.0-beta.10 - Add examples guidance doc and link it in SKILL/doc index; update TODO.
- 2026-01-26: 1.0.0-beta.11 - Note .md URL deprecation; rely on llms.txt/llms-full.txt.
- 2026-01-27: 1.0.0-beta.12 - Clarify market data init and test-vs-prod limit price guidance.
- 2026-01-27: 1.0.0-beta.13 - Clarify intraday.ticker usage and order status behavior in test env.
- 2026-01-27: 1.0.0-beta.14 - Update doc paths (no .md) and add integrated test result notes.
- 2026-02-03: 1.0.0-beta.15 - Add Usage Cheat Sheet to SKILL.md (Quickstart, Enums) and Shioaji migration guide.
- 2026-02-03: 1.0.0-beta.16 - Add "Crafting Migration Experience" log and "Agent Instruction for Migration" guide.
- 2026-02-03: 1.0.0-beta.17 - Add Localization and Bilingual Terminology to SKILL.md.
- 2026-02-09: 1.0.0-beta.18 - Add Build-with-LLM links and prioritize online llms*.txt endpoints in skill docs.
- 2026-02-09: 1.0.0-beta.19 - Refresh bundled llms*.txt from official endpoints and normalize doc paths to extensionless format.
- 2026-02-09: 1.0.0-beta.20 - Add root adapters (CLAUDE.md, GEMINI.md, AGENTS.md) for multi-agent support.
- 2026-02-09: 1.0.0-beta.21 - Add local regression suite documentation and record full-suite validation.
