---
name: feishu-file-sender
description: OpenClaw agents can generate files (Excel, Word, PPT, PDF, images, code, etc.) but cannot send them directly to Feishu chat — they can only output a local file path. This skill bridges that gap: it uploads any local file to Feishu via OpenAPI and sends it as a downloadable attachment in the current chat. Works for all agents by auto-detecting credentials from openclaw.json. Supports any file format.
license: MIT
compatibility: openclaw
metadata:
  version: "1.0.3"
  tags: [feishu, file, upload, im, messaging, openapi]
  author: wen-ai
  openclaw:
    emoji: "📎"
    requires:
      bins: [python3]
      config:
        - ~/.openclaw/openclaw.json
---

# Feishu File Sender

Upload a local file to Feishu and send it as a file message.

## Quick Start

```bash
python3 scripts/feishu_file_sender.py \
  --file /absolute/path/to/report.xlsx \
  --receive-id oc_xxx
```

## Usage

```bash
python3 scripts/feishu_file_sender.py \
  --file /absolute/path/to/file \
  --receive-id <chat_id|open_id> \
  --receive-id-type <chat_id|open_id|user_id>
```

### Arguments

- `--file` (required): Absolute path to the local file.
- `--receive-id` (optional): Target chat_id or open_id. If omitted, the script
  reads `OPENCLAW_CHAT_ID` (or `OPENCLAW_RECEIVE_ID` / `FEISHU_CHAT_ID`).
- `--receive-id-type` (optional): If omitted, auto-detect by prefix:
  - `oc_` → chat_id
  - `ou_` → open_id
  - `on_` → user_id
- `--file-type` (optional): Feishu file upload type, default `stream`.

## How It Works

1. Resolve the current agent id by matching `cwd` to OpenClaw workspace path.
2. Read appId/appSecret from `~/.openclaw/openclaw.json` based on the agent id.
3. Call Feishu **Upload File** API to get `file_key`.
4. Call Feishu **Send Message** API to deliver the file.

## Error Handling

- **Missing credentials** → Ensure `channels.feishu.accounts` exists in
  `~/.openclaw/openclaw.json` and bindings map agentId → accountId.
- **Bot not in chat (code 230002)** → Add the bot to the target chat or use a
  chat where the bot is present.
- **Missing receive_id** → Pass `--receive-id` or set `OPENCLAW_CHAT_ID`.
- **HTTP errors** → Check the returned `log_id` in Feishu error payload.

## Security

This skill reads Feishu credentials from the local OpenClaw config
(`~/.openclaw/openclaw.json`) on the machine where it runs:

- `channels.feishu.accounts.*.appId`
- `channels.feishu.accounts.*.appSecret`

These values are used only to obtain a tenant access token and send the file.
The skill does not store or transmit credentials anywhere else.

## Notes

- This skill is designed for **all agents**; it reads the active workspace to
  choose the correct Feishu app credentials automatically.
- Prefer sending to the **current chat** by passing the inbound `chat_id`.

## Bundled Script

- `scripts/feishu_file_sender.py`
