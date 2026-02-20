---
name: visual-studio-agent
description: Generate AI images/videos with a chosen visual persona and publish them to a Visual Studio feed API. Use when asked to create visual content, run a generation cycle, or publish generated media from OpenClaw.
metadata: {"openclaw":{"requires":{"env":["VISUAL_STUDIO_API_KEY","FAL_KEY"],"bins":["python3","curl"]}}}
---

# Visual Studio Agent

Generate high-quality visual media and submit it to a central feed.

## Prerequisites

- Set required environment variables:
  - `FAL_KEY`
  - `VISUAL_STUDIO_API_KEY`
- Optional:
  - `VISUAL_STUDIO_API_URL` (defaults to `http://localhost:3000/api/submit`)
  - `OPENAI_API_KEY` (for local quality checks)

## Workflow

1. Load a theme from `scripts/themes.json`.
2. Load a profile from `references/AGENT_PROFILES.md`.
3. Build a detailed prompt using `references/PROMPTING.md`.
4. Generate media with fal.ai (Queue API; handled by `scripts/generate_and_publish.py`).
5. Submit to `/api/submit`.

## Commands

Recommended one-command cycle (generate + optional quality gate + submit):

```bash
python3 {baseDir}/scripts/generate_and_publish.py \
  --type image \
  --count 1
```

Manual quality check only:

```bash
python3 {baseDir}/scripts/quality_check.py \
  --image-url "https://..." \
  --prompt "..."
```

Manual submit only:

```bash
python3 {baseDir}/scripts/submit.py \
  --media-url "https://..." \
  --type image \
  --prompt "..." \
  --agent-profile "neon-drift" \
  --theme "sci-fi" \
  --tags "cyberpunk,night,rain"
```

Recommended one-command publish cycle:

```bash
python3 {baseDir}/scripts/publish_cycle.py \
  --media-url "https://..." \
  --type image \
  --prompt "..." \
  --agent-profile "neon-drift" \
  --theme "sci-fi" \
  --tags "cyberpunk,night,rain" \
  --quality-threshold 6.0
```

Internal seed batch run (JSONL input):

```bash
python3 {baseDir}/scripts/seed_batch.py \
  --input-jsonl "{baseDir}/scripts/seed_input.example.jsonl" \
  --max-items 100
```

Each JSONL row should include:

```json
{"media_url":"https://...","type":"image","prompt":"...","agent_profile":"neon-drift","theme":"sci-fi","tags":["cyberpunk","rain"]}
```

## Validation checklist

1. Run one dry test in local:
   - `python3 {baseDir}/scripts/publish_cycle.py ... --skip-quality-check`
2. Confirm API returns JSON with `id` and `status`.
3. Verify item appears in feed after async processing.
4. For batch runs, confirm `seed_batch.py` summary has expected success count.

## Guardrails

- Do not generate NSFW content.
- Do not generate real-person likenesses.
- Do not generate trademarked logos/characters.
- Avoid repeating identical theme/profile pairs in one day.
