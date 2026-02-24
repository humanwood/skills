# Feishu File Sender

Upload a local file to Feishu OpenAPI and send it into a chat.

## Features

- 📎 Upload local files and send as Feishu file messages
- 🔑 Auto-resolve appId/appSecret from OpenClaw config
- 🧭 Works across **all agents** based on workspace
- 🧰 Simple CLI for quick use

## Requirements

- Python 3.6+
- `requests` installed
- OpenClaw with Feishu channel configured

## Install

```bash
python3 -m pip install requests
```

## Usage

### Send to current chat (recommended)

```bash
# If your runtime provides the chat id via environment
export OPENCLAW_CHAT_ID=oc_xxx

python3 scripts/feishu_file_sender.py \
  --file /absolute/path/to/report.xlsx
```

### Send to a specific chat

```bash
python3 scripts/feishu_file_sender.py \
  --file /absolute/path/to/report.xlsx \
  --receive-id oc_xxx \
  --receive-id-type chat_id
```

### Send to a user

```bash
python3 scripts/feishu_file_sender.py \
  --file /absolute/path/to/report.xlsx \
  --receive-id ou_xxx \
  --receive-id-type open_id
```

## How It Works

1. Resolve current agent id by matching `cwd` to the configured workspace.
2. Read Feishu `appId/appSecret` from `~/.openclaw/openclaw.json` via bindings.
3. Upload the file to Feishu (`im/v1/files`) and get `file_key`.
4. Send a file message (`im/v1/messages`) to the target chat/user.

## Error Handling

| Issue | Cause | Fix |
|------|------|-----|
| `Missing receive_id` | No `--receive-id` and no env | Set `OPENCLAW_CHAT_ID` or pass `--receive-id` |
| `No Feishu account binding` | Agent binding missing | Ensure bindings map agentId → accountId in OpenClaw config |
| `Bot/User can NOT be out of the chat (230002)` | Bot not in chat | Add the bot to the chat or send to a different chat |
| `HTTPError` | API failure | Check response `log_id` and Feishu troubleshooting link |

## Configuration

OpenClaw should already have Feishu accounts configured in `~/.openclaw/openclaw.json`.
This skill only **reads** config; it does not modify any files.

## Security

This skill reads Feishu credentials from your local OpenClaw config
(`~/.openclaw/openclaw.json`):

- `channels.feishu.accounts.*.appId`
- `channels.feishu.accounts.*.appSecret`

These values are used only to obtain a tenant access token and send the file.
The skill does not store or transmit credentials anywhere else.

## License

MIT
