# Changelog — neoapi-skill / neoapi-python

This changelog is a **minimal index** derived from the version notes already present in `README.md`.
If details diverge, treat `README.md` + `skills/neoapi-python/VERSION` as the source of truth.

## 1.0.0-beta.24 — 2026-03-26

- Refreshed bundled official `llms.txt` / `llms-full.txt` snapshots for both zh and en variants.
- Updated `README.md` / `README.en.md` to document the llms snapshot refresh rule and the need to bump `VERSION` when bundled snapshots change.
- Bumped `skills/neoapi-python/VERSION` and `SKILL.md` to `1.0.0-beta.24` so update scripts can deliver the refresh.

## 1.0.0-beta.23 — 2026-02-18

- Restructured `SKILL.md` for higher agent reliability (TL;DR, error table, decision tree).
- Expanded response-shape references, day-trade workflow notes, and status/error code tables.
- Moved localization rules into per-agent adapter docs.

## 1.0.0-beta.20 — 2026-02-09

- Added multi-agent root adapters (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`).

## 1.0.0-beta.1 — 2026-01-26

- Initial beta: update scripts, VERSIONing, install guidance.

## Notes

Intermediate betas exist and are recorded in `README.md`; they are not duplicated here.
