#!/usr/bin/env python3
"""Check for OpenClaw updates by comparing installed vs npm registry version."""

import subprocess
import json
import sys
import re


def get_installed_version():
    """Get currently installed openclaw version."""
    try:
        result = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except Exception as e:
        return None


def get_registry_versions():
    """Get all available versions from npm registry."""
    try:
        result = subprocess.run(
            ["npm", "show", "openclaw", "versions", "--json"],
            capture_output=True, text=True, timeout=15
        )
        versions = json.loads(result.stdout)
        if isinstance(versions, str):
            versions = [versions]
        return versions
    except Exception:
        return None


def parse_version(v):
    """Parse version string into comparable tuple. Handles YYYY.M.DD[-N] format."""
    match = re.match(r"(\d+)\.(\d+)\.(\d+)(?:-(\d+))?", v)
    if not match:
        return (0, 0, 0, 0)
    major, minor, patch = int(match.group(1)), int(match.group(2)), int(match.group(3))
    hotfix = int(match.group(4)) if match.group(4) else 0
    return (major, minor, patch, hotfix)


def get_latest_version(versions):
    """Find the latest version from a list."""
    if not versions:
        return None
    return max(versions, key=parse_version)


def get_changelog_url(version):
    """Generate GitHub release URL for a version."""
    # Strip hotfix suffix for release tag
    base = re.sub(r"-\d+$", "", version)
    return f"https://github.com/openclaw/openclaw/releases/tag/v{base}"


def main():
    output_format = "text"
    if "--format" in sys.argv:
        idx = sys.argv.index("--format")
        if idx + 1 < len(sys.argv):
            output_format = sys.argv[idx + 1]

    installed = get_installed_version()
    if not installed:
        if output_format == "json":
            print(json.dumps({"error": "Could not determine installed version"}))
        else:
            print("Error: Could not determine installed openclaw version")
        sys.exit(1)

    versions = get_registry_versions()
    if not versions:
        if output_format == "json":
            print(json.dumps({"error": "Could not fetch versions from npm registry"}))
        else:
            print("Error: Could not fetch versions from npm registry")
        sys.exit(1)

    latest = get_latest_version(versions)
    is_current = parse_version(installed) >= parse_version(latest)

    # Find versions newer than installed
    installed_tuple = parse_version(installed)
    newer = [v for v in versions if parse_version(v) > installed_tuple]
    newer.sort(key=parse_version)

    result = {
        "installed": installed,
        "latest": latest,
        "up_to_date": is_current,
        "newer_versions": newer,
        "changelog_url": get_changelog_url(latest),
        "update_command": f"npm i -g openclaw@{latest}"
    }

    if output_format == "json":
        print(json.dumps(result, indent=2))
    else:
        if is_current:
            print(f"✅ OpenClaw is up to date: {installed}")
        else:
            print(f"⬆️  Update available: {installed} → {latest}")
            print(f"   Versions behind: {len(newer)}")
            if len(newer) <= 5:
                for v in newer:
                    print(f"   • {v}")
            else:
                for v in newer[-5:]:
                    print(f"   • {v}")
                print(f"   ... and {len(newer) - 5} more")
            print(f"   Release: {get_changelog_url(latest)}")
            print(f"   Update:  {result['update_command']}")


if __name__ == "__main__":
    main()
