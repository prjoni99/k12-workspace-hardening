#!/usr/bin/env bash
# ⚠ MAKES CHANGES TO MANY ACCOUNTS. Resets passwords from a list.
#
# Usage:
#   ./bulk-reset-passwords.sh accounts.txt            # dry-run
#   ./bulk-reset-passwords.sh accounts.txt --commit   # apply
#
# accounts.txt: one email address per line.
#
# For mass student compromise - playbooks/02 section 5.
# COORDINATE WITH SCHOOLS BEFORE RUNNING. The front office absorbs the volume of
# students who cannot sign in, and they need warning, not a surprise.
#
# NOT reversible.

source "$(dirname "${BASH_SOURCE[0]}")/_rlib.sh"

LIST="${1:-}"
[[ -z "$LIST" || "$LIST" == "--commit" ]] && {
  echo "Usage: $0 <accounts.txt> [--commit]" >&2; exit 2; }
[[ -f "$LIST" ]] || { echo "ERROR: $LIST not found" >&2; exit 2; }

COUNT=$(grep -cve '^\s*$' "$LIST")

banner "Bulk password reset: $COUNT accounts from $LIST"
mode_notice
need_gam
echo
echo "Accounts (first 20):"
grep -ve '^\s*$' "$LIST" | head -20 | sed 's/^/  /'
(( COUNT > 20 )) && echo "  ... and $((COUNT - 20)) more"

echo
echo "Checklist before committing:"
echo "  [ ] Schools notified - front offices ready for the sign-in volume"
echo "  [ ] Password delivery method agreed (in person, through the school)"
echo "  [ ] Not during state testing or the first week of school"
echo "  [ ] The root cause is understood - otherwise this recurs"

confirm

while read -r acct; do
  [[ -z "$acct" ]] && continue
  run "reset password for $acct" \
    gam update user "$acct" password random changepassword on
done < "$LIST"

echo
echo "Reset complete. Deliver new passwords IN PERSON through the school."
echo "Never by email - if the mailbox is compromised you are handing the"
echo "credential to the attacker."
