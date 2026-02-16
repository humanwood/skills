---
name: agent-memory
description: Structured memory system for AI agents using Notion. Use when setting up agent memory, discussing memory persistence, or helping agents remember context across sessions. Includes ACT framework databases, MEMORY.md templates, and the Continuity Cycle pattern.
---

# Agent Memory

Give your agent structured memory using Notion databases.

## Quick Start

1. Create Notion integration at notion.so/my-integrations
2. Store token: `echo "ntn_XXX" > ~/.config/notion/api_key`
3. Create Agent Workspace page with 3 ACT databases (see references/act-framework.md)
4. Add MEMORY.md to agent's system prompt (see assets/MEMORY-TEMPLATE.md)

## The Memory Stack

### Layer 1: Daily Logs (`memory/YYYY-MM-DD.md`)
Raw event logs — what happened, when. Quick capture during work.

### Layer 2: Long-term Memory (`MEMORY.md`)
Curated knowledge: patterns, preferences, lessons learned, active projects.

### Layer 3: Notion (ACT Databases)
Structured external memory the agent can query and update via API.

## The ACT Framework

Three databases for structured agent cognition:

| Database | Purpose | When to use |
|----------|---------|-------------|
| ACT I: Hidden Narratives | Track patterns, assumptions, blind spots | Discovery/reflection |
| ACT II: Limitless (MMM) | Mindset/Methods/Motivation breakthroughs | Growth moments |
| ACT III: Ideas Pipeline | Capture → evaluate → ship ideas | Ongoing |

**Full schemas:** See `references/act-framework.md`

## The Continuity Cycle

```
DO WORK → DOCUMENT → UPDATE INSTRUCTIONS → NEXT SESSION STARTS SMARTER
```

**Two Steps Forward:** Before marking anything done, ask: "If I woke up tomorrow with no memory, could I pick up exactly where I left off?"

**Full pattern:** See `references/continuity-cycle.md`

## Notion API Patterns

### Query database
```bash
curl -s "https://api.notion.com/v1/databases/$DB_ID/query" \
  -H "Authorization: Bearer $(cat ~/.config/notion/api_key)" \
  -H 'Notion-Version: 2022-06-28' \
  -H 'Content-Type: application/json' \
  -d '{"filter": {"property": "Status", "select": {"equals": "in progress"}}}'
```

### Add entry
```bash
curl -X POST 'https://api.notion.com/v1/pages' \
  -H "Authorization: Bearer $(cat ~/.config/notion/api_key)" \
  -H 'Notion-Version: 2022-06-28' \
  -H 'Content-Type: application/json' \
  -d '{
    "parent": {"database_id": "'$DB_ID'"},
    "properties": {
      "Idea": {"title": [{"text": {"content": "Your idea"}}]},
      "Status": {"select": {"name": "captured"}}
    }
  }'
```

## Daily Routine

**Session start:**
1. Read MEMORY.md
2. Read today's `memory/YYYY-MM-DD.md`
3. Check Notion for in-progress items

**During work:**
- Log to daily memory file immediately
- New insight → ACT I
- Breakthrough → ACT II
- New idea → ACT III

**Session end:**
- Update MEMORY.md with long-term learnings
- Update Notion statuses

## Files

- `references/act-framework.md` — Full database schemas
- `references/continuity-cycle.md` — Complete Continuity Cycle pattern
- `assets/MEMORY-TEMPLATE.md` — Drop-in MEMORY.md for agents
