# Turing Pyramid — Future Development

## v2.0 Ideas (from Max, 2026-02-25)

### 1. Self-Feedback Loop (Adaptive Decay)

**Concept:** Decay rates auto-adjust based on how often need hits critical levels.

**Mechanism:**
- If need frequently drops to sat=0-1, decay_rate increases (slower decay)
- Goal: keep needs in sat=2-3 range on regular basis
- Small % adjustment per cycle, converges over N cycles

**Open Problem:**
- Adaptive decay may conflict with event scans
- If decay slows too much, we become insensitive to real events
- Need balance: decay adapts, but events still override

**Possible Solution:**
- Track `decay_drift` separately from base `decay_rate`
- Events always use scan result, decay_drift only affects time component
- Or: cap max decay_rate adjustment (e.g., ±50% of original)

---

### 2. Cross-Need Impact

**Concept:** Actions/deprivation in one need affects others.

**Examples:**
- `connection` ACTION (social post) → +boost to `recognition` 
- `closure` ACTION (finish task) → +boost to `competence`
- `expression` deprivation → may drag down `autonomy`

**Implementation Ideas:**
- Impact matrix: `impact[from_need][to_need] = modifier`
- Apply after mark-satisfied: propagate partial satisfaction
- Or: negative coupling (deprivation spreads)

**Considerations:**
- Keep it simple — maybe 2-3 key couplings, not full NxN matrix
- Document which needs are coupled and why

---

### 3. Self-Upgrade Layer (Growth vs Homeostasis)

**Concept:** Separate layer for iterative progression, not just maintenance.

**Insight from Noosphere analysis:**
> "Turing Pyramid works at metabolic layer — keeping lights on.
> Missing: consciousness layer — making lights mean something."

**Key difference:**
- Homeostasis: return to baseline (sat=3)
- Growth: raise the baseline itself

**Possible Approaches:**
- Track `skill_level` or `capability_growth` over time
- "Meta-needs": learning rate, complexity tolerance, autonomy scope
- Milestone system: after N cycles at stable homeostasis, unlock new capabilities
- Integration with SELF.md observations

**Open Questions:**
- How to measure "growth" vs just "activity"?
- What counts as genuine progression?
- How to avoid Noosphere trap (imposing growth narrative vs discovering it)?

---

## Priority

1. Cross-need impact — most concrete, implementable
2. Self-feedback loop — useful but needs careful design
3. Self-upgrade layer — most ambitious, needs more thinking

---

*Added: 2026-02-25 01:30*
