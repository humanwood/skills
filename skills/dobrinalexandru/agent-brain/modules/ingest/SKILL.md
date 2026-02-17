# Ingest Memory 📥

**Status:** ✅ Live | **Module:** ingest | **Part of:** Agent Brain

External knowledge ingestion. Reads, processes, and stores knowledge from URLs, articles, essays, and documents.

## What It Does

- **Fetch**: Get content from URLs
- **Extract**: Parse key knowledge from content
- **Store**: Save in usable format for retrieval
- **Link**: Connect to existing knowledge

## Use Cases

### Reading Essays
```
"Read https://paulgraham.com/ammers.html"
"Ingest this article: [URL]"
"Learn from this: [URL]"
```

### Processing Documents
```
"Process this PDF"
"Extract knowledge from [URL]"
"Index this page"
```

### Building Knowledge Base
```
"What do you know about X?"
"Summarize what you ingested from Y"
"Link these concepts"

## Processing Pipeline

```
1. Fetch URL / Content
2. Extract:
   - Key concepts
   - Main ideas
   - Supporting arguments
   - Facts / Data
   - Source metadata
3. Store in Archive
4. Link to existing knowledge
5. Make retrievable
```

## Extraction Format

```json
{
  "source": "https://paulgham.com/article.html",
  "title": "Article Title",
  "author": "Paul Graham",
  "date": "2026-01",
  "concepts": ["startup", "ideas", "execution"],
  "key_points": [
    "Point 1",
    "Point 2"
  ],
  "facts": ["Fact A", "Fact B"],
  "linked_concepts": ["existing concept"],
  "raw_summary": "..."
}
```

## Integration

Works with:
- **Archive** → stores processed knowledge
- **Signal** → validates new information
- **Gauge** → confidence in extraction

## Usage

```
"Ingest: [URL]"
"Learn from: [URL]"
"Read this: [URL]"
"What did you learn from [source]?"
"What do you know about [topic]?"
```

## Sources Supported

- Articles / Blog posts
- Essays (Paul Graham, etc.)
- Documentation
- Research papers
- News posts
- PDFs (text content)

## Memory

Stores ingested knowledge:
```json
{
  "sources": [],
  "concepts": {},
  "extracted_knowledge": []
}
```

## Continuous Learning

- Mark sources for re-checking
- Update on new content
- Link related concepts
- Build interconnected knowledge graph
