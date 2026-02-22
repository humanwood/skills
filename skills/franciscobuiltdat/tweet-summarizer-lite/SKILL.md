---
name: tweet-summarizer-lite
description: Fetch and summarize single tweets from Twitter/X. Basic search and single tweet fetching. Lightweight version perfect for quick tweet lookups.
requiredEnv:
  - AUTH_TOKEN
  - CT0
requiredBins:
  - bird
permissions:
  - network: Contact X/Twitter API via bird CLI (uses session cookies)
  - filesystem: Write tweets to ~/.openclaw/workspace/data/tweets/
---

# Tweet Summarizer Lite

Fetch and summarize single tweets from Twitter/X. Lightweight version for quick lookups.

## Features

- 🐦 **Single tweet fetching** - Fetch individual tweets by URL
- 🔍 **Basic search** - Search for tweets by query
- 📊 **Auto-summary** - Generate summaries after fetching
- 📁 **Simple storage** - Organized file storage

## Prerequisites

Requires `bird` CLI with valid cookie auth. Set `AUTH_TOKEN` and `CT0` environment variables.

## Quick Start

```bash
# Fetch a single tweet
python3 scripts/tweet.py https://x.com/user/status/123

# Search for tweets
python3 scripts/search_tweets.py --text "AI agents"

# Skip summary
python3 scripts/tweet.py https://x.com/user/status/123 -ns
```

## Usage

### Fetch Single Tweet

```bash
python3 scripts/tweet.py <URL>
```

Options:
- `-ns` or `--no-summary` - Skip auto-summary

### Search Stored Tweets

```bash
# By text content
python3 scripts/search_tweets.py --text "artificial intelligence"

# By source
python3 scripts/search_tweets.py --source elonmusk

# By date
python3 scripts/search_tweets.py --since 2026-02-01

# List all sources
python3 scripts/search_tweets.py --list-sources

# Storage stats
python3 scripts/search_tweets.py --stats
```

### Generate Summary

```bash
# From stored file
python3 scripts/summarize.py <file_path>

# From source
python3 scripts/summarize.py elonmusk
```

## Storage Structure

```
~/.openclaw/workspace/data/tweets/
├── index.json           # Master search index
└── single/
    └── <tweet-id>/      # Individual tweets
        └── single_*.json
```

## Configuration

Edit `config.json`:

```json
{
  "defaults": {
    "show_summary": true,
    "auto_detect_urls": true,
    "default_mode": "single"
  }
}
```

## Direct Bird Commands

For quick reads without storage:

```bash
# Read tweet (plain text)
bird read <url-or-id> --plain

# Search
bird search "query" -n 20 --plain
```

## Upgrading to Pro

Need more features? [tweet-summarizer-pro](https://github.com/openclaw/openclaw-tweet-summarizer-pro) includes:

- 🧵 **Thread fetching** - Fetch full conversation threads
- 📂 **Collections** - Organize tweets into custom collections
- 👤 **User timelines** - Fetch tweets from specific users
- 🏠 **Home timeline** - Fetch your home/following timeline
- 🏷️ **Tags** - Tag tweets for organization
- 📦 **Archive** - Archive and restore collections

## Scripts

| Script | Description |
|--------|-------------|
| `tweet.py` | Fetch single tweet + summary |
| `fetch_tweets.py` | Low-level fetch (single only) |
| `search_tweets.py` | Search stored tweets |
| `summarize.py` | Generate summaries |
| `config.py` | Manage configuration |

## Files

- `config.json` - Default settings
- `config.example.json` - Example configuration
- `scripts/` - All scripts
