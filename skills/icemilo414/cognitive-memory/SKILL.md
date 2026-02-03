---
name: cognitive-memory
description: Intelligent multi-store memory system with human-like encoding, consolidation, decay, and recall. Use when setting up agent memory, configuring remember/forget triggers, enabling sleep-time reflection, building knowledge graphs, or adding audit trails. Replaces basic flat-file memory with a cognitive architecture featuring episodic, semantic, procedural, and core memory stores. Supports multi-agent systems with shared read, gated write access model. Includes philosophical meta-reflection that deepens understanding over time. Covers MEMORY.md, episode logging, entity graphs, decay scoring, reflection cycles, evolution tracking, and system-wide audit.
---

# Cognitive Memory System

Multi-store memory with natural language triggers, knowledge graphs, decay-based forgetting, reflection consolidation, philosophical evolution, multi-agent support, and full audit trail.

## Quick Setup

### 1. Run the init script

```bash
bash scripts/init_memory.sh /path/to/workspace
```

Creates directory structure, initializes git for audit tracking, copies all templates.

### 2. Update config

Add to `~/.clawdbot/clawdbot.json` (or `moltbot.json`):

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "voyage",
    "sources": ["memory", "sessions"],
    "indexMode": "hot",
    "minScore": 0.3,
    "maxResults": 20
  }
}
```

### 3. Add agent instructions

Append `assets/templates/agents-memory-block.md` to your AGENTS.md.

### 4. Verify

```
User: "Remember that I prefer TypeScript over JavaScript."
Agent: [Classifies → writes to semantic store + core memory, logs audit entry]

User: "What do you know about my preferences?"
Agent: [Searches core memory first, then semantic graph]
```

---

## Architecture — Four Memory Stores

```
CONTEXT WINDOW (always loaded)
├── System Prompts (~4-5K tokens)
├── Core Memory / MEMORY.md (~3K tokens)  ← always in context
└── Conversation + Tools (~185K+)

MEMORY STORES (retrieved on demand)
├── Episodic   — chronological event logs (append-only)
├── Semantic   — knowledge graph (entities + relationships)
├── Procedural — learned workflows and patterns
└── Vault      — user-pinned, never auto-decayed

ENGINES
├── Trigger Engine    — keyword detection + LLM routing
├── Reflection Engine — 5-phase consolidation with meta-reflection
└── Audit System      — git + audit.log for all file mutations
```

### File Structure

```
workspace/
├── MEMORY.md                    # Core memory (~3K tokens)
├── memory/
│   ├── episodes/                # Daily logs: YYYY-MM-DD.md
│   ├── graph/                   # Knowledge graph
│   │   ├── index.md             # Entity registry + edges
│   │   ├── entities/            # One file per entity
│   │   └── relations.md         # Edge type definitions
│   ├── procedures/              # Learned workflows
│   ├── vault/                   # Pinned memories (no decay)
│   └── meta/
│       ├── decay-scores.json    # Relevance tracking
│       ├── reflection-log.md    # Consolidation history
│       ├── pending-reflection.md # Current reflection proposal
│       ├── pending-memories.md  # Sub-agent proposals
│       ├── evolution.md         # Philosophical evolution tracker
│       └── audit.log            # System-wide change log
└── .git/                        # Audit ground truth
```

---

## Trigger System

**Remember:** "remember", "don't forget", "keep in mind", "note that", "important:", "for future reference", "save this"
→ Classify via routing prompt, write to appropriate store, update decay scores

**Forget:** "forget about", "never mind", "disregard", "scratch that", "remove from memory"
→ Confirm target, soft-archive (decay=0), log in audit

**Reflect:** "reflect on", "consolidate memories", "review memories"
→ Run 5-phase reflection cycle, present summary for approval

---

## Decay Model

```
relevance(t) = base × e^(-0.03 × days_since_access) × log2(access_count + 1) × type_weight
```

| Score | Status | Behavior |
|-------|--------|----------|
| 1.0–0.5 | Active | Fully searchable |
| 0.5–0.2 | Fading | Deprioritized |
| 0.2–0.05 | Dormant | Explicit search only |
| < 0.05 | Archived | Hidden from search |

Type weights: core=1.5, episodic=0.8, semantic=1.2, procedural=1.0, vault=∞

---

## Reflection Engine — 5 Phases

**Token Budgets:**
- Input: ~30,000 tokens max
- Output: 8,000 tokens max

**Scope Rules (CRITICAL):**
- ✅ Episodes: Only since `last_reflection` (first run: last 7 days)
- ✅ Graph entities: Only decay > 0.3
- ✅ Reflection-log: Last 5 entries only
- ❌ NEVER read: code, configs, transcripts, files outside memory/

1. **Survey** — Read scoped memory stores. Plan consolidation.

2. **Meta-Reflection** — Review last 5 reflections + evolution.md (not full history).

3. **Consolidate** — Extract facts, build graph, detect contradictions, propose archival.

4. **Rewrite Core** — Update MEMORY.md. Stay under 3K tokens.

5. **Summarize** — Generate pending-reflection.md with philosophical evolution section.

**User approval required.** Never auto-applied.

**After reflection:** Update `last_reflection` timestamp in decay-scores.json.

**Evolution milestones:** #10, #25, #50, #100 trigger deeper meta-analysis.

See `references/reflection-process.md` for full prompts and pruning rules.

---

## Multi-Agent Memory Access

**Model: Shared Read, Gated Write**

- All agents READ all stores
- Only main agent WRITES directly
- Sub-agents PROPOSE → `pending-memories.md`
- Main agent REVIEWS and commits

Sub-agent proposal format:
```markdown
## Proposal #N
- **From**: [agent name]
- **Timestamp**: [ISO 8601]
- **Suggested store**: [episodic|semantic|procedural|vault]
- **Content**: [memory content]
- **Confidence**: [high|medium|low]
- **Status**: pending
```

---

## Audit Trail

**Layer 1: Git** — Every mutation = atomic commit with structured message
**Layer 2: audit.log** — One-line queryable summary

Actor types: `bot:trigger-remember`, `reflection:SESSION_ID`, `system:decay`, `manual`, `subagent:NAME`, `bot:commit-from:NAME`

**Critical file alerts:** SOUL.md, IDENTITY.md changes flagged ⚠️ CRITICAL

---

## Key Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Core memory cap | 3,000 tokens | Always in context |
| Evolution.md cap | 2,000 tokens | Pruned at milestones |
| Reflection input budget | ~30,000 tokens | Episodes + graph + meta |
| Reflection output budget | 8,000 tokens | All phases combined |
| Decay λ | 0.03 | ~23 day half-life |
| Archive threshold | 0.05 | Below = hidden |
| Reflection-log entries | 20 full | Older → archive with summary line |
| Audit log retention | 90 days | Older → monthly digests |

---

## Reference Materials

- `references/architecture.md` — Full design document (1200+ lines)
- `references/routing-prompt.md` — LLM memory classifier
- `references/reflection-process.md` — 5-phase reflection prompts

## Troubleshooting

**Memory not persisting?** Check `memorySearch.enabled: true`, verify MEMORY.md exists, restart gateway.

**Reflection not running?** Ensure previous reflection was approved/rejected.

**Audit trail not working?** Check `.git/` exists, verify `audit.log` is writable.
