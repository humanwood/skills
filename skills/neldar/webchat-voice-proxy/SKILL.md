---
name: webchat-voice-proxy
description: Voice input and microphone button for OpenClaw WebChat Control UI. Adds a mic button to chat, records audio via browser MediaRecorder, transcribes locally via faster-whisper, and injects text into the conversation. Includes HTTPS/WSS reverse proxy, TLS cert management, and gateway hook for update safety. Fully local speech-to-text, no API costs. Keywords: voice input, microphone, WebChat, Control UI, speech to text, STT, local transcription, MediaRecorder, HTTPS proxy, voice button, mic button.
---

# WebChat Voice Proxy

Set up a reboot-safe voice stack for OpenClaw WebChat (including the current polished mic/stop/hourglass UI states):
- HTTPS Control UI on port 8443
- `/transcribe` proxy to local faster-whisper service
- WebSocket passthrough to gateway (`ws://127.0.0.1:18789`)
- Voice button script injection into Control UI

## Prerequisites (required)

This skill requires a **local faster-whisper HTTP service**.

Expected default:
- URL: `http://127.0.0.1:18790/transcribe`
- systemd user service: `openclaw-transcribe.service`

Verify before deployment:

```bash
systemctl --user is-active openclaw-transcribe.service
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:18790/transcribe -X POST -H 'Content-Type: application/octet-stream' --data-binary 'x'
```

If this dependency is missing, set up faster-whisper first (model load + HTTP endpoint), then run this skill.

Related skills:
- `faster-whisper-local-service` (backend prerequisite)
- `webchat-voice-full-stack` (meta-installer that deploys both backend + proxy)

## Workflow

1. Ensure transcription service exists and is running (`openclaw-transcribe.service`).
2. Deploy `voice-input.js` to Control UI assets and inject script tag into `index.html`.
3. Configure gateway allowed origin for external HTTPS UI.
4. Run HTTPS+WSS proxy as persistent user systemd service (`openclaw-voice-https.service`).
5. Verify pairing/token/origin errors and resolve in order.

## Deploy

Run (auto-detect host IP):

```bash
bash scripts/deploy.sh
```

Or set host/port explicitly:

```bash
VOICE_HOST=10.0.0.42 VOICE_HTTPS_PORT=8443 bash scripts/deploy.sh
```

This script is idempotent.

## Quick verify

Run:

```bash
bash scripts/status.sh
```

Expected:
- both services active
- injection present
- `https:200`

## Common fixes

- `404 /chat?...` → SPA fallback missing in HTTPS proxy.
- `origin not allowed` → ensure deploy used correct `VOICE_HOST` and added matching HTTPS origin to `gateway.controlUi.allowedOrigins`.
- `token missing` → open URL with `?token=...` once.
- `pairing required` → approve pending device via `openclaw devices approve <requestId> --token <gateway-token>`.
- Mic breaks after reboot → cert paths must be persistent (not `/tmp`).
- No transcription result → check local faster-whisper endpoint first.

See `references/troubleshooting.md` for exact commands.
