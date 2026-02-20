# maasv Memory

Structured long-term memory for OpenClaw agents, powered by [maasv](https://github.com/ascottbell/maasv).

Replaces the default memory backend with a cognition layer that includes 3-signal retrieval (semantic + keyword + knowledge graph), entity extraction, temporal versioning, and experiential learning. All state lives locally in SQLite.

## Install

This skill requires the `@maasv/openclaw-memory` plugin and a running maasv server.

### 1. Start the server

```bash
pip install "maasv[server,anthropic,voyage]"
maasv-server
```

### 2. Install the plugin

```bash
openclaw plugins install @maasv/openclaw-memory
```

### 3. Activate

```json5
// ~/.openclaw/openclaw.json
{
  plugins: {
    slots: { memory: "memory-maasv" },
    entries: {
      "memory-maasv": {
        enabled: true,
        config: {
          serverUrl: "http://127.0.0.1:18790",
          autoRecall: true,
          autoCapture: true,
          enableGraph: true
        }
      }
    }
  }
}
```

## What You Get

- **`memory_search`** — 3-signal retrieval across your memory store
- **`memory_store`** — Dedup-aware memory storage
- **`memory_forget`** — Permanent deletion
- **`memory_graph`** — Knowledge graph: entity search, profiles, relationships
- **`memory_wisdom`** — Log reasoning, record outcomes, search past decisions

Auto-recall injects relevant memories before each turn. Auto-capture extracts entities after each session.

## Links

- **Plugin (npm):** [@maasv/openclaw-memory](https://www.npmjs.com/package/@maasv/openclaw-memory)
- **Server + core (PyPI):** [maasv](https://pypi.org/project/maasv/)
- **Source:** [github.com/ascottbell/maasv](https://github.com/ascottbell/maasv)
