# Coupler.io

Read-only data access via Coupler.io's MCP server.

**Author:** Coupler.io Team
**Homepage:** [coupler.io](https://coupler.io)

## Prerequisites

- [mcporter](https://github.com/openclaw/mcporter) CLI installed and on PATH
- Coupler.io account with at least one data flow configured to OpenClaw destination

## Quick Reference

```bash
mcporter call coupler.list-dataflows
mcporter call coupler.get-dataflow dataflowId=<uuid>
mcporter call coupler.get-schema executionId=<exec-id>
mcporter call coupler.get-data executionId=<exec-id> query="SELECT * FROM data LIMIT 10"
```

---

## Connection Setup

> **Endpoint verification:** This skill connects to `auth.coupler.io` (OAuth) and `mcp.coupler.io` (MCP data). These are official Coupler.io endpoints. You can verify them via your Coupler.io account (AI integrations page).

### 1. Add the server to mcporter config

```bash
mcporter config add coupler --url https://mcp.coupler.io/mcp
```

### 2. Authenticate via OAuth

```bash
mcporter auth --http-url https://mcp.coupler.io/mcp --persist config/mcporter.json         
```

This opens the browser for Coupler.io login and handles the OAuth flow (PKCE) automatically. Tokens are stored in mcporter's config.

To re-authenticate (e.g. after revoking access):

```bash
mcporter auth coupler --reset
```

### 3. Verify

```bash
mcporter list coupler --schema
```

---

## Token Refresh

mcporter handles token refresh automatically on 401 errors. No manual intervention needed.

If you need to force a fresh token: `mcporter auth coupler --reset`

---

## MCP Tools

### list-dataflows

List all data flows with OpenClaw destination.

```bash
mcporter call coupler.list-dataflows --output json
```

### get-dataflow

Get flow details including `lastSuccessfulExecutionId`.

```bash
mcporter call coupler.get-dataflow dataflowId=<uuid> --output json
```

### get-schema

Get column definitions. Column names are in `columnName` (e.g., `col_0`, `col_1`).

```bash
mcporter call coupler.get-schema executionId=<exec-id>
```

### get-data

Run SQL on flow data. Table is always `data`.

```bash
mcporter call coupler.get-data executionId=<exec-id> query="SELECT col_0, col_1 FROM data WHERE col_2 > 100 LIMIT 50"
```

**Always sample first** (`LIMIT 5`) to understand structure before larger queries.

---

## Typical Workflow

```bash
# 1. List flows, find ID
mcporter call coupler.list-dataflows --output json | jq '.[] | {name, id}'

# 2. Get execution ID
mcporter call coupler.get-dataflow dataflowId=<id> --output json | jq '.lastSuccessfulExecutionId'

# 3. Check schema
mcporter call coupler.get-schema executionId=<exec-id>

# 4. Query
mcporter call coupler.get-data executionId=<exec-id> query="SELECT * FROM data LIMIT 10"
```

---

## Constraints

- Read-only: cannot modify flows, sources, or data
- Only flows with OpenClaw destination are visible
- Tokens expire in 2 hours (mcporter refreshes automatically)
