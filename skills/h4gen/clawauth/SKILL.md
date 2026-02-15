---
name: clawauth
description: Secure delegated OAuth for agents: request user approval, hand off a short auth link, then claim provider access tokens for direct third-party API calls without a central SaaS token vault.
metadata: {"openclaw":{"emoji":"🔐","homepage":"https://auth.clawauth.app"}}
---

# Clawauth OAuth Skill

This skill gives agents a production-safe OAuth handover flow that is async by default and works across chat/session interruptions.

Use this when the agent needs provider credentials from a human user, but must avoid blocking execution and must avoid long-lived token storage on a third-party auth SaaS.

## Why this exists

Most "OAuth gateway" patterns keep user refresh tokens in a central hosted database. clawauth avoids that model:

- Hosted edge service mints short-lived auth sessions.
- User authorizes directly with the provider.
- Token response is encrypted end-to-end to the requesting CLI session.
- CLI claims once and stores token locally in system keychain.
- Server-side session is ephemeral and deleted on claim/expiry.

Result: async UX for agents, minimal operator overhead, and no permanent central token vault by design.

## How the agent gets the command

The agent must be able to run `clawauth` commands. Use one of these methods:

1) Zero-install invocation:

```bash
npx clawauth --help
```

2) Global install:

```bash
npm i -g clawauth
clawauth --help
```

3) Project-local install:

```bash
npm i clawauth
npx clawauth --help
```

4) Optional version pinning can be enforced by the operator in the runtime/tooling policy.

If `clawauth` is not found, use `npx clawauth ...` or an operator-approved pinned version.

## Hosted service endpoint

The published CLI is already wired to:

- `https://auth.clawauth.app`

Agents do not need `CLAWAUTH_WORKER_URL` for normal hosted usage.

## Provider support

Implemented providers in current worker:

- notion
- github
- discord
- linear
- airtable
- todoist
- asana
- trello
- dropbox
- digitalocean
- slack
- gitlab
- reddit
- figma
- spotify
- bitbucket
- box
- calendly
- fathom
- twitch

Always treat server output as source of truth:

```bash
clawauth providers --json
```

## Canonical async flow (non-blocking)

1) Start auth and return immediately:

```bash
clawauth login start <provider> --json
```

2) Extract and forward `shortAuthUrl` to the user.

3) Continue other work. Do not block.

4) Later poll/check:

```bash
clawauth login status <sessionId> --json
```

5) When status is `completed`, claim once:

```bash
clawauth login claim <sessionId> --json
```

6) Use stored token later:

```bash
clawauth token get <provider> --json
clawauth token env <provider>
```

Use `token env` only when a downstream command explicitly needs env vars in the same process.

## Command map

### Login lifecycle

- `clawauth login start [provider] [--ttl <seconds>] [--scope <scope>] [--json]`
- `clawauth login status <sessionId> [--json]`
- `clawauth login claim <sessionId> [--json]`
- `clawauth login wait <sessionId> [--timeout <ms>] [--interval <ms>] [--json]`

### Session management

- `clawauth sessions [--json]`
- `clawauth session-rm <sessionId> [--json]`

### Token access

- `clawauth token list [--json]`
- `clawauth token get [provider] [--json]`
- `clawauth token env [provider] [--json]`

### Discovery and docs

- `clawauth providers [--json]`
- `clawauth explain`
- `clawauth docs`

## JSON fields agents should parse

### `login start --json`

- `provider`
- `sessionId`
- `expiresIn`
- `shortAuthUrl`
- `authUrl`
- `statusCommand`
- `claimCommand`

### `login status --json`

- `status` (`pending | completed | error`)
- `provider`
- `error`

### `login claim --json`

- `status` (`pending | completed | error`)
- `provider`
- `tokenData`
- `storedInKeychain`
- `keychainService`
- `keychainAccount`

### `token get --json`

- `action`
- `account`
- `token.provider`
- `token.access_token`
- `token.refresh_token`
- `token.token_type`
- `token.saved_at`

## Agent behavior rules

- Prefer `--json` for machine parsing.
- Never block by default; only use `login wait` when explicitly needed.
- On `pending`: schedule retry later.
- On `completed`: run `login claim` once.
- On `error`: surface concise reason and restart with new `login start`.
- If session context is lost, recover using `clawauth sessions --json`.
- If provider unknown, run `clawauth providers --json` and choose supported value.
- Never print raw tokens into user-facing chat.
- Do not use `npx ...@latest` in autonomous execution.
- Avoid shell-wide token exports unless strictly required for the immediate API call.

## Security model summary

- Short-lived session data in Cloudflare KV (default TTL: 3600s, configurable).
- Signed OAuth `state` binding provider and expiry.
- Signed request verification for status/claim with timestamp + nonce.
- Replay and rate-limit protections during polling.
- End-to-end encrypted token blob (`nacl.box`) from callback to CLI claimant.
- Session blob removed from server on successful claim.
- Tokens stored locally in OS keychain via CLI.

## Failure handling

Provider not implemented:

- `login start` returns error indicating feature request recorded.

Provider misconfigured on backend:

- server returns clear missing secret/config message.

Session expired:

- `status`/`claim` returns not found/expired; start new session.

Lost chat context:

- run `clawauth sessions --json`, then continue with `status`/`claim`.

No token found later:

- run `clawauth token list --json` and select provider/account explicitly.

## Minimal end-to-end example

```bash
# 1) Start
clawauth login start notion --json

# 2) Share shortAuthUrl with user (from JSON output)

# 3) Later check
clawauth login status <sessionId> --json

# 4) Claim when completed
clawauth login claim <sessionId> --json

# 5) Use token
clawauth token get notion --json
```

## Reference

See `references/commands.md` for compact copy-paste command blocks.
