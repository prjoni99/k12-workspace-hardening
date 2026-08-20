#!/usr/bin/env bash
# 04 - OAuth tokens granted by users to third-party applications.
#
# Admin console equivalent:
#   Security > Access and data control > API controls > App access control
#   (console is authoritative; this gives you a diffable per-user export)
# Doc: docs/07-oauth-app-control.md
#
# READ-ONLY.
#
# NOTE: domain-wide delegation is NOT covered here. GAM visibility is limited and
# the console is authoritative. Review DWD at:
#   Security > Access and data control > API controls > Manage Domain Wide Delegation
# DWD is the largest blast radius in the tenant - see docs/07 section 6.

source "$(dirname "${BASH_SOURCE[0]}")/_lib.sh"
need_gam
banner "OAuth tokens"

TOKENS="$OUT_DIR/$STAMP-oauth-tokens.csv"
BY_APP="$OUT_DIR/$STAMP-oauth-by-app.txt"

gam all users print tokens > "$TOKENS"
report "$TOKENS" "OAuth token grants"

banner "Grants per application (highest user count first)"
# Column layout varies between GAM builds; find the client/app column by header name.
awk -F, 'NR==1{
           for(i=1;i<=NF;i++){
             h=tolower($i)
             if(h ~ /displaytext|clientid|application/){c=i; break}
           }
           if(!c){c=3}
           next
         }
         {print $c}' "$TOKENS" \
  | sort | uniq -c | sort -rn | tee "$BY_APP" | head -40

echo
echo "Full ranking -> $BY_APP"
echo
echo "Triage: high user count on an unrecognized app is the priority. Then check"
echo "scopes against necessity - a flashcard app with full Drive access is asking"
echo "for far more than it needs. See docs/07 section 5."
echo
echo "REMINDER: review domain-wide delegation in the console. It is not in this export."
