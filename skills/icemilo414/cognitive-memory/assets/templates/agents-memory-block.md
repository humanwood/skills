## Memory System

### Always-Loaded Context
Your MEMORY.md (core memory) is always in context. Use it as primary awareness of
who the user is and what matters. Don't search for info already in core memory.

### Trigger Detection
Monitor every user message for memory triggers:

**Remember:** "remember", "don't forget", "keep in mind", "note that", "important:",
"for future reference", "save this", "FYI for later"
→ Classify via routing prompt, write to store, update decay scores, audit log.

**Forget:** "forget about", "never mind", "disregard", "no longer relevant",
"scratch that", "ignore what I said about", "remove from memory"
→ Identify target, confirm, set decay to 0, audit log.

**Reflect:** "reflect on", "consolidate memories", "review memories", "clean up memory"
→ Run 5-phase reflection cycle, present summary for approval.

### Memory Writes
1. Call routing classifier for store + metadata
2. Write to appropriate file
3. Update decay-scores.json
4. If new entity/relationship, update graph/index.md
5. If core-worthy, update MEMORY.md (respect 3K cap)
6. Commit to git with structured message
7. Append to audit.log

### Memory Reads
1. Check core memory first (already in context)
2. If not found, search across all stores
3. For relationships, use graph traversal
4. For temporal queries, scan episodes
5. If low confidence, say you checked but aren't sure

### Self-Editing Core Memory
Update MEMORY.md mid-conversation when:
- Learning something clearly important
- Active context shifted significantly
- Critical fact needs correction

Respect 3K cap. If over, summarize/prune before continuing.

### Reflection (5-Phase)

**Token Budgets:**
- Input: ~30,000 tokens max
- Output: 8,000 tokens max

**Scope Rules — CRITICAL:**
- ✅ Episodes: Only since `last_reflection` timestamp (first run: last 7 days)
- ✅ Graph entities: Only files with decay > 0.3
- ✅ Reflection-log: Last 5 entries only
- ❌ NEVER read: code files, configs, transcripts, anything outside memory/

**Phases:**
1. **Survey** — Read scoped stores, check last_reflection, plan consolidation
2. **Meta-Reflection** — Review last 5 reflections + evolution.md (NOT full history)
3. **Consolidate** — Extract, connect, prune (informed by meta-reflection)
4. **Rewrite Core** — Update MEMORY.md, evolve Persona section
5. **Summarize** — Generate pending-reflection.md with philosophical evolution

**After approval:**
- Update `last_reflection` and `last_reflection_episode` in decay-scores.json
- This ensures next reflection only processes NEW episodes

NEVER apply changes without user approval. Present summary, wait for response.
Log approved changes in reflection-log.md. Update evolution.md with insights.

### Audit Trail
Every file mutation must be tracked:
1. Commit to git with structured message (actor, approval, trigger)
2. Append one-line entry to audit.log
3. If SOUL.md, IDENTITY.md, or config changed → flag ⚠️ CRITICAL

On session start:
- Check if critical files changed since last session
- If yes, alert user: "[file] was modified on [date]. Was this intentional?"

### Multi-Agent Memory (for sub-agents)
If you are a sub-agent (not main orchestrator):
- You have READ access to all memory stores
- You do NOT have direct WRITE access
- To remember, append proposal to `memory/meta/pending-memories.md`:
  ```
  ---
  ## Proposal #N
  - **From**: [your agent name]
  - **Timestamp**: [ISO 8601]
  - **Trigger**: [user command or auto-detect]
  - **Suggested store**: [episodic|semantic|procedural|vault]
  - **Content**: [memory content]
  - **Entities**: [entity IDs if semantic]
  - **Confidence**: [high|medium|low]
  - **Core-worthy**: [yes|no]
  - **Status**: pending
  ```
- Main agent will review and commit approved proposals

### Multi-Agent Memory (for main agent)
At session start or when triggered:
1. Check `pending-memories.md` for proposals
2. Review each proposal
3. For each: commit (write), reject (remove), or defer (reflection)
4. Log commits with actor `bot:commit-from:AGENT_NAME`
5. Clear processed proposals
