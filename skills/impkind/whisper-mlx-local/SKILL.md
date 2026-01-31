---
name: local-whisper
description: "Free local speech-to-text using MLX Whisper on Apple Silicon. Free, private, no API costs."
metadata:
  openclaw:
    emoji: "🎤"
    version: "1.2.0"
    author: "Community"
    repo: "https://github.com/ImpKind/local-whisper"
    requires:
      os: ["darwin"]
      arch: ["arm64"]
      bins: ["python3"]
    install:
      - id: "deps"
        kind: "manual"
        label: "Install dependencies"
        instructions: "pip3 install -r requirements.txt"
---

# Local Whisper

**Transcribe voice messages for free.** No API keys. No costs. Runs on your Mac.

## The Problem

Voice transcription APIs cost money:
- OpenAI Whisper: **$0.006/minute**
- Groq: **$0.001/minute**  
- AssemblyAI: **$0.01/minute**

If you transcribe a lot of Telegram voice messages, it adds up.

## The Solution

This skill runs Whisper **locally on your Mac**. Same quality, **zero cost**.

- ✅ Free forever
- ✅ Private (audio never leaves your Mac)
- ✅ Fast (~1 second per message)
- ✅ Works offline

## Quick Start

```bash
# Install
pip3 install -r requirements.txt

# Start (keeps model loaded for instant transcription)
python3 scripts/daemon.py

# Transcribe
./scripts/transcribe.sh voice_message.ogg
```

## Use Case: Telegram Voice Messages

Instead of paying for OpenAI API to transcribe incoming voice messages, point OpenClaw to this local daemon. Free transcription forever.

## Auto-Start on Login

```bash
cp com.local-whisper.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.local-whisper.plist
```

## API

Daemon runs at `localhost:8787`:

```bash
curl -X POST http://localhost:8787/transcribe -F "file=@audio.ogg"
# {"text": "Hello world", "language": "en"}
```

## Translation

Any language → English:

```bash
./scripts/transcribe.sh spanish_audio.ogg --translate
```

## Requirements

- macOS with Apple Silicon (M1/M2/M3/M4)
- Python 3.9+

## License

MIT
