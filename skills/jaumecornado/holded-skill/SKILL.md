---
name: holded-skill
description: Operate Holded ERP through holdedcli to read and update data safely. Use when the user asks to read, search, create, update, or delete Holded entities (contacts, invoices, products, CRM, projects, team, accounting) or run Holded API endpoints from the terminal.
metadata: {"openclaw":{"homepage":"https://github.com/jaumecornado/holded-skill","requires":{"bins":["holded"]},"primaryEnv":"HOLDED_API_KEY","install":[{"id":"brew","kind":"brew","formula":"jaumecornado/tap/holded","bins":["holded"],"label":"Install holdedcli (brew)"}]}}
---

# holded-skill

Use `holdedcli` to read and modify Holded data with a safe, repeatable workflow.

## Operational Flow

1. Confirm technical prerequisites.
2. Discover available actions with `holded actions list`.
3. Inspect the selected action with `holded actions describe <action-id|operation-id>`.
4. Classify the action as read or write.
5. If it is a write operation, ask for explicit confirmation before execution.
6. Run with `--json` and summarize IDs, HTTP status, and applied changes.

## Prerequisites

- Verify that the binary exists: `holded help`
- Verify credentials: `holded auth status` or `HOLDED_API_KEY`
- Prefer structured output whenever possible: `--json`

## Safety Rules

- Treat any `POST`, `PUT`, `PATCH`, or `DELETE` action as **write**.
- Treat any `GET` action (or `HEAD` when present) as **read**.
- Always run `holded actions list` and `holded actions describe` before execution to validate action availability and accepted parameters.
- Ask for explicit user confirmation **every time** before any write action.
- Do not execute writes on ambiguous replies (`ok`, `go ahead`, `continue`) without clarification.
- Repeat the exact command before confirmation to avoid unintended changes.
- If the user does not confirm, stop and offer payload adjustments.

## Mandatory Confirmation Protocol

Before any write action, show:

1. Holded action (`action_id` or `operation_id`).
2. Method and endpoint.
3. `--path`, `--query`, and body parameters (`--body` or `--body-file`).
4. The exact command to run.

Use this format:

```text
This operation will modify data in Holded.
Action: <action_id> (<METHOD> <endpoint>)
Changes: <short summary>
Command: holded actions run ... --json
Do you confirm that I should run exactly this command? (reply with "yes" or "confirm")
```

Execute only after an explicit affirmative response.

## Execution Pattern

### Read Operations

1. Locate the action with `holded actions list --json` (use `--filter`).
2. Verify accepted path/query/body parameters with `holded actions describe <action-id|operation-id> --json`.
3. Run `holded actions run <action> ... --json`.
4. Return a clear summary and relevant IDs for follow-up steps.

### Write Operations

1. Locate and validate the action.
2. Run `holded actions describe <action-id|operation-id> --json` to verify required/optional parameters.
3. Prepare the final payload.
4. Request mandatory confirmation.
5. Run the command after confirmation.
6. Report result (`status_code`, affected ID, API response).

## Base Commands

```bash
holded auth set --api-key "$HOLDED_API_KEY"
holded auth status
holded ping --json
holded actions list --json
holded actions list --filter contacts --json
holded actions describe invoice.get-contact --json
holded actions run invoice.get-contact --path contactId=<id> --json
```

For long payloads, prefer `--body-file`:

```bash
holded actions run invoice.update-contact \
  --path contactId=<id> \
  --body-file payload.json \
  --json
```

## Error Handling

- If `MISSING_API_KEY` appears, configure API key through `--api-key`, `HOLDED_API_KEY`, or `holded auth set`.
- If `ACTION_NOT_FOUND` appears, list the catalog and search with `--filter`.
- If `INVALID_BODY` appears, validate JSON before execution.
- If `API_ERROR` appears, report `status_code` and the API snippet.

## References

- Read `{baseDir}/references/holdedcli-reference.md` for quick commands and criteria.
- Use dynamic action discovery and parameter inspection via:
  - `holded actions list --json`
  - `holded actions describe <action-id|operation-id> --json`
