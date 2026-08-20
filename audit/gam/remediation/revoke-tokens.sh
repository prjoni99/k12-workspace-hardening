#!/usr/bin/env bash
# ⚠ MAKES CHANGES. Revokes OAuth tokens and app-specific passwords.
#
# Usage:
#   ./revoke-tokens.sh user@domain            # dry-run
#   ./revoke-tokens.sh user@domain --commit   # apply
#
# Use during playbooks/01 step 5, and at staff offboarding.
# NOT reversible - users must re-consent to legitimate apps.

source "$(dirname "${BASH_SOURCE[0]}")/_rlib.sh"

ACCOUNT="${1:-}"
[[ -z "$ACCOUNT" || "$ACCOUNT" == "--commit" ]] && {
  echo "Usage: $0 <user@domain> [--commit]" >&2; exit 2; }

banner "Revoke tokens and app passwords: $ACCOUNT"
mode_notice
need_gam

echo
echo "Current state (recorded before change):"
SNAP="$OUT_DIR/$(date +%Y-%m-%d)-pre-revoke-${ACCOUNT//[^a-zA-Z0-9]/_}.txt"
{
  echo "=== tokens ==="; gam user "$ACCOUNT" show tokens 2>/dev/null || true
  echo "=== asps ===";   gam user "$ACCOUNT" show asps   2>/dev/null || true
} | tee "$SNAP"
echo
echo "Snapshot -> $SNAP  (this is your only record of what was revoked)"

confirm
run "revoke all OAuth tokens for $ACCOUNT" gam user "$ACCOUNT" delete tokens
run "revoke all app passwords for $ACCOUNT" gam user "$ACCOUNT" delete asps all

echo
echo "Verify: gam user $ACCOUNT show tokens   # expect empty"
echo "        gam user $ACCOUNT show asps     # expect empty"
