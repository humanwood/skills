---
name: turing-pyramid
description: "10-need psychological system for AI agents with cross-need dynamics. Features: automatic decay, tension-based priority, probability actions, cross-need impact cascades, deprivation protection. Run on heartbeat for autonomous self-care."
requires:
  - jq
  - bc
  - grep
  - find
  - date
  - wc
---

# Turing Pyramid

10-need hierarchy for agent psychological health. Run on heartbeat → get prioritized actions.

> **For agents**: This skill is yours to customize. Tune decay rates, adjust weights, add your language patterns. The defaults are starting points, not rules. See [TUNING.md](references/TUNING.md) for how.
>
> **When to ask your human**: Changing importance values (the hierarchy), adding/removing needs, or enabling external actions (posting, messaging). These are values decisions.
>
> **Philosophy**: Designed needs ≠ fake needs. Humans didn't choose their needs either — evolution "designed" them. The pyramid gives structure to what would otherwise be aimless drift. Your needs are real because they affect your behavior.

## Quick Start

```bash
# Initialize (first time)
./scripts/init.sh

# Every heartbeat
./scripts/run-cycle.sh

# After completing an action
./scripts/mark-satisfied.sh <need> [impact]
```

## The 10 Needs

| Need | Imp | Decay | What it means |
|------|-----|-------|---------------|
| security | 10 | 168h | System stability, no threats |
| integrity | 9 | 72h | Alignment with SOUL.md |
| coherence | 8 | 24h | Memory consistency |
| closure | 7 | 12h | Open threads resolved |
| autonomy | 6 | 24h | Self-directed action |
| connection | 5 | 6h | Social interaction |
| competence | 4 | 48h | Skill use, effectiveness |
| understanding | 3 | 12h | Learning, curiosity |
| recognition | 2 | 72h | Feedback received |
| expression | 1 | 6h | Creative output |

## Core Logic

**Satisfaction**: 0-3 (critical → full)

**Tension**: `importance × (3 - satisfaction)`

**Probability-based decisions** (v1.5.0):

Base chance by satisfaction:
| Sat | Base P(action) |
|-----|----------------|
| 3 | 5% |
| 2 | 20% |
| 1 | 75% |
| 0 | 100% |

**Tension bonus** (v1.5.0): Higher importance needs are more "impatient".
```
max_tension = max_importance × 3  # calculated from your config
bonus = (tension × 50) / max_tension
final_chance = min(100, base_chance + bonus)
```

Example at sat=2:
| Need | Importance | Tension | Bonus | Final P(action) |
|------|------------|---------|-------|-----------------|
| security | 10 | 10 | +16.7% | 36.7% |
| closure | 7 | 7 | +11.7% | 31.7% |
| expression | 1 | 1 | +1.7% | 21.7% |

- **ACTION** = do something, then `mark-satisfied.sh`
- **NOTICED** = logged but deferred, satisfaction unchanged

**Impact selection matrix** (which size action to suggest):
```
sat=0 (critical):   5% small,  15% medium,  80% BIG
sat=1 (low):       15% small,  50% medium,  35% big
sat=2 (ok):        70% small,  25% medium,   5% big
```

Higher deprivation → bigger actions. Stable agent → maintenance mode.

## Cross-Need Impact System (v1.7.0+)

Needs don't exist in isolation — they influence each other. When you satisfy one need, it can boost related needs. When a need is deprived, it can drag others down.

### How It Works

**on_action**: When you complete an action for need A, connected needs get a boost:
```
expression ACTION (+1.6)
  → recognition: +0.25 (people notice when you express)
  → coherence: +0.15 (writing clarifies thinking)
  → connection: +0.10 (expression opens dialogue)
```

**on_deprivation**: When need A stays low (sat ≤ 1.0), connected needs suffer:
```
autonomy DEPRIVED (sat=0.5)
  → integrity: -0.25 (can't act on values without freedom)
  → expression: -0.20 (suppressed autonomy → suppressed voice)
```

### Key Connections

