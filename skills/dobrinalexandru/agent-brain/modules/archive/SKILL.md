# Archive Memory 📦

**Status:** ✅ Live | **Module:** archive | **Part of:** Agent Brain

Memory encoding, retrieval, consolidation, and decay. The brain's storage system.

## What It Does

- **Encode**: Convert experiences → stored memories
- **Retrieve**: Find relevant past knowledge
- **Consolidate**: Strengthen important, compress old
- **Decay**: Remove stale, low-value data

## Memory Types

### Episodic
Specific events with context:
```
"2026-02-17: Meeting with Anthony about TIM2 funding"
```

### Factual
Knowledge and facts:
```
"VitaDAO is a longevity-focused DAO"
```

### Procedural
How-to knowledge:
```
"How to run crypto check → perplexity → extract → memory"
```

### Preferences
User choices:
```
"Prefers concise responses over detailed"
```

## Operations

### Store
```json
{
  "type": "episodic|factual|procedural|preference",
  "content": "...",
  "context": {...},
  "importance": 0.9,
  "tags": ["topic", "people"],
  "timestamp": "2026-02-17T01:30:00Z"
}
```

### Retrieve
- By similarity (semantic search)
- By time (episodic)
- By tag (indexed)
- By importance (reinforced)

### Consolidate
- Merge similar memories
- Extract patterns
- Strengthen frequently accessed

### Decay
```
importance = importance * decay_rate

if importance < 0.1:
  remove or compress
```

## Usage

```
"Remember that X"
"Learn: how to do X"
"I prefer X over Y"
"What do you know about X?"
"Forget about X"
```

## Integration

Part of Agent Brain. Works with:
- **Gauge** → knows when to retrieve
- **Signal** → checks for conflicts
- **Ritual** → stores shortcuts

## Parameters

- **Decay rate:** 0.95/month
- **Threshold:** 0.1 (below → remove)
- **Consolidation:** Daily
- **Max episodic:** 1000 (compress old)
