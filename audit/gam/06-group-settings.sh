#!/usr/bin/env bash
# 06 - Group posting, joining, and external-member settings.
#
# Admin console equivalent: Directory > Groups > (each group) > Access settings
#   - one group at a time, which is why this script exists.
# Doc: docs/04-groups.md
#
# READ-ONLY.
#
# This is the control that decides whether one spoofed email reaches three people
# or twelve hundred.

source "$(dirname "${BASH_SOURCE[0]}")/_lib.sh"
need_gam
banner "Group settings"

GROUPS="$OUT_DIR/$STAMP-groups.csv"
RISKY="$OUT_DIR/$STAMP-groups-risky.csv"

gam print groups \
  settings \
  allfields \
  > "$GROUPS"

report "$GROUPS" "all groups with settings"

banner "Higher-risk groups"
head -1 "$GROUPS" > "$RISKY"
grep -Ei 'ANYONE_CAN_POST|allowExternalMembers.?,?True|true.*allowExternalMembers|ALL_IN_DOMAIN_CAN_POST' \
  "$GROUPS" >> "$RISKY" 2>/dev/null || true
report "$RISKY" "groups allowing wide/external posting"

echo
echo "Triage by member count - see the tier model in docs/04 section 3."
echo "  Tier 1: all-staff@, all-teachers@, everyone@  -> owners/managers only, moderated"
echo "  Tier 2: per-school staff lists                -> same"
echo "  Tier 3: principals@, finance@                 -> treat as Tier 1"
echo
echo "Also check NESTED groups: a hardened all-staff@ can still be fed by an open"
echo "child group. Check membership OF groups, not just members IN them."
echo
echo "KEEP THIS OUTPUT. It is your only rollback for a bulk permission change."
