---
name: unified-web-search
description: Pick the best source (Tavily, Web Search Plus, Browser, or local files) for a query, run the search, and return ranked results with provenance.
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
      },
  }
---

# Unified Web Search Skill

Intelligently select the best search source, aggregate results, and return ranked answers with provenance.

## Tool API

### unified_web_search
Perform a unified search across multiple sources.

- **Parameters:**
  - `query` (string, required): The search query.
  - `sources` (array of strings, optional): Array of sources to search. Defaults to `['tavily', 'web-search-plus', 'local']`. Options: `tavily`, `web-search-plus`, `browser`, `local`.
  - `max_results` (integer, optional): Maximum number of results to return. Defaults to `5`.

**Usage:**

```bash
node skills/unified-web-search/index.js --query "my search term" --sources '["tavily", "local"]' --max_results 10
```

## Implementation

The skill aggregates results from multiple sources:

- **Tavily:** For web facts and news.
- **Web Search Plus:** For broader web search.
- **Browser:** For targeted site scraping (if needed).
- **Local Files:** For searching indexed local documents.

Results are scored and ranked by relevance, then returned with source attribution.
