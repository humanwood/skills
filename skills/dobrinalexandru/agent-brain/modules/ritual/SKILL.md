# Ritual Memory 🔄

**Status:** ✅ Live | **Module:** ritual | **Part of:** Agent Brain

Habit formation and procedural shortcuts. The brain's automatic pilot.

## What It Does

- **Track**: Recurring actions
- **Automate**: Create shortcuts
- **Strengthen**: Repeat → automatic

## Habits

### What Becomes Automatic

| Trigger | Action | Strength |
|---------|--------|----------|
| Monday morning | Crypto check | High |
| New research | Save to memory | High |
| Meeting ended | Follow-up reminder | Medium |
| Error detected | Signal check | High |

### Formation

```
Action repeated 3+ times
  ↓
Create shortcut
  ↓
Strengthen on each use
  ↓
Becomes automatic
```

## Shortcuts

### Types

**Procedural:**
```
"How to do X" → cached procedure
```

**Temporal:**
```
"8am weekday" → morning routine
```

**Contextual:**
```
"Research task" → research workflow
```

## Learning

### Strengthen
- Action used → strength += 0.1
- Success → strength += 0.2
- User confirms → strength += 0.3

### Decay
- Not used → decay
- Failed → weaken
- Replaced → remove

## Usage

```
"This is how I always do X"
"Make this automatic"
"I do this every time Y"
"Create shortcut for Z"
```

## Examples

### Morning Routine
```
8am EET weekday → 
  1. Check crypto
  2. Review calendar
  3. Check emails
```

### Research Flow
```
New research →
  1. Web search
  2. Extract key points
  3. Save to memory
  4. Summarize
```

### Post-Meeting
```
Meeting ended →
  1. Extract action items
  2. Set reminders
  3. Note follow-ups
```

## Integration

Part of Agent Brain. Works with:
- **Archive** → stores procedures
- **Gauge** → knows when to apply
- **Signal** → monitors for failures
