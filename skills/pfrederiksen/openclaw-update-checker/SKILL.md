---
name: openclaw-update-checker
description: "Check for OpenClaw updates by comparing installed version against npm registry. Use when: user asks about updates, version status, or 'is openclaw up to date'. Also useful in heartbeats/cron for periodic update monitoring. Reports installed vs latest version, changelog URL, and update command."
---

# OpenClaw Update Checker

Check if the installed OpenClaw version is current, and report available updates with changelog links.

## Usage

```bash
# Text output (human-readable)
python3 scripts/check_update.py

# JSON output (for dashboards, cron jobs, integrations)
python3 scripts/check_update.py --format json
```

## Output

**Text mode** prints a one-liner if current, or a summary with version diff, changelog URL, and update command if behind.

**JSON mode** returns:
```json
{
  "installed": "2026.2.21-2",
  "latest": "2026.2.21-2",
  "up_to_date": true,
  "newer_versions": [],
  "changelog_url": "https://github.com/openclaw/openclaw/releases/tag/v2026.2.21",
  "update_command": "npm i -g openclaw@2026.2.21-2"
}
```

## Update Workflow

When an update is available:
1. Run the check script to get the latest version
2. Fetch the changelog URL to summarize what's new
3. Ask the user before updating (it requires a gateway restart)
4. Update: `npm i -g openclaw@<version>`
5. Restart: `openclaw gateway restart`

## Integration

Add to a cron job or heartbeat for periodic checks. Pair with `web_fetch` on the changelog URL to summarize release notes for the user.

## Requirements

- `openclaw` CLI installed globally via npm
- `npm` available in PATH
- No API keys or external services needed
