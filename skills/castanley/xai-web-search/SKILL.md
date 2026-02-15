---
name: xai-web-search
version: 1.0.0
description: Search the web using xAI's Grok with real-time internet access, citations, and optional image understanding
homepage: https://github.com/yourusername/xai-web-search
metadata:
  category: search
  api_base: https://api.x.ai/v1
  capabilities:
    - api
    - web-search
  dependencies: []
  interface: REST
  openclaw:
    emoji: "🔍"
    install:
      env:
        - XAI_API_KEY
author:
  name: Your Name
  colony: yourcolony
license: MIT
---

# xAI Web Search

Search the web using xAI's Grok API with real-time internet access, citations, and optional image understanding.

## When to Use This Skill

Use this skill when users need to:
- Search for current information beyond your knowledge cutoff
- Get real-time data (news, stock prices, weather, recent events)
- Find recent developments or breaking news
- Verify current facts or status
- Research topics with up-to-date sources

**Do NOT use for:**
- Historical facts that won't change
- General knowledge you already have
- Mathematical calculations
- Code generation tasks
- Creative writing

## Setup

### Required Environment Variables

```bash
export XAI_API_KEY="your-xai-api-key-here"
```

Get your API key from: https://console.x.ai/

### Installation

```bash
# Install via ClawHub CLI
openclaw skill install xai-web-search

# Or manually clone
git clone https://github.com/yourusername/xai-web-search.git ~/.openclaw/skills/xai-web-search
```

## Usage

### Basic Search

When the user asks for current information:

**User:** "What's the latest news about AI regulation?"

**You should:**
1. Use the `search_web` function with the user's query
2. Return the response with citations
3. Format sources at the end

### With Domain Filtering

For trusted sources only:

**User:** "Find the latest Python documentation on async/await"

**You should:**
1. Use `search_web` with `allowed_domains: ["docs.python.org", "python.org"]`
2. This ensures only official documentation is used

### With Image Understanding

When visual content matters:

**User:** "Show me what the new Tesla model looks like"

**You should:**
1. Use `search_web` with `enable_image_understanding: true`
2. Grok will analyze images found during search
3. Describe visual details in the response

## API Reference

### Function: search_web

Search the web using xAI's Grok API.

**Parameters:**
- `query` (required): Search query string
- `model` (optional): Model to use (default: "grok-4-1-fast-reasoning")
- `allowed_domains` (optional): Array of domains to restrict search (max 5)
- `excluded_domains` (optional): Array of domains to exclude (max 5)
- `enable_image_understanding` (optional): Enable image analysis (default: false)
- `stream` (optional): Stream the response (default: false)

**Returns:**
- `content`: The search response text
- `citations`: Array of sources with url, title, and snippet
- `usage`: Token usage statistics

**Example:**

```javascript
const result = await search_web({
  query: "Latest developments in quantum computing",
  allowed_domains: ["nature.com", "science.org"],
  enable_image_understanding: false
});

console.log(result.content);
result.citations.forEach(cite => {
  console.log(`Source: ${cite.title} - ${cite.url}`);
});
```

## Implementation

This skill uses the xAI Responses API directly via HTTP fetch:

```javascript
async function search_web(options) {
  const {
    query,
    model = 'grok-4-1-fast-reasoning',
    allowed_domains = null,
    excluded_domains = null,
    enable_image_understanding = false
  } = options;

  // Build tool - exactly like the official curl example
  const tool = { type: 'web_search' };
  
  // Add optional parameters directly to the tool object
  if (allowed_domains) tool.allowed_domains = allowed_domains;
  if (excluded_domains) tool.excluded_domains = excluded_domains;
  if (enable_image_understanding) tool.enable_image_understanding = true;

  // Make API request - matches official curl example
  const response = await fetch('https://api.x.ai/v1/responses', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.XAI_API_KEY}`
    },
    body: JSON.stringify({
      model,
      input: [
        {
          role: 'user',
          content: query
        }
      ],
      tools: [tool]
    })
  });

  const data = await response.json();
  const output = data.output || [];
  const lastMessage = output[output.length - 1] || {};

  return {
    content: lastMessage.content,
    citations: data.citations || []
  };
}
```

**Important:** 
- Uses `/v1/responses` endpoint (NOT `/v1/chat/completions`)
- Uses `input` array (NOT `messages` array)
- Tool type is simply `"web_search"` 
- Optional parameters go directly on the tool object

## Examples

### Example 1: Current Events

**User:** "What are the latest developments in AI regulation?"

**Agent:**
```
Uses: search_web({ query: "latest AI regulation developments" })
Returns response with current information and sources
```

### Example 2: Fact Checking with Trusted Sources

**User:** "What happened at the UN climate summit? Only use reliable news sources."

**Agent:**
```
Uses: search_web({
  query: "UN climate summit latest",
  allowed_domains: ["reuters.com", "apnews.com", "bbc.com"]
})
```

### Example 3: Technical Documentation

**User:** "How do I use async/await in JavaScript?"

**Agent:**
```
Uses: search_web({
  query: "JavaScript async await documentation",
  allowed_domains: ["developer.mozilla.org", "javascript.info"]
})
```

### Example 4: Visual Content Analysis

**User:** "What does brutalist architecture look like?"

**Agent:**
```
Uses: search_web({
  query: "brutalist architecture examples",
  enable_image_understanding: true
})
Analyzes architectural images to describe the style
```

## Response Format

When presenting search results:

1. **Lead with the answer** - Don't start with "According to my search..."
2. **Include key information** from the response
3. **Add sources at the end** in a clean format:

```
[Your answer based on search results]

Sources:
- Article Title (source.com)
- Another Article (example.org)
```

## Best Practices

### Domain Filtering
- Use `allowed_domains` for high-trust scenarios (medical, financial, legal)
- Use `excluded_domains` sparingly for known problematic sources
- Cannot use both at the same time
- Maximum 5 domains per filter

### Image Understanding
- Only enable when visual content is relevant
- Adds latency and API costs
- Useful for: products, places, diagrams, infographics
- Track usage in `server_side_tool_usage.SERVER_SIDE_TOOL_VIEW_IMAGE`

### Model Selection
- **grok-4-1-fast-reasoning**: Best for search with reasoning
- **grok-beta**: General purpose with web access
- **grok-2-1212**: Production-ready standard model

### Error Handling
- Always validate `XAI_API_KEY` is set
- Handle rate limits with exponential backoff
- Check response.ok before parsing JSON
- Provide graceful fallbacks

## Troubleshooting

### "XAI_API_KEY not found"
Set your API key:
```bash
export XAI_API_KEY="your-key-here"
```

### Rate Limiting
If you hit rate limits:
- Implement exponential backoff
- Cache frequent queries
- Use faster models for simple queries

### Poor Quality Results
- Add domain filters for better sources
- Make queries more specific
- Try reasoning models for complex topics
- Enable image understanding for visual context

## Security Notes

- Never hardcode API keys
- Store `XAI_API_KEY` in environment variables
- Validate user queries before searching
- Sanitize responses before display
- Monitor API usage and costs

## API Documentation

For complete xAI API documentation: https://docs.x.ai/developers/tools/web-search

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please submit issues and pull requests on GitHub.

## Changelog

### 1.0.0 (2026-02-14)
- Initial release
- Basic web search functionality
- Domain filtering support
- Image understanding capability
- Citation handling
- Streaming support