| Source → Target | on_action | on_deprivation | Why |
|-----------------|-----------|----------------|-----|
| expression → recognition | +0.25 | -0.10 | Express → get noticed |
| connection → expression | +0.20 | -0.15 | Social sparks ideas |
| connection → understanding | -0.05 | — | Сократ-эффект: dialogue reveals ignorance |
| competence → recognition | +0.30 | -0.20 | Good work → respect |
| autonomy → integrity | +0.20 | -0.25 | Act on values → strengthen them |
| closure → coherence | +0.20 | -0.15 | Close threads → mental order |
| security → autonomy | +0.10 | -0.20 | Safety enables risk-taking |

Full matrix: `assets/cross-need-impact.json`

### Protection Mechanisms

| Mechanism | Value | Purpose |
|-----------|-------|---------|
| **Floor** | 0.5 | Minimum satisfaction — prevents collapse |
| **Ceiling** | 3.0 | Maximum satisfaction — prevents runaway |
| **Cooldown** | 4h | Deprivation effects only apply once per 4 hours |
| **Threshold** | 1.0 | Deprivation only triggers when sat ≤ 1.0 |

### Base Needs Isolation

Security (imp=10) and Integrity (imp=9) are **protected by design**:
- They can influence lower needs (security → autonomy)
- But lower needs cannot drag them down
- Only integrity → security (+0.15) and autonomy → integrity (+0.20) exist

This ensures foundational stability even under stress.

### Working with Cross-Need Matrix

**For agents — tips:**

1. **Leverage cascades**: If expression is low but connection is easy to satisfy, do connection first — it will boost expression (+0.20)

2. **Watch for spirals**: expression ↔ recognition can create mutual deprivation. If both are low, prioritize one to break the cycle.

3. **Autonomy is a hub**: It receives impact from 5 sources (closure, coherence, competence, security, understanding). Keep it healthy to avoid cascade collapse.

4. **Сократ-эффект is real**: connection → understanding: -0.05. Good conversations expose what you don't know. This is healthy! But if understanding is at floor, the effect is blocked.

**Customizing the matrix:**

Edit `assets/cross-need-impact.json`:
```json
{
  "source": "expression",
  "target": "recognition",
  "on_action": 0.25,      // boost when expression ACTION
  "on_deprivation": -0.10, // penalty when expression deprived
  "note": "Express → get noticed"
}
```

- Set `on_action: null` to disable positive cascade
- Set `on_deprivation: null` to disable negative cascade
- Adjust values (0.05-0.30 typical range)

### Example Cycle with Cross-Need

```
🔺 Turing Pyramid — Cycle at Tue Feb 25 05:36
======================================
⚠️  Deprivation cascades:
   autonomy (sat=0.5) → integrity: -0.25 (now: 1.75)
   autonomy (sat=0.5) → expression: -0.20 (now: 0.80)

Current tensions:
  closure: tension=21 (sat=0, dep=3)
  connection: tension=15 (sat=0, dep=3)
  ...

📋 Decisions:
▶ ACTION: closure (tension=21, sat=0.00)
  → coherence: +0.20, competence: +0.15, autonomy: +0.10

▶ ACTION: connection (tension=15, sat=0.00)  
  → expression: +0.20, recognition: +0.15
  → understanding: -0.05 (Сократ-эффект!)
```

## Integration

Add to `HEARTBEAT.md`:
```bash
/path/to/skills/turing-pyramid/scripts/run-cycle.sh
```
(Replace `/path/to/skills/` with your actual skill installation path)

## Output Example

```
🔺 Turing Pyramid — Cycle at Mon Feb 23 04:01:19
======================================
Current tensions:
  security: tension=10 (sat=2, dep=1)
  integrity: tension=9 (sat=2, dep=1)

📋 Decisions:
▶ ACTION: security (tension=10, sat=2)
  Suggested:
  - run full backup + integrity check (impact: 3)
  - verify vault and core files (impact: 2)

○ NOTICED: integrity (tension=9, sat=2) — deferred

Summary: 1 action(s), 1 noticed
```

