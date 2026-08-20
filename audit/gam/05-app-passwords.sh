#!/usr/bin/env bash
# 05 - Application-specific passwords (ASPs).
#
# Admin console equivalent: per-user only (Directory > Users > user > Security).
# Doc: playbooks/01-compromised-staff-account.md step 6
#
# READ-ONLY.
#
# ASPs bypass 2SV by design. Each one is a standing credential that survives a
# password reset. If POP/IMAP is off per docs/01 section 5, most of these should
# not exist - their presence usually means a legacy client nobody migrated.

source "$(dirname "${BASH_SOURCE[0]}")/_lib.sh"
need_gam
banner "Application-specific passwords"

ASPS="$OUT_DIR/$STAMP-app-passwords.csv"
gam all users print asps > "$ASPS"
report "$ASPS" "app-specific passwords"

echo
echo "Every ASP should have a known owner and a known purpose."
echo "Document legitimate exceptions (e.g. the parsedmarc IMAP account, docs/09"
echo "section 7) so a future sweep does not revoke them blindly."
echo "Revoke the rest: audit/gam/remediation/revoke-tokens.sh"
