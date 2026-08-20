#!/usr/bin/env bash
# 08 - Service on/off state per organizational unit.
#
# Admin console equivalent: Apps > (each service) > (each OU) - one at a time.
# Doc: docs/05-other-services.md section 7
#
# READ-ONLY.
#
# Every service that is ON is a service an attacker can use to generate an
# authentically-signed notification email to your users (threat T7).

source "$(dirname "${BASH_SOURCE[0]}")/_lib.sh"
need_gam
banner "OU structure and service state"

ORGS="$OUT_DIR/$STAMP-orgunits.csv"
SERVICES="$OUT_DIR/$STAMP-ou-service-state.txt"

gam print orgs > "$ORGS"
report "$ORGS" "organizational units"

: > "$SERVICES"
{
  echo "# Service state per OU - generated $STAMP"
  echo "# Verify against Admin console > Apps; GAM coverage of service state varies by build."
  echo
  gam print orgs 2>/dev/null | tail -n +2 | cut -d, -f1 | while read -r ou; do
    [[ -z "$ou" ]] && continue
    echo "## OU: $ou"
    gam info org "$ou" 2>/dev/null || echo "  (no detail available)"
    echo
  done
} >> "$SERVICES"

echo "  OU service detail -> $SERVICES"
echo
echo "GAM's per-OU service reporting is incomplete in some builds. Treat this as a"
echo "starting point and confirm the sweep list against Admin console > Apps >"
echo "Additional Google services, per OU."
echo
echo "Candidates to turn OFF where unused - see docs/05 section 7:"
echo "  AppSheet, Blogger, Google Ads, consumer Groups, Photos (students),"
echo "  and the long tail under Additional Google services."
