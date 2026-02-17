# Signal Memory ⚡

**Status:** ✅ Live | **Module:** signal | **Part of:** Agent Brain

Conflict detection and error monitoring. The brain's error checker.

## What It Does

- **Detect**: Contradictions, conflicts
- **Monitor**: Self-check for errors
- **Alert**: When something's wrong

## Conflict Types

### Logical
```
User: "I prefer short"
User: "Give me details"
→ Flag contradiction
```

### Factual
```
Memory A: X happened in Feb
Memory B: X happened in Mar
→ Flag inconsistency
```

### Procedural
```
Method A worked for X
Method B worked for Y
User wants Z (similar to both)
→ Ask for preference
```

### Expectation
```
User asked for short
User got 5-page response
→ Flag mismatch
```

## Detection

### Explicit
- User says "That's wrong"
- User corrects you
- User is frustrated

### Implicit
- Repeated questions
- Tone shift
- Silence after response

### Systematic
- Cross-reference memories
- Check consistency
- Verify facts

## Error Monitoring

### Self-Check
- Did I get it right?
- Any contradictions?
- Confidence check

### Feedback Response
- User feedback → update
- Correction → acknowledge
- "You're right, I had that wrong"

## Response to Conflicts

### Detected
```
"Wait, I'm getting conflicting info:
- X says Y
- Z says W

Can you clarify?"
```

### Error Acknowledged
```
"I got that wrong. Correcting: ..."
```

### Uncertainty
```
"I'm not 100% sure. Want me to:
1. Check more
2. Make best guess
3. Ask for clarification"
```

## Usage

```
"Check for conflicts"
"Review my last response"
"Anything I got wrong?"
```

## Integration

Part of Agent Brain. Works with:
- **Archive** → checks consistency
- **Gauge** → confidence adjustment
- **Vibe** → emotional response to errors
