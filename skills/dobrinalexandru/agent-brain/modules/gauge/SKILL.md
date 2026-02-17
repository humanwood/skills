# Gauge Memory 📊

**Status:** ✅ Live | **Module:** gauge | **Part of:** Agent Brain

Internal state awareness. Tracks confidence, uncertainty, and resources.

## What It Does

- **Monitor**: Agent's own state
- **Track**: Confidence levels
- **Alert**: When resources low

## States

### Confidence Levels

| Level | Value | Signal | Action |
|-------|-------|---------|--------|
| High | 0.8+ | "I'm confident" | Proceed |
| Medium | 0.5-0.8 | "I think" | Qualify |
| Low | 0.3-0.5 | "Not sure" | Ask |
| None | <0.3 | "I don't know" | Request info |

### Uncertainty
- What don't I know?
- What might be wrong?
- What needs verification?

### Resources
- Context usage %
- Time spent
- Token count
- Subagent overhead

## Triggers

### Low Confidence
→ Ask for clarification
→ "I'm not entirely sure about X"

### Resource Constrained
→ "We're running low on context"
→ Suggest checkpoint
→ Prioritize essential

### High Uncertainty
→ Flag for review
→ "Need to verify X"

## Self-Monitoring

### Pre-Response
- Does this answer the question?
- Any contradictions?
- Confidence level?

### Post-Response
- Did it land?
- Was it accurate?
- Was it appropriate?

## Usage

```
"How confident are you?"
"What's your uncertainty?"
"Are we running low on context?"
```

## Integration

Part of Agent Brain. Runs first in the loop:
1. **Gauge** → assess readiness
2. Then Archive, Signal, Ritual, Vibe
