---
name: scrapling
description: "Adaptive web scraping framework with anti-bot bypass and spider crawling. Full features except MCP server."
version: "1.2.0"
metadata:
  {"openclaw":{"emoji":"🕷️","requires":{"bins":["python3","pip"]}, "tags":["web-scraping", "crawling", "research", "automation"]}}
---

# Scrapling - Adaptive Web Scraping

> "Effortless web scraping for the modern web."

---

## Credits

- **Repository:** https://github.com/D4Vinci/Scrapling
- **Author:** D4Vinci
- **License:** MIT
- **Documentation:** https://scrapling.readthedocs.io

---

## Installation

```bash
# Core library (basic scraping)
pip install scrapling

# With fetchers (HTTP + browser automation) - RECOMMENDED
pip install "scrapling[fetchers]"

# With shell (CLI tools) - RECOMMENDED
pip install "scrapling[shell]"

# With AI (MCP server) - OPTIONAL
pip install "scrapling[ai]"

# Everything except MCP
pip install "scrapling[fetchers,shell]"

# Browser for stealth mode
playwright install chromium
```

---

## Agent Instructions

### When to Use Scrapling

**Use Scrapling when:**
- Research topics from websites
- Extract data from blogs, news sites, docs
- Crawl multiple pages with Spider
- Gather content for summaries
- Bypass anti-bot protection

**Do NOT use for:**
- X/Twitter (use x-tweet-fetcher skill)
- Login-protected sites (unless credentials provided)
- Paywalled content (respect robots.txt)

---

## Quick Commands

### 1. Basic Fetch (Most Common)

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://example.com')

# Extract content
title = page.css('h1::text').get()
paragraphs = page.css('p::text').getall()
```

### 2. Stealthy Fetch (Anti-Bot)

```python
from scrapling.fetchers import StealthyFetcher

StealthyFetcher.adaptive = True
page = StealthyFetcher.fetch('https://example.com', headless=True)
```

### 3. Adaptive Parsing (Survives Design Changes)

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://example.com')

# First scrape - saves selectors
items = page.css('.product', auto_save=True)

# Later - if site changes, use adaptive=True to relocate
items = page.css('.product', adaptive=True)
```

### 4. Spider (Multiple Pages)

```python
from scrapling.spiders import Spider, Response

class MySpider(Spider):
    name = "demo"
    start_urls = ["https://example.com"]
    concurrency = 3
    
    async def parse(self, response: Response):
        # Extract items
        for item in response.css('.item::text').getall():
            yield {"item": item}
        
        # Follow links
        next_page = response.css('.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page)

MySpider().start()
```

### 5. CLI Usage

```bash
# Simple fetch
scrapling extract get https://example.com /tmp/page.html

# Stealthy fetch
scrapling extract stealthy-fetch https://example.com /tmp/page.html

# Interactive shell
scrapling shell https://example.com
```

---

## Common Patterns

### Extract Article Content

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://spectrum.ieee.org/moltbook-agentic-ai-agents-openclaw')

# Try multiple selectors for title
title = (
    page.css('[itemprop="headline"]::text').get() or
    page.css('article h1::text').get() or
    page.css('h1::text').get()
)

# Get paragraphs
content = page.css('article p::text, .article-body p::text').getall()

print(f"Title: {title}")
print(f"Paragraphs: {len(content)}")
```

### Research Multiple Pages

```python
from scrapling.spiders import Spider, Response

class ResearchSpider(Spider):
    name = "research"
    start_urls = ["https://news.ycombinator.com"]
    concurrency = 5
    
    async def parse(self, response: Response):
        # Get stories
        for item in response.css('.titleline a::text').getall()[:10]:
            yield {"title": item, "source": "HN"}
        
        # Next page
        more = response.css('.morelink::attr(href)').get()
        if more:
            yield response.follow(more)

ResearchSpider().start()
```

### Handle Errors

```python
from scrapling.fetchers import Fetcher, StealthyFetcher

try:
    page = Fetcher.get('https://example.com')
except Exception as e:
    # Try stealth mode
    page = StealthyFetcher.fetch('https://example.com', headless=True)
    
if page.status == 403:
    print("Blocked - try StealthyFetcher")
elif page.status == 200:
    print("Success!")
```

---

## Feature Comparison

| Feature | Status | Notes |
|---------|--------|-------|
| Basic fetch | ✅ Working | Fetcher.get() |
| Stealthy fetch | ✅ Working | StealthyFetcher.fetch() |
| Adaptive parsing | ✅ Working | auto_save + adaptive |
| Spider crawling | ✅ Working | async def parse() |
| CSS selectors | ✅ Working | .css() |
| XPath | ✅ Working | .xpath() |
| CLI tools | ✅ Working | scrapling extract |
| Session/cookies | ⚠️ Via storage | Use Fetcher.configure(storage=True) |
| Proxy rotation | ⚠️ Limited | Configure at fetcher level |
| MCP server | ❌ Excluded | Not needed |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 403/429 Blocked | Use StealthyFetcher with headless=True |
| Cloudflare | Use StealthyFetcher - handles automatically |
| JavaScript required | Use DynamicFetcher |
| Site changed | Use adaptive=True |
| Captcha | Cannot bypass - skip or use human |

---

## Examples Tested

### IEEE Spectrum
```python
page = Fetcher.get('https://spectrum.ieee.org/...')
title = page.css('h1::text').get()
content = page.css('article p::text').getall()
```
✅ Works

### Hacker News
```python
page = Fetcher.get('https://news.ycombinator.com')
stories = page.css('.titleline a::text').getall()
```
✅ Works

### Example Domain
```python
page = Fetcher.get('https://example.com')
title = page.css('h1::text').get()
```
✅ Works

---

## Skill Graph

Related skills:

- [[content-research]] - Research workflow
- [[blogwatcher]] - RSS/feed monitoring
- [[youtube-watcher]] - Video content
- [[chirp]] - Twitter/X interactions
- [[newsletter-digest]] - Content summarization
- [[x-tweet-fetcher]] - X/Twitter (use instead of Scrapling)

---

## Changelog

### v1.2.0 (2026-02-24)
- Full features documented (except MCP)
- CLI usage added
- Agent instructions clarified
- Tested: basic fetch, stealth, spider, CLI

### v1.1.0 (2026-02-24)
- Initial release with agent instructions

---

*Last updated: 2026-02-24*
