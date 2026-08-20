#!/usr/bin/env bash
# 02 - External forwarding, forwarding addresses, and mail filters.
#
# Admin console equivalent: NONE at scale. This is the single strongest reason
# to have GAM in a district. The console cannot answer "who is forwarding
# externally" across 1,200 mailboxes.
#
# Doc: docs/01-gmail.md section 5, playbooks/01-compromised-staff-account.md
#
# READ-ONLY.
#
# Forwarding is the #1 attacker persistence mechanism - it survives a password
# reset. Filters are the same thing wearing a different hat, and are missed more
# often. Run this MONTHLY at minimum.

source "$(dirname "${BASH_SOURCE[0]}")/_lib.sh"
need_gam
banner "Forwarding, forwarding addresses, and filters"

FWD="$OUT_DIR/$STAMP-forwarding.csv"
FWD_ADDR="$OUT_DIR/$STAMP-forwarding-addresses.csv"
FILTERS="$OUT_DIR/$STAMP-filters.csv"

# Active forwarding setting per user
gam all users print forwards > "$FWD" 2>/dev/null \
  || gam all users show forward > "$FWD"

# Registered forwarding destinations (may exist without forwarding being enabled -
# an attacker pre-registers, verifies, then enables later)
gam all users print forwardingaddresses > "$FWD_ADDR"

# Filters - includes forward-to and delete/archive suppression rules
gam all users print filters > "$FILTERS"

report "$FWD"      "forwarding settings"
report "$FWD_ADDR" "forwarding addresses"
report "$FILTERS"  "mail filters"

banner "Quick triage"
echo "External forwarding destinations (excluding <PRIMARY_DOMAIN>):"
grep -iv '<PRIMARY_DOMAIN>' "$FWD_ADDR" 2>/dev/null | tail -n +2 | head -50 \
  || echo "  (edit this script to substitute your real domain)"

echo
echo "Filters containing suppression keywords - attacker pattern, not user preference:"
grep -Ei 'payroll|invoice|direct.?deposit|password|security|bank' "$FILTERS" 2>/dev/null \
  | head -50 || echo "  none matched"

echo
echo "A filter that forwards externally, or that deletes/archives mail matching"
echo "'payroll' or 'direct deposit', is attacker suppression. Investigate each."
