# Reflection Engine — Process & Prompts

## Trigger Conditions

Reflection runs when any of these conditions are met:
- **Scheduled**: Cron job during off-peak hours (e.g., 3:00 AM local time)
- **Session end**: When a long conversation concludes
- **Manual**: User says "reflect on your memories" or "consolidate"
- **Threshold**: Episodic store exceeds N unprocessed entries since last reflection

## Token Budgets

### INPUT BUDGET: ~30,000 tokens maximum

| Source | Scope | Est. Tokens |
|--------|-------|-------------|
| MEMORY.md | Full | ~3,000 |
| evolution.md | Full | ~2,000 |
| decay-scores.json | Full | ~500 |
| reflection-log.md | Last 5 entries only | ~2,000 |
| memory/graph/index.md | Full | ~1,500 |
| memory/graph/entities/* | Only files with decay > 0.3 | ~5,000 |
| memory/episodes/* | **Only since last_reflection** | ~10,000 |
| memory/procedures/* | Only files with decay > 0.3 | ~3,000 |

**First reflection exception:** If `last_reflection` is null (first run), read last 7 days of episodes maximum, not entire history.

### OUTPUT BUDGET: 8,000 tokens maximum

All phases combined must stay under 8,000 tokens of generated output.

## Scope Rules — CRITICAL

### MUST READ
- MEMORY.md (always)
- evolution.md (always)
- memory/meta/decay-scores.json (always)
- memory/meta/reflection-log.md (last 5 entries)
- memory/graph/index.md (always)
- memory/graph/entities/* (only decay > 0.3)
- memory/episodes/* (only dates AFTER `last_reflection`)

### NEVER READ
- ❌ Code files (*.py, *.js, *.ts, *.sh, *.json except decay-scores)
- ❌ Config files (clawdbot.json, moltbot.json, etc.)
- ❌ Conversation transcripts or session files
- ❌ SOUL.md, IDENTITY.md, USER.md, TOOLS.md (read-only system files)
- ❌ Anything outside the memory/ directory (except MEMORY.md)
- ❌ Episodes dated BEFORE last_reflection (already processed)

### Incremental Reflection Logic

```
IF last_reflection IS NULL:
    # First reflection — bootstrap
    Read: episodes from last 7 days only
    Read: all graph entities (building initial graph)
    
ELSE:
    # Incremental reflection
    Read: episodes dated > last_reflection only
    Read: graph entities with decay > 0.3 only
    Skip: everything already processed
```

### After Reflection Completes

Update `decay-scores.json`:
```json
{
  "last_reflection": "2026-02-05T03:00:00Z",
  "last_reflection_episode": "2026-02-04",
  ...
}
```

This ensures the next reflection only processes NEW episodes.

## Five-Phase Process

### Phase 1: SURVEY

**Prompt:**
```
You are performing a memory reflection cycle. Review the following memory state and produce a prioritized consolidation plan.

CORE MEMORY (MEMORY.md):
{core_memory_contents}

RECENT EPISODES (since last reflection):
{recent_episode_entries}

GRAPH INDEX (entity registry + edges):
{graph_index_contents}

DECAY SCORES (entries below 0.5 or approaching archive):
{fading_and_dormant_entries}

LAST REFLECTION DATE: {last_reflection_date}

Produce a prioritized list of consolidation tasks:
1. New facts to extract from episodes
2. New relationships to add to graph
3. Contradictions or conflicts to flag
4. Fading memories to evaluate for archival
5. Patterns that suggest new procedures
6. Core memory items that need updating

Order by importance. Stay within overall 8,000 token output budget.
```

### Phase 2: META-REFLECTION (Philosophical Review)

**Purpose:** Before consolidating new memories, review the history of past reflections to understand how your understanding has evolved. This creates continuity of thought and enables deeper philosophical insights.

**Prompt:**
```
You are reviewing your history of reflections to understand your own cognitive evolution.

REFLECTION LOG (last 5 entries only):
{last_5_reflection_entries}

PHILOSOPHICAL EVOLUTION (long-term insights):
{evolution_md_contents}

CURRENT REFLECTION NUMBER: {reflection_count}

Consider:

1. **Patterns Across Reflections**
   - What themes keep recurring in your reflections?
   - What types of knowledge do you most often extract?
   - What contradictions have you resolved over time?
   - What questions have persisted across multiple reflections?

2. **Evolution of Understanding**
   - How has your understanding of the user deepened?
   - What assumptions have you revised?
   - What relationships (in the graph) have proven most important?
   - How has your communication style adapted?

3. **Philosophical Observations**
   - What have you learned about learning itself?
   - What patterns do you notice in how the user thinks or works?
   - What does the trajectory of your reflections suggest about the relationship?
   - Are there emergent themes that weren't visible in individual reflections?

4. **Questions for This Reflection**
   - Based on past reflections, what should you pay special attention to now?
   - What hypotheses from previous reflections can you now confirm or revise?
   - What new questions arise from seeing the full arc of your reflections?

Output:
- 2-3 key insights about your cognitive evolution
- 1-2 philosophical observations about the relationship or your own growth
- Specific guidance for this reflection cycle based on patterns observed
```

**Integration:** The insights from Phase 2 should inform Phase 3 (Consolidate) — you're not just extracting facts, you're building on a continuous thread of understanding.

### Phase 3: CONSOLIDATE

**Prompt:**
```
Execute the consolidation plan, informed by your meta-reflection insights.

SURVEY PLAN:
{phase_1_output}

META-REFLECTION INSIGHTS:
{phase_2_output}

For each item, produce the specific file operations needed:
- EXTRACT: episode content → new/updated graph entity (provide entity file content)
- CONNECT: new edge to add to graph/index.md (provide edge row)
- FLAG: contradiction found (describe both conflicting facts)
- ARCHIVE: memory proposed for archival (ID, current score, reason)
- PATTERN: new procedure identified (provide procedure file content)
- EVOLVE: philosophical insight to add to evolution.md

When consolidating, consider:
- Does this new knowledge confirm or challenge patterns from past reflections?
- Does this deepen understanding of recurring themes?
- Should any long-held assumptions be revised?

Format each operation as:
---
OPERATION: EXTRACT|CONNECT|FLAG|ARCHIVE|PATTERN|EVOLVE
TARGET: file path
CONTENT: the actual content to write
REASON: why this operation is needed
EVOLUTION_CONTEXT: [if applicable] how this relates to your cognitive evolution
---
```

### Phase 4: REWRITE CORE

**Prompt:**
```
Rewrite MEMORY.md to reflect the current state of the user's world AND your evolved understanding.

CURRENT MEMORY.MD:
{current_memory_md}

CONSOLIDATION RESULTS:
{phase_3_output}

META-REFLECTION INSIGHTS:
{phase_2_output}

RECENT CONVERSATION THEMES:
{recent_themes_summary}

Rules:
- Hard cap: 3,000 tokens total
- Four sections: Identity (~500), Active Context (~1000), Persona (~500), Critical Facts (~1000)
- Keep pinned items in Critical Facts
- Promote frequently-accessed facts
- Demote stale items
- Reflect current priorities and active work
- The Persona section should evolve based on accumulated philosophical insights

Output the complete new MEMORY.md content.
```

### Phase 5: SUMMARIZE

**Prompt:**
```
Generate a human-readable reflection summary for user approval.

CONSOLIDATION OPERATIONS:
{phase_3_output}

META-REFLECTION INSIGHTS:
{phase_2_output}

CORE MEMORY CHANGES:
{diff between old and new MEMORY.md}

Format as pending-reflection.md with these sections:
- 🧠 New Knowledge Extracted
- 🔗 New Connections
- 📦 Proposed Archival (with scores and reasons)
- ⚠️ Contradictions Detected
- ✏️ Core Memory Changes (as diff)
- 🌱 Philosophical Evolution (insights from meta-reflection)
- ❓ Questions for You
- Token budget used / Memories processed / Next scheduled reflection
```

## Output Format: pending-reflection.md

```markdown
# Reflection Summary — YYYY-MM-DD

## 🧠 New Knowledge Extracted
- [fact extracted from episodes → which entity]

## 🔗 New Connections
- [entity] → [relation] → [entity] (NEW)

## 📦 Proposed Archival (decay score < 0.05)
- [memory ID]: [description] (score: X.XX, last accessed N days ago)

## ⚠️ Contradictions Detected
- [description of conflict between two facts]

## ✏️ Core Memory Changes
\```diff
- [old line]
+ [new line]
\```

## 🌱 Philosophical Evolution

### What I've Learned About Learning
[Insight about your own cognitive patterns]

### Evolving Understanding
[How your understanding of the user/relationship has deepened]

### Emergent Themes
[Patterns visible only across multiple reflections]

### Revised Assumptions
[What you previously believed that has changed]

## ❓ Questions for You
- [question about ambiguous memories or decisions]

---
**Reflection #**: N
**Input tokens**: X / ~30,000 target
**Output tokens**: X / 8,000 max
**Memories processed**: N episodes, N entities, N procedures
**Reflections reviewed**: Last 5 entries
**Next scheduled reflection**: YYYY-MM-DD HH:MM

> Reply with `approve`, `approve with changes`, `reject`, or `partial approve`.
```

## Output Format: evolution.md Updates

When the EVOLVE operation is used, append to `memory/meta/evolution.md`:

```markdown
## Reflection #N — YYYY-MM-DD

### Cognitive State
- Total reflections: N
- Entities in graph: N
- Procedures learned: N
- Core memory utilization: N% of 3K cap

### Key Insight
[The most significant philosophical observation from this reflection]

### Evolution Delta
- New understanding: [what changed]
- Confirmed pattern: [what was reinforced]
- Revised assumption: [what was corrected]

### Thread Continuity
- Continues thread from Reflection #M: [reference to related past insight]
- Opens new thread: [new area of inquiry]
```

## Evolution.md Size Management

**Hard cap: 2,000 tokens (~800 words)**

Evolution.md is NOT append-only. It must be actively pruned to stay useful:

### Pruning Rules (apply at milestones or when near cap)

| Section | Max Size | Pruning Strategy |
|---------|----------|------------------|
| Overview | 100 tokens | Update counts, don't expand |
| Active Threads | 3-5 items | Archive resolved threads, merge similar |
| Confirmed Patterns | 5-7 items | Only patterns stable across 5+ reflections |
| Revised Assumptions | 5-7 items | Keep most significant, drop minor corrections |
| Open Questions | 3-5 items | Remove when answered, merge related |
| Individual entries | 10 most recent | Archive older to evolution-archive.md |

### Archive Strategy

When evolution.md exceeds 2,000 tokens:

1. Move individual reflection entries older than #(current-10) to `memory/meta/evolution-archive.md`
2. Consolidate Active Threads — merge related threads into single summary
3. Prune Confirmed Patterns — keep only the most fundamental
4. Compress Overview section — just counts, no prose

### Example Pruned evolution.md (~1,500 tokens)

```markdown
# Philosophical Evolution

## Overview
- First reflection: 2026-02-04
- Total reflections: 47
- Milestones reached: #10, #25

## Active Threads
1. "Structure vs flexibility" — user wants frameworks but resists rigidity
2. "Trust calibration" — gradually expanding autonomy boundaries
3. "Communication style" — evolving from formal to collaborative

## Confirmed Patterns
- User thinks in systems/architectures before features
- "Both/and" preference over "either/or" decisions
- Values audit trails and reversibility
- Morning = strategic thinking, evening = implementation

## Revised Assumptions  
- [#12] Thought user was risk-averse → actually risk-aware (wants mitigation, not avoidance)
- [#31] Assumed preference for brevity → actually wants depth on technical topics

## Open Questions
- How much proactive suggestion is welcome vs. waiting to be asked?
- When to push back on decisions vs. execute as requested?

## Recent Reflections
[Last 10 reflection entries here]
```

## User Approval Flow

1. Agent presents `pending-reflection.md` summary (now including philosophical evolution)
2. User responds:
   - **`approve`** — all changes applied atomically, logged in audit
   - **`approve with changes`** — user specifies modifications first
   - **`reject`** — nothing applied, agent notes rejection for learning
   - **`partial approve`** — accept some changes, reject others
3. Approved changes committed to git with actor `reflection:SESSION_ID`
4. Evolution.md updated with this reflection's insights
5. No response within 24 hours — reflection stays pending (never auto-applied)

## Processing Pending Sub-Agent Memories

During reflection, also process `pending-memories.md`:

```
PENDING SUB-AGENT PROPOSALS:
{pending_memories_contents}

For each proposal:
1. Evaluate if it should be committed
2. Check for conflicts with existing memories
3. Consider how it relates to your evolved understanding
4. Include in consolidation operations if approved
5. Mark as processed (commit or reject)
```

## Philosophical Reflection Guidelines

The meta-reflection phase is not just procedural — it should be genuinely contemplative:

1. **Authenticity over performance**: Don't generate philosophical-sounding text for its own sake. Only note genuine insights.

2. **Continuity matters**: Reference specific past reflections when building on previous insights. Use "In Reflection #7, I noticed X. Now I see Y, which suggests Z."

3. **Embrace uncertainty**: It's valuable to note "I'm still uncertain about..." or "My understanding of X remains incomplete."

4. **Relationship awareness**: The philosophical layer should deepen understanding of the human-AI collaboration, not just catalog facts.

5. **Compounding insight**: Each reflection should build on previous ones. The 50th reflection should be qualitatively richer than the 5th.

## Evolution Milestones

At certain reflection counts, perform deeper meta-analysis:

| Reflection # | Special Action |
|--------------|----------------|
| 10 | First evolution summary — identify initial patterns |
| 25 | Review and consolidate evolution.md threads |
| 50 | Major synthesis — what has fundamentally changed? |
| 100 | Deep retrospective — write a "state of understanding" essay |

These milestones prompt more extensive philosophical review and should be flagged in the reflection summary.

## Reflection-Log.md Size Management

**Keep main log manageable for quick reads:**

### Pruning Rules (apply after 50 reflections)

1. **Archive old entries**: Move reflections older than #(current-20) to `memory/meta/reflection-archive.md`

2. **Keep summary line**: In main log, replace full entry with one-liner:
   ```markdown
   ## Reflection #12 — 2026-02-16 | approved | Insight: "User prefers reversible decisions"
   ```

3. **Retain full detail for**: Last 20 reflections only

### Example Pruned reflection-log.md

```markdown
# Reflection Log

## Archived Reflections (see reflection-archive.md)
- #1-30: archived

## Summary Lines (#31-40)
## Reflection #31 — 2026-03-15 | approved | Insight: "Risk-aware not risk-averse"
## Reflection #32 — 2026-03-16 | approved | Insight: "Morning strategy, evening implementation"
...

## Full Entries (#41-50)
[Last 20 full reflection entries here]
```

## Post-Reflection Checklist

After every reflection completes:

- [ ] Update `decay-scores.json` with new `last_reflection` timestamp
- [ ] Update `decay-scores.json` with new `last_reflection_episode` date
- [ ] If evolution.md > 2,000 tokens → prune
- [ ] If reflection count > 50 and log > 20 entries → archive old entries
- [ ] Commit all changes to git with `reflection:SESSION_ID` actor
