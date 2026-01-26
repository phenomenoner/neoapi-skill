# Install neoapi-python Skill (Folder or Zip Bundle)

This folder contains a skill for AI coding assistants (Claude Code, Codex) that provides guidance on using the Fubon Neo Python SDK for trading and market data.

## What This Skill Provides

- API documentation references for Fubon Neo SDK
- Implementation patterns for low-latency trading systems
- WebSocket management, error handling, and async patterns
- Order placement and market data best practices

## Contents

- `SKILL.md` - Main skill definition and workflow guidance
- `references/doc-index.md` - Documentation index
- `references/implementation-practices.md` - Production-tested patterns
- `llms*.txt` - LLM-friendly documentation exports
- `VERSION` - Optional semantic version string (recommended)
- `neoapi-python.skill` - Optional packaged archive (ZIP format)

---

## Installation

### Prerequisites

- You have a `neoapi-python` folder (or zip) that contains `SKILL.md`
- PowerShell (Windows) or Bash (macOS/Linux)
- In this repo, the skill lives under `skills/` (not `.skills/`).

### Step 1: Navigate to the skill folder (if using this repo)

```bash
# From project root
# This repo uses "skills/" (no leading dot).
cd .\skills\neoapi-python
```

### Step 2: Install the skill

#### Windows (PowerShell)

**If you have the folder (recommended):**

```powershell
$codexHome = "$env:USERPROFILE\.codex\skills\public"
New-Item -ItemType Directory -Force $codexHome | Out-Null
Copy-Item -Recurse -Force "." "$codexHome\neoapi-python"
```

**If you have a zip (ensure it contains a top-level `neoapi-python/` folder):**

```powershell
$codexHome = "$env:USERPROFILE\.codex\skills\public"
New-Item -ItemType Directory -Force $codexHome | Out-Null
Expand-Archive -Force ".\neoapi-python.zip" "$codexHome"
```

#### macOS/Linux

**If you have the folder (recommended):**

```bash
mkdir -p ~/.codex/skills/public
cp -R ./neoapi-python ~/.codex/skills/public/neoapi-python
```

**If you have a zip (ensure it contains a top-level `neoapi-python/` folder):**

```bash
mkdir -p ~/.codex/skills/public
unzip -o neoapi-python.zip -d ~/.codex/skills/public
```

### Step 3: Verify installation

```bash
# Check the skill was extracted
ls ~/.codex/skills/public/neoapi-python/
# Should show: SKILL.md, INSTALL.md, references/, llms*.txt (and VERSION if present)
```

### Step 4: Restart your AI assistant

Restart Claude Code or Codex to load the new skill.

---

## Offline Docs

The `llms*.txt` files are bundled so the skill works without internet access:

- `llms.txt` / `llms.en.txt` - Navigation index
- `llms-full.txt` / `llms-full.en.txt` - Full documentation content

---

## Rebuilding the Skill Archive (Optional)

After updating skill files, you can rebuild either a `.skill` archive or a `.zip` bundle:

**Windows (PowerShell):**

```powershell
cd .\skills\neoapi-python
Compress-Archive -Path SKILL.md, INSTALL.md, references, llms.txt, llms-full.txt, llms.en.txt, llms-full.en.txt, VERSION -DestinationPath neoapi-python.skill -Force
Compress-Archive -Path .\* -DestinationPath neoapi-python.zip -Force
```

**macOS/Linux:**

```bash
cd ./skills/neoapi-python
zip -r neoapi-python.skill SKILL.md INSTALL.md references/ llms.txt llms-full.txt llms.en.txt llms-full.en.txt VERSION
zip -r neoapi-python.zip .
```

Note: The `.skill` file is a standard ZIP archive with a custom extension.

---

## Versioning (Recommended)

Create a `VERSION` file with a semantic version (e.g., `1.2.0`) and keep it updated when you change the skill. This lets humans and automation compare installed vs. latest versions.

---

## Uninstall

**Windows (PowerShell):**

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.codex\skills\public\neoapi-python"
```

**macOS/Linux:**

```bash
rm -rf ~/.codex/skills/public/neoapi-python
```
