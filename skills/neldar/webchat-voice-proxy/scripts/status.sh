#!/usr/bin/env bash
set -euo pipefail

systemctl --user is-active openclaw-transcribe.service openclaw-voice-https.service

grep -q 'voice-input.js' /home/openclaw/.npm-global/lib/node_modules/openclaw/dist/control-ui/index.html && echo 'inject:ok' || echo 'inject:missing'

curl -sk https://127.0.0.1:8443/chat?session=main -o /dev/null -w 'https:%{http_code}\n'

echo 'status:done'
