---
name: openclaw-update-checker
description: "Check for OpenClaw updates by comparing installed version against the npm registry. Use when: user asks about updates, version status, or 'is openclaw up to date'. Also useful in heartbeats/cron for periodic update monitoring. Read-only — reports status only, does not modify the system."
---

# OpenClaw Update Checker

Read-only version checker. Compares the installed OpenClaw version against the npm registry and reports whether updates are available. Does not install, modify, or restart anything.

## Usage

```bash
# Human-readable output
python3 scripts/check_update.py

# Machine-readable JSON (for dashboards, cron, integrations)
python3 scripts/check_update.py --format json
```

## Output

**Text mode:** One-liner if current, or a summary showing installed vs latest version and number of versions behind.

**JSON mode:**
```json
{
  "installed": "2026.2.21-2",
  "latest": "2026.2.21-2",
  "up_to_date": true,
  "newer_versions": [],
  "changelog_url": "https://github.com/openclaw/openclaw/releases/tag/v2026.2.21"
}
```

## What It Does

- Runs `openclaw --version` to get the installed version
- Runs `npm show openclaw versions --json` to get available versions
- Compares them and reports the result
- Generates a changelog URL for the latest release

## What It Does NOT Do

- Does not install or update anything
- Does not write to any files
- Does not restart any services
- Does not open network connections (delegates to `npm` CLI)

## Requirements

- `openclaw` and `npm` available in PATH
- No API keys or external services needed
