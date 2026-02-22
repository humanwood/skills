#!/bin/bash
# 1-SEC Automated Install & Configure Script
# For use by AI agents deploying security on VPS instances.
#
# Usage:
#   bash install-and-configure.sh                    # Default: safe preset, dry-run
#   bash install-and-configure.sh --preset vps-agent # AI agent host
#   bash install-and-configure.sh --preset balanced --live  # Production, enforcement live
#
# Environment variables (optional):
#   GEMINI_API_KEY      — Gemini API key for AI analysis
#   ONESEC_API_KEY      — API key to secure the REST endpoint
#   ONESEC_WEBHOOK_URL  — Webhook URL for alert notifications

set -euo pipefail

PRESET="${1:-safe}"
LIVE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --preset)   PRESET="$2"; shift 2 ;;
    --live)     LIVE=true; shift ;;
    *)          shift ;;
  esac
done

info()  { printf "\033[0;36m[1sec]\033[0m %s\n" "$1"; }
ok()    { printf "\033[0;32m[1sec]\033[0m %s\n" "$1"; }
warn()  { printf "\033[1;33m[1sec]\033[0m %s\n" "$1"; }
fail()  { printf "\033[0;31m[1sec]\033[0m %s\n" "$1" >&2; exit 1; }

# Step 1: Install
if command -v 1sec >/dev/null 2>&1; then
  ok "1sec already installed: $(1sec version 2>/dev/null | head -1)"
else
  info "Installing 1-SEC..."
  curl -fsSL https://1-sec.dev/get | sh
  command -v 1sec >/dev/null 2>&1 || fail "Installation failed — 1sec not found in PATH"
  ok "1-SEC installed: $(1sec version 2>/dev/null | head -1)"
fi

# Step 2: Non-interactive setup
info "Running setup (non-interactive)..."
1sec setup --non-interactive

# Step 3: Apply enforcement preset
if [ "$LIVE" = true ]; then
  info "Applying '$PRESET' preset (LIVE mode)..."
  1sec enforce preset "$PRESET"
else
  info "Applying '$PRESET' preset (dry-run mode)..."
  1sec enforce preset "$PRESET" --dry-run
fi

# Step 4: Validate
info "Running pre-flight checks..."
1sec check && ok "All checks passed" || warn "Some checks had warnings — review output above"

# Step 5: Summary
ok "1-SEC is configured and ready."
echo ""
echo "  Preset:    $PRESET"
echo "  Dry-run:   $([ "$LIVE" = true ] && echo 'OFF (live)' || echo 'ON (safe)')"
echo "  AI keys:   $([ -n "${GEMINI_API_KEY:-}" ] && echo 'configured' || echo 'not set (optional)')"
echo ""
echo "  Next steps:"
echo "    1sec up                    # Start the engine"
echo "    1sec dashboard             # Real-time monitoring"
echo "    1sec enforce dry-run off   # Go live when ready"
echo ""
