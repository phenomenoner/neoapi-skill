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

The skill version is stored in `skills/neoapi-python/VERSION` using semver. Current version: `1.0.0-beta.7` (Beta 1.0.0).

## Updating from GitHub

The update scripts download the repo zip from GitHub, copy `skills/neoapi-python` into the install location, and compare `VERSION` to skip if already up to date.

Example:

```powershell
.\update-skill.ps1 -Repo phenomenoner/neoapi-skill
```

```bash
./update-skill.sh phenomenoner/neoapi-skill
```

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
