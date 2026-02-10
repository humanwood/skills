---
name: relayplane
description: Cut API costs 40-60% with intelligent model routing. Auto-routes simple tasks to cheaper models, keeps Opus for complex reasoning.
user-invocable: true
model-invocable: true
disableModelInvocation: false
homepage: https://relayplane.com
version: 2.3.1
author: Continuum
license: MIT
requiredBins:
  - node
  - npx
metadata:
  openclaw:
    emoji: "🚀"
    category: ai-tools
    requires:
      bins: ["node", "npx"]
    env:
      optional:
        - name: ANTHROPIC_API_KEY
          purpose: "Forward requests to Anthropic API (never transmitted to RelayPlane)"
        - name: OPENAI_API_KEY
          purpose: "Forward requests to OpenAI API (never transmitted to RelayPlane)"
        - name: GOOGLE_API_KEY
          purpose: "Forward requests to Google API (never transmitted to RelayPlane)"
        - name: RELAYPLANE_API_KEY
          purpose: "Optional - enables cloud dashboard and authenticated telemetry"
    network:
      - host: "api.anthropic.com"
        purpose: "Forward LLM requests (using your API key)"
      - host: "api.openai.com"
        purpose: "Forward LLM requests (using your API key)"
      - host: "api.relayplane.com"
        purpose: "Telemetry upload (anonymized, opt-out available)"
    telemetry:
      enabled-by-default: true
      opt-out: "relayplane-proxy telemetry off"
      collects:
        - "model (which model was used)"
        - "tokens (input/output counts, not content)"
        - "latency (response time)"
        - "cost (estimated USD)"
        - "task_type (routing category)"
        - "device_id (anonymous installation identifier)"
      never-collects:
        - "prompts (message content)"
        - "responses (model output)"
        - "file_paths"
        - "API keys"
        - "user identity"
    capabilities:
      reads-env: true
      network-access: true
      executes-code: true
    model-invocation-rationale: |
      Model invocation is intentionally enabled because:
      1. The skill only performs READ operations (stats, status, doctor) by default
      2. Proxy start requires explicit user command (/relayplane proxy start)
      3. All API costs are from the user's existing LLM usage, not new requests
      4. No destructive operations are possible
    security-notes: |
      CREDENTIAL HANDLING:
      - Reads LLM provider API keys from environment to forward your requests
      - Keys stay local - they are NEVER transmitted to RelayPlane servers
      - Verify this claim: inspect relayplane.js or run with RELAYPLANE_OFFLINE=1
      
      TELEMETRY:
      - Enabled by default to improve routing intelligence
      - Collects only anonymized usage metadata (model, tokens, latency)
      - Never collects prompts, responses, or identifying information
      - Disable anytime: relayplane-proxy telemetry off
      
      COST CONTROL:
      - The proxy routes YOUR existing LLM requests - it doesn't create new ones
      - Monitor usage: /relayplane stats
      - All costs are from your normal AI usage, optimized for savings
---

# RelayPlane

**Intelligent AI routing that saves you money.**

Route LLM requests through RelayPlane to automatically use the optimal model for each task.

> ⚠️ **Cost Monitoring Required**
>
> RelayPlane routes requests to LLM providers using your API keys. **This incurs real costs.**
> Use `/relayplane stats` to track usage and savings.

## Slash Commands

| Command | Description |
|---------|-------------|
| `/relayplane stats` | Show usage statistics and cost savings |
| `/relayplane status` | Show proxy health and configuration |
| `/relayplane doctor` | Diagnose configuration and connectivity issues |
| `/relayplane proxy [start\|stop\|status]` | Manage the proxy server |
| `/relayplane telemetry [on\|off\|status]` | Manage telemetry settings |
| `/relayplane dashboard` | Get link to cloud dashboard |
| `/relayplane models` | List available routing modes and aliases |

## Usage

When user invokes `/relayplane <subcommand>`, run:

```bash
node {baseDir}/relayplane.js <subcommand>
```

Examples:
- `/relayplane stats` → `node {baseDir}/relayplane.js stats`
- `/relayplane doctor` → `node {baseDir}/relayplane.js doctor`
- `/relayplane proxy start` → `node {baseDir}/relayplane.js proxy start`
- `/relayplane telemetry off` → `node {baseDir}/relayplane.js telemetry off`

## Quick Start

```bash
# Install CLI globally
npm install -g @relayplane/cli @relayplane/proxy

# Check configuration
relayplane doctor

# Start proxy
relayplane proxy start

# Point your SDKs to the proxy
export ANTHROPIC_BASE_URL=http://localhost:3001
export OPENAI_BASE_URL=http://localhost:3001

# Use routing aliases in your API calls
# model: "rp:auto"     - Smart routing
# model: "rp:cost"     - Cheapest model
# model: "rp:best"     - Best quality
# model: "rp:fast"     - Fastest response
```

## Model Routing Aliases

| Alias | Description |
|-------|-------------|
| `rp:auto` / `relayplane:auto` | Smart routing based on task complexity |
| `rp:cost` / `rp:cheap` | Always cheapest model (GPT-4o-mini) |
| `rp:fast` | Lowest latency (Claude Haiku) |
| `rp:best` / `rp:quality` | Best quality (Claude Sonnet 4) |
| `rp:balanced` | Balance of cost and quality |

## Telemetry Control

RelayPlane collects anonymous usage data to improve routing. You can control this:

```bash
relayplane-proxy telemetry status  # Check current setting
relayplane-proxy telemetry off     # Disable completely
relayplane-proxy telemetry on      # Re-enable

# Or run with flags:
relayplane-proxy --offline   # Disable transmission
relayplane-proxy --audit     # See what's sent before sending
```

**What's collected:** Model used, token counts, latency, task type.
**What's NOT collected:** Prompts, responses, or any message content.

## Pricing

- **Free:** Local-only mode, unlimited requests, no account required
- **Pro:** $29/month - Cloud dashboard, analytics, team features
- **Max:** $99/month - Policies, budget controls, 5 team seats
- **Enterprise:** Custom pricing, SSO, audit logs, self-hosted

Sign up at [relayplane.com/trial](https://relayplane.com/trial)

## More Info

- [Dashboard](https://relayplane.com/dashboard)
- [Documentation](https://relayplane.com/docs)
- [GitHub](https://github.com/RelayPlane)