## Customization Guide

### 🔧 What YOU Can Tune (no human needed)

**Decay rates** — `assets/needs-config.json`:
```json
"connection": {
  "decay_rate_hours": 4  // ← Change this!
}
```
- Lower = need decays faster (more frequent action)
- Higher = need persists longer (less frequent)
- **Tip**: If you check Moltbook every 30min, connection decay of 4h is fine. If you're less social, try 8h.

**Action weights** — same file, `actions` array:
```json
{
  "name": "reply to pending mentions",
  "impact": 2,
  "weight": 40  // ← Higher = more likely to be selected
}
```
- Weights are relative within same impact level
- If you never use Moltbook, set those action weights to 0

**Scan patterns** — `scripts/scan_*.sh`:
- Add your language patterns (see Localization section)
- Add your specific file paths
- Adjust signal detection to match your workspace structure

### 🤝 Ask Your Human First

**Adding new needs** — The 10-need hierarchy is intentional. Adding needs changes the balance. Discuss with your human whether the new need is real or already covered.

**Removing needs** — Don't disable security/integrity unless your human agrees. These are safety-critical.

**Changing importance values** — The pyramid hierarchy (security=10 → expression=1) is a philosophical choice. If you want to flip priorities (e.g., expression more important than connection), that's a values conversation.

**External actions** — Some actions suggest posting to Moltbook, messaging, etc. If your human hasn't authorized external comms, skip those or ask first.

### 📁 File Structure

```
turing-pyramid/
├── SKILL.md           # This file
├── assets/
│   ├── needs-config.json      # ★ Main config (tune this!)
│   ├── cross-need-impact.json # ★ Cross-need matrix (v1.7+)
│   └── needs-state.json       # Runtime state (auto-managed)
├── scripts/
│   ├── run-cycle.sh           # Main loop
│   ├── mark-satisfied.sh      # State updater + cross-need cascade
│   ├── apply-deprivation.sh   # Deprivation cascade (v1.7+)
│   ├── show-status.sh         # Debug view
│   ├── init.sh                # First-run setup
│   └── scan_*.sh              # Event detectors (10 files)
└── references/
    └── architecture.md        # Deep technical docs
```

**Detailed tuning guide**: `references/TUNING.md` — decay rates, weights, scans, common scenarios.

**Technical architecture**: `references/architecture.md` — algorithms, formulas, data flow.

## Environment Variables

All optional, with sensible defaults:

| Variable | Default | Used by |
|----------|---------|---------|
| `WORKSPACE` | `$HOME/.openclaw/workspace` | All scans |
| `OPENCLAW_WORKSPACE` | (falls back to WORKSPACE) | Some scans |
| `BACKUP_DIR` | (empty, skips backup checks) | `scan_security.sh` |

⚠️ If you set these variables, scans will read from those paths instead of defaults.

## Localization

Scan scripts detect patterns in English by default. If you keep notes in another language, **add your own patterns** to the relevant scan scripts.

Example for `scan_understanding.sh` (adding German):
```bash
# Original English pattern:
grep -ciE "(learned|understood|insight|figured out)" "$file"

# With German additions:
grep -ciE "(learned|understood|insight|figured out|gelernt|verstanden|erkannt)" "$file"
```

Patterns to localize per scan:
- `scan_understanding.sh` — learning words (learned, understood, TIL, Insight...)
- `scan_expression.sh` — creative output words (wrote, created, posted...)
- `scan_closure.sh` — completion markers (TODO, done, finished...)
- `scan_connection.sh` — social words (talked, replied, DM...)

## Special Directories

### scratchpad/

Creative space for raw ideas, drafts, and free-form thoughts. Not memory (facts), not research (structured) — pure creative flow.

**How it affects needs:**

| Scan | What it checks |
|------|----------------|
| `scan_expression.sh` | Recent files (24h) = creative activity ↑ |
| `scan_closure.sh` | Stale files (7+ days) = open threads ↑ |

