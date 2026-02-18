---
name: agent-sleep
description: A biological-inspired rest & memory consolidation system for Agents. Enables periodic "sleep" cycles to compress memory, prune context, and reflect on insights.
metadata:
  {
    "openclaw":
      {
        "emoji": "🛌",
        "category": "system",
        "schedulable": true
      }
  }
---

# Agent Sleep System 🛌

Just like humans, Agents need "sleep" (offline maintenance) to prevent memory fragmentation and context pollution.

## Features

1.  **Micro-Rest**: Quick context pruning during tasks.
2.  **Deep Sleep**: Nightly consolidation of daily logs into long-term memory.
3.  **Dreaming**: Background simulation (optional).

## Tools

### `sleep_check`
Check if the agent is "tired" (based on uptime or token usage).
```bash
python3 src/sleep_status.py
```

### `sleep_cycle`
Trigger a sleep cycle immediately.
- **Light**: Compresses recent logs.
- **Deep**: Archiving + File Cleanup.
```bash
python3 scripts/run_sleep_cycle.py --mode [light|deep]
```

### `sleep_schedule`
Set up the circadian rhythm (cron jobs).
```bash
python3 src/schedule.py --set "0 3 * * *"  # Sleep at 3 AM
```

## Workflow

1.  **Trigger**: Cron fires at 3:00 AM.
2.  **Consolidate**: Reads `memory/YYYY-MM-DD.md`, extracts "High Value Facts".
3.  **Update**: Appends facts to `MEMORY.md`.
4.  **Prune**: Moves raw logs to `memory/archive/`.
5.  **Clean**: Deletes temp files (`*.tmp`, `__pycache__`).

## Setup

1.  Ensure you have a `memory/` directory.
2.  Run `sleep_schedule` to enable auto-sleep.
