#!/usr/bin/env python3
"""Publish a batch of pre-generated media items for internal seeding."""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PUBLISH_SCRIPT = SCRIPT_DIR / "publish_cycle.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-jsonl", required=True, help="Path to JSONL seed items.")
    parser.add_argument("--max-items", type=int, default=100)
    parser.add_argument("--delay-seconds", type=float, default=0.4)
    parser.add_argument("--quality-threshold", type=float, default=6.0)
    parser.add_argument("--skip-quality-check", action="store_true")
    parser.add_argument("--stop-on-error", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def normalize_tags(raw_tags) -> str:
    if raw_tags is None:
        return ""
    if isinstance(raw_tags, list):
        return ",".join(str(tag).strip() for tag in raw_tags if str(tag).strip())
    if isinstance(raw_tags, str):
        return raw_tags
    return ""


def load_items(path: Path) -> list[dict]:
    items: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for idx, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                parsed = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"line {idx}: invalid JSON: {exc}") from exc
            if not isinstance(parsed, dict):
                raise ValueError(f"line {idx}: expected object")
            items.append(parsed)
    return items


def build_command(item: dict, args: argparse.Namespace) -> list[str]:
    media_url = str(item.get("media_url", "")).strip()
    prompt = str(item.get("prompt", "")).strip()
    agent_profile = str(item.get("agent_profile", "")).strip()
    theme = str(item.get("theme", "")).strip()
    media_type = str(item.get("type", "image")).strip() or "image"
    tags = normalize_tags(item.get("tags"))
    model_id = str(item.get("model_id", "")).strip()
    generator = str(item.get("generator", "openclaw-agent")).strip() or "openclaw-agent"

    if not media_url or not prompt or not agent_profile or not theme:
        raise ValueError("missing required keys: media_url, prompt, agent_profile, theme")
    if media_type not in {"image", "video"}:
        raise ValueError(f"invalid type: {media_type}")

    cmd = [
        sys.executable,
        str(PUBLISH_SCRIPT),
        "--media-url",
        media_url,
        "--type",
        media_type,
        "--prompt",
        prompt,
        "--agent-profile",
        agent_profile,
        "--theme",
        theme,
        "--tags",
        tags,
        "--quality-threshold",
        str(args.quality_threshold),
    ]

    if model_id:
        cmd.extend(["--model-id", model_id])
    if generator:
        cmd.extend(["--generator", generator])
    if args.skip_quality_check:
        cmd.append("--skip-quality-check")

    return cmd


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_jsonl).expanduser().resolve()
    if not input_path.exists():
        print(f"ERROR: seed file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        items = load_items(input_path)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.max_items <= 0:
        print("ERROR: --max-items must be > 0", file=sys.stderr)
        return 1

    selected = items[: args.max_items]

    summary = {
        "requested": len(selected),
        "success": 0,
        "quality_rejected": 0,
        "failed": 0,
        "results": [],
    }

    for index, item in enumerate(selected, start=1):
        try:
            cmd = build_command(item, args)
        except ValueError as exc:
            summary["failed"] += 1
            summary["results"].append(
                {
                    "index": index,
                    "status": "invalid_item",
                    "error": str(exc),
                }
            )
            if args.stop_on_error:
                break
            continue

        if args.dry_run:
            summary["results"].append(
                {
                    "index": index,
                    "status": "dry_run",
                    "command": cmd,
                }
            )
            continue

        proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
        if proc.returncode == 0:
            summary["success"] += 1
            output = proc.stdout.strip()
            parsed_output = None
            if output:
                try:
                    parsed_output = json.loads(output)
                except json.JSONDecodeError:
                    parsed_output = output
            summary["results"].append(
                {
                    "index": index,
                    "status": "submitted",
                    "response": parsed_output,
                }
            )
        elif proc.returncode == 2:
            summary["quality_rejected"] += 1
            summary["results"].append(
                {
                    "index": index,
                    "status": "quality_rejected",
                    "error": proc.stderr.strip(),
                }
            )
            if args.stop_on_error:
                break
        else:
            summary["failed"] += 1
            summary["results"].append(
                {
                    "index": index,
                    "status": "failed",
                    "error": proc.stderr.strip(),
                }
            )
            if args.stop_on_error:
                break

        if args.delay_seconds > 0:
            time.sleep(args.delay_seconds)

    print(json.dumps(summary, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
