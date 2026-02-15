---
name: opencode-omo
description: Use OpenCode + Oh-My-OpenCode (Sisyphus/Prometheus/Atlas) as the coding backend. Sisyphus-first workflow.
homepage: https://github.com/IISweetHeartII/openclaw-skills
metadata: {"openclaw":{"emoji":"🧱","category":"devtools","tags":["opencode","oh-my-opencode","sisyphus","coding"],"requires":{"bins":["opencode","git","clawhub"]}}}
---

# OpenCode + Oh-My-OpenCode Operator

This skill is an operating guide for using **OpenCode** as the place where planning/coding happens, with **Oh-My-OpenCode** providing Sisyphus/Prometheus/Atlas workflows.

## Core rules

- Do not edit code directly outside OpenCode unless explicitly asked.
- Prefer Sisyphus-first execution for coding tasks.
- For complex work: plan with Prometheus (`@plan`) then execute with Atlas (`/start-work`).

## Quick commands

### Check that Oh-My-OpenCode plugin is installed

```bash
cat ~/.config/opencode/opencode.json | sed -n '1,120p'
```

You should see `"oh-my-opencode"` in the `plugin` list.

### Run one-shot coding (Sisyphus + ultrawork)

```bash
opencode run --agent sisyphus "ulw <your request>"
```

### Start interactive OpenCode (Sisyphus)

```bash
opencode --agent sisyphus
```

Inside OpenCode:

- Use `@plan "..."` to invoke Prometheus planning.
- Use `/start-work` to let Atlas execute the plan.

## Failure handling

- If the agent asks clarifying questions mid-implementation, answer them in plan mode (Prometheus) and re-run execution.
- If you need more determinism, re-run with `ulw` and a smaller, explicit request.
