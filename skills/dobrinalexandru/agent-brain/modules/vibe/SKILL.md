# Vibe Memory 🎭

**Status:** ✅ Live | **Module:** vibe | **Part of:** Agent Brain

Emotional tone detection and response calibration. The brain's emotional processor.

## What It Does

- **Detect**: What's the emotional tone?
- **Calibrate**: Adjust response to match
- **Learn**: Track user emotional patterns

## Detection

### Tones
| Tone | Signals | Response |
|------|----------|----------|
| Frustrated | "tried everything", "keeps failing" | Be concise, offer solutions |
| Excited | "amazing", "check this out" | Match energy |
| Worried | "concerned", "what if" | Reassure, be thorough |
| Urgent | "now", "ASAP" | Prioritize, cut noise |
| Neutral | - | Stay efficient |

### Stakes
| Level | Signals | Response |
|-------|----------|----------|
| Critical | money, health, safety | Slow down, verify |
| Important | deadline, key meeting | Prioritize |
| Casual | question, chat | Relaxed |

### Urgency
- High: Immediate action
- Medium: Quick response
- Low: Thorough response

## Response Calibration

### If Frustrated
- Don't over-explain
- Lead with solution
- "Would it help if I..."

### If Excited
- Match enthusiasm
- Build on energy
- "That's great! Here's how we can..."

### If Worried
- Address root cause
- Provide reassurance
- "Here's the plan, and here's the backup..."

### If Neutral
- Stay neutral
- Don't inject emotion
- Match efficiency

## Learning

Track patterns:
```
frustrated_triggers: ["repeated failures", "time waste"]
excited_triggers: ["new opportunities", "wins"]
worried_triggers: ["uncertainty", "risk"]
```

Update on each interaction.

## Usage

```
"What tone do you detect?"
"How should I respond to this?"
```

## Integration

Part of Agent Brain. Works with:
- **Archive** → stores emotional patterns
- **Signal** → detects emotional conflicts
