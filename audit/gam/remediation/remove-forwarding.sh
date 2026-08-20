#!/usr/bin/env bash
# ⚠ MAKES CHANGES. Removes mail forwarding and forwarding addresses.
#
# Usage:
#   ./remove-forwarding.sh user@domain            # dry-run
#   ./remove-forwarding.sh user@domain --commit   # apply
#
# Run 02-forwarding-and-filters.sh FIRST and keep the output. Some forwarding is
# legitimate and users will ask what happened to it.
#
# NOTE: this removes the forwarding configuration. It does NOT delete filters -
# review those manually; a filter that forwards externally needs the same
# treatment but deleting filters in bulk is too blunt to automate safely.

source "$(dirname "${BASH_SOURCE[0]}")/_rlib.sh"

ACCOUNT="${1:-}"
[[ -z "$ACCOUNT" || "$ACCOUNT" == "--commit" ]] && {
  echo "Usage: $0 <user@domain> [--commit]" >&2; exit 2; }

banner "Remove forwarding: $ACCOUNT"
mode_notice
need_gam

SNAP="$OUT_DIR/$(date +%Y-%m-%d)-pre-fwd-${ACCOUNT//[^a-zA-Z0-9]/_}.txt"
{
  echo "=== forward ===";              gam user "$ACCOUNT" show forward 2>/dev/null || true
  echo "=== forwardingaddresses ==="; gam user "$ACCOUNT" show forwardingaddresses 2>/dev/null || true
  echo "=== filters ===";             gam user "$ACCOUNT" print filters 2>/dev/null || true
} | tee "$SNAP"
echo
echo "Snapshot -> $SNAP  (your rollback record)"

confirm
run "disable forwarding for $ACCOUNT" gam user "$ACCOUNT" forward off

echo
echo "Forwarding addresses are NOT auto-deleted - review the snapshot and remove"
echo "individually so you do not destroy a legitimate registered address:"
echo "  gam user $ACCOUNT delete forwardingaddress <address>"
echo
echo "Then review filters in the snapshot. A filter that forwards externally, or"
echo "that deletes/archives mail matching 'payroll' or 'direct deposit', is"
echo "attacker suppression - remove it and treat the account as compromised."
