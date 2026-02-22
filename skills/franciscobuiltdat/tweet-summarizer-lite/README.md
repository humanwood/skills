# Tweet Summarizer Lite

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Fetch and summarize single tweets from Twitter/X. Lightweight version for quick lookups.

## Features

- **Single Tweet Fetching** - Fetch individual tweets by URL
- **Basic Search** - Search stored tweets by text, source, or date
- **Auto-Summary** - Generate summaries after fetching
- **Simple Storage** - Clean organized file storage

## Prerequisites

Requires the `bird` CLI tool with valid Twitter session cookies.

```bash
# Set authentication
export AUTH_TOKEN="your_auth_token"
export CT0="your_ct0_token"
```

See [SECURITY.md](SECURITY.md) for how to obtain these safely.

## Installation

```bash
# Clone the repository
git clone https://github.com/openclaw/openclaw-tweet-summarizer-lite.git
cd openclaw-tweet-summarizer-lite

# No additional dependencies required
```

## Quick Start

```bash
# Fetch a tweet
python3 scripts/tweet.py https://x.com/elonmusk/status/123456789

# Search stored tweets
python3 scripts/search_tweets.py --text "AI"

# View storage stats
python3 scripts/search_tweets.py --stats
```

## Usage

### Fetch Tweet

```bash
# Fetch with auto-summary (default)
python3 scripts/tweet.py https://x.com/user/status/123

# Skip summary
python3 scripts/tweet.py https://x.com/user/status/123 -ns
```

### Search Tweets

```bash
# By text
python3 scripts/search_tweets.py --text "artificial intelligence"

# By source
python3 scripts/search_tweets.py --source elonmusk

# Since date
python3 scripts/search_tweets.py --since 2026-02-01

# List sources
python3 scripts/search_tweets.py --list-sources
```

### Summarize

```bash
python3 scripts/summarize.py <source_or_file>
```

## Configuration

```json
{
  "defaults": {
    "show_summary": true,
    "auto_detect_urls": true,
    "default_mode": "single"
  }
}
```

## Pro Version

Need threads, collections, and user timelines? Check out [tweet-summarizer-pro](https://github.com/openclaw/openclaw-tweet-summarizer-pro):

- Thread fetching
- Custom collections with archive/restore
- User and home timeline fetching
- Advanced folder organization
- Tags for categorization

## Contributing

Contributions welcome! Please read [SECURITY.md](SECURITY.md) before contributing.

## License

MIT - see [LICENSE](LICENSE)
