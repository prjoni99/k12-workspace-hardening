#!/usr/bin/env bash
# ⚠ MAKES CHANGES. Locks a group to internal, owner-post, moderated.
#
# Usage:
#   ./lockdown-group.sh all-staff@domain            # dry-run
#   ./lockdown-group.sh all-staff@domain --commit   # apply
#
# Applies the docs/04 section 3 Tier 1 profile.
# Run 06-group-settings.sh FIRST - its output is your only restore point.

source "$(dirname "${BASH_SOURCE[0]}")/_rlib.sh"

GROUP="${1:-}"
[[ -z "$GROUP" || "$GROUP" == "--commit" ]] && {
  echo "Usage: $0 <group@domain> [--commit]" >&2; exit 2; }

banner "Lock down group: $GROUP"
mode_notice
need_gam

SNAP="$OUT_DIR/$(date +%Y-%m-%d)-pre-lockdown-${GROUP//[^a-zA-Z0-9]/_}.txt"
gam info group "$GROUP" 2>/dev/null | tee "$SNAP"
echo
echo "Snapshot -> $SNAP  (RESTORE POINT - do not lose this)"

confirm
run "set $GROUP to Tier 1 profile" gam update group "$GROUP" \
  whoCanPostMessage ALL_OWNERS_CAN_POST \
  whoCanJoin INVITED_CAN_JOIN \
  whoCanViewMembership ALL_MANAGERS_CAN_VIEW \
  allowExternalMembers false \
  messageModerationLevel MODERATE_NON_MEMBERS

echo
echo "Verify: gam info group $GROUP"
echo
echo "Before announcing: confirm the authorized senders can still post."
echo "See docs/04 section 4 for the authorized-senders pattern and the emergency"
echo "path for weather and safety notices - those cannot wait on moderation."
