#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-OWNER/REPO}"
BRANCH="${BRANCH:-main}"
SKILL_SUBDIR="${SKILL_SUBDIR:-skills/neoapi-python}"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.codex/skills/public/neoapi-python}"
FORCE="${FORCE:-0}"

if [ "$REPO" = "OWNER/REPO" ]; then
  echo "Usage: $0 <owner/repo>"
  echo "Example: $0 yourorg/neoapi-skill"
  exit 1
fi

remote_version="$(curl -fsSL "https://raw.githubusercontent.com/$REPO/$BRANCH/$SKILL_SUBDIR/VERSION" | tr -d '\r')"
local_version=""
if [ -f "$INSTALL_DIR/VERSION" ]; then
  local_version="$(tr -d '\r' < "$INSTALL_DIR/VERSION")"
fi

if [ "$FORCE" != "1" ] && [ -n "$local_version" ] && [ "$local_version" = "$remote_version" ]; then
  echo "Already up to date ($local_version)."
  exit 0
fi

tmp="$(mktemp -d)"
cleanup() { rm -rf "$tmp"; }
trap cleanup EXIT

curl -fsSL "https://github.com/$REPO/archive/refs/heads/$BRANCH.zip" -o "$tmp/repo.zip"
unzip -q "$tmp/repo.zip" -d "$tmp"

repo_name="$(basename "$REPO")"
src="$tmp/${repo_name}-${BRANCH}/${SKILL_SUBDIR}"
if [ ! -d "$src" ]; then
  echo "Skill subdir not found: $src"
  exit 1
fi

mkdir -p "$(dirname "$INSTALL_DIR")"
rm -rf "$INSTALL_DIR"
cp -R "$src" "$INSTALL_DIR"

echo "Installed $remote_version to $INSTALL_DIR"
