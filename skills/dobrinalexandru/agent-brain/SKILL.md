---
name: agent-brain
description: "Continuous learning system for AI agents with 6 cognitive modules"
homepage: https://github.com/alexdobri/clawd/tree/main/skills/agent-brain
metadata:
  clawdbot:
    emoji: 🧠
    modules: [archive, ingest, vibe, gauge, signal, ritual]
---

# Agent Brain 🧠

Continuous learning system for AI agents. Like a human brain - learns, remembers, and improves from experience.

## External Endpoints

| Endpoint | Data Sent | Data Received |
|----------|-----------|---------------|
| None | This is an instruction-only skill | N/A |

## Security & Privacy

This skill runs locally. No data leaves your machine. Memory is stored in `memory/` folder only.

## Model Invocation

This skill runs autonomously on every task. You can disable by unloading the skill.

## Trust

By using this skill, you agree to its instructions operating in your sessions. Only install if you trust the skill author.

## Overview

One skill with 6 cognitive modules:

| Module | File | Function |
|--------|------|----------|
| **Archive** | `modules/archive/SKILL.md` | Memory encoding, retrieval |
| **Ingest** | `modules/ingest/SKILL.md` | External knowledge ingestion |
| **Vibe** | `modules/vibe/SKILL.md` | Emotional tone detection |
| **Gauge** | `modules/gauge/SKILL.md` | Confidence, resources |
| **Signal** | `modules/signal/SKILL.md` | Conflict detection |
| **Ritual** | `modules/ritual/SKILL.md` | Habit formation |

## How It Works

This skill runs automatically. The dispatcher selects only relevant modules per task - not all modules run every time.

## Core Loop

```
Task received
    ↓
[DISPATCHER] → Determine which modules needed
    ↓
[RELEVANT MODULES] → Only run these
    ↓
[EXECUTE]
    ↓
[ARCHIVE] → Store outcome (always)
```

### Module Selection by Task Type

| Task Type | Modules Run |
|-----------|-------------|
| Simple question | Gauge + Archive |
| URL provided | Gauge + Ingest + Archive + Vibe |
| Recurring task | Gauge + Ritual + Vibe |
| Error check | Gauge + Signal + Vibe |
| New topic | Gauge + Archive + Ingest + Signal + Vibe |

## Usage

```
/skill agent-brain
```

All 6 modules included - no extra installs needed.
