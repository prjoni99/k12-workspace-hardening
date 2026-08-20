#!/usr/bin/env bash
# 03 - Mailbox delegates and send-as aliases.
#
# Admin console equivalent: NONE at scale (per-user only).
# Doc: playbooks/01-compromised-staff-account.md step 8
#
# READ-ONLY.
#
# A delegate is persistent mailbox access that survives a password reset and is
# invisible to the mailbox owner unless they go looking. A send-as alias lets an
# attacker send as another identity from a mailbox they control.

source "$(dirname "${BASH_SOURCE[0]}")/_lib.sh"
need_gam
banner "Delegates and send-as aliases"

DELEGATES="$OUT_DIR/$STAMP-delegates.csv"
SENDAS="$OUT_DIR/$STAMP-sendas.csv"

gam all users print delegates > "$DELEGATES"
gam all users print sendas    > "$SENDAS"

report "$DELEGATES" "mailbox delegates"
report "$SENDAS"    "send-as aliases"

echo
echo "Findings to look for:"
echo "  - delegates on Finance-HR mailboxes that are not a known assistant relationship"
echo "  - delegates granted TO suspended or departed accounts"
echo "  - send-as aliases on domains the district does not own"
echo "  - any delegate relationship neither party can explain"