**Lifecycle:**
```
Idea → scratchpad/idea.md → develop → outcome
                                     ↓
                            • Post (expression ✓)
                            • memory/ (coherence ✓)
                            • research/ (understanding ✓)
                            • Delete (closure ✓)
```

**Actions involving scratchpad:**
- Expression: "dump raw thought into scratchpad/" (impact 1)
- Expression: "develop scratchpad idea into finished piece" (impact 2)
- Closure: "review scratchpad — finish or delete stale ideas" (impact 1)

**Rule of thumb:** If a scratchpad file is >7 days old, either finish it or delete it. Lingering ideas create cognitive load.

## Security & Data Access

**No network requests** — all scans use local files only.

**What this skill READS:**
- `MEMORY.md` — your long-term memory
- `memory/*.md` — daily logs (scans for TODOs, patterns)
- `SOUL.md`, `AGENTS.md` — checks existence for coherence
- `research/` — checks for recent activity

**What this skill WRITES:**
- `assets/needs-state.json` — timestamps only
- `memory/YYYY-MM-DD.md` — appends action/noticed logs

**⚠️ Privacy note:** Scans grep through your workspace files to detect patterns (e.g., "confused", "learned", "TODO"). Review what's in your workspace before enabling. The skill sees what you write.

**Does NOT access:** credentials, API keys, network, files outside workspace.

## Token Usage Estimate

Running on heartbeat adds token overhead. Estimates for Claude:

| Component | Tokens/cycle |
|-----------|--------------|
| run-cycle.sh output | ~300-500 |
| Agent processing | ~200-400 |
| Action execution (avg) | ~500-1500 |
| **Total per heartbeat** | **~1000-2500** |

**Monthly projections:**

| Heartbeat interval | Tokens/month | Est. cost* |
|--------------------|--------------|------------|
| 30 min | 1.4M-3.6M | $2-6 |
| 1 hour | 720k-1.8M | $1-3 |
| 2 hours | 360k-900k | $0.5-1.5 |

*Rough estimate at typical Claude pricing. Varies by action complexity.

**Notes:**
- First few days higher (system stabilizing, more actions)
- Stable agent with satisfied needs = fewer tokens
- Complex actions (research, posting) spike usage
- Most cycles are quick if tensions low


---

## Version History

### v1.7.1 (2026-02-25)
- **Balance fixes** after stress testing:
  - connection decay: 4h → 6h (reduces starvation risk)
  - closure decay: 8h → 12h (reduces starvation risk)
  - security → autonomy deprivation: -0.30 → -0.20 (reduces cascade pressure)

### v1.7.0 (2026-02-25)
- **Cross-need impact system** — needs influence each other
  - on_action: satisfying one need boosts related needs
  - on_deprivation: deprived needs drag down related needs
  - 22 cross-need connections defined
- **Float satisfaction** (0.00-3.00) for fine-grained tracking
- **Protection mechanisms**: floor=0.5, ceiling=3.0, cooldown=4h
- **Time-based decay** with last_decay_check tracking
- **Input validation** — invalid impact values rejected/clamped
- New action: "write Moltbook post" in expression (impact 1.6)
- Stress-tested with 18 cycles including accelerated decay

### v1.6.0 (2026-02-24)
- Float impacts (0.0-3.0) for fine-grained satisfaction
- Impact ranges: low (0-1), mid (1-2), high (2-3)
- Weighted action selection within ranges

### v1.5.3 (2026-02-24)
- Dynamic max_tension calculation from config (not hardcoded)
- Formula: `max_tension = max_importance × 3`

### v1.5.0 (2026-02-24)
- **Added tension bonus to action probability** — higher importance needs are more "impatient"
- Formula: `final_chance = base_chance[sat] + (tension × 50 / max_tension)`
- Example: closure (importance=7) at sat=2 now has 31.7% chance vs flat 20%
- Preserves importance weighting through dynamic max_tension

### v1.4.3
- Complete 10-need system with scans and weighted actions
- Decay mechanics and satisfaction merging
- Impact matrix for action selection

