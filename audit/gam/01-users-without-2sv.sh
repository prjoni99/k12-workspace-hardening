#!/usr/bin/env bash
# 01 - Accounts not enrolled in / not enforced for 2-Step Verification.
#
# Admin console equivalent:
#   Directory > Users > Manage columns > add "2-Step Verification Enrollment"
#                                            and "2-Step Verification Enforcement"
# Doc: docs/06-accounts-mfa-admins.md
#
# READ-ONLY.
#
# Expected non-compliant: /Service Accounts, /Shared Devices, and students
# (not enforced by design). ANY staff account in the enrolled=False list is a finding.

source "$(dirname "${BASH_SOURCE[0]}")/_lib.sh"
need_gam
banner "2SV enrollment and enforcement"

ALL="$OUT_DIR/$STAMP-2sv-all-users.csv"
NOT_ENROLLED="$OUT_DIR/$STAMP-2sv-not-enrolled.csv"
NOT_ENFORCED="$OUT_DIR/$STAMP-2sv-not-enforced.csv"

gam print users \
  fields primaryemail,name,suspended,orgunitpath,isenrolledin2sv,isenforcedin2sv \
  > "$ALL"

gam print users query "isEnrolledIn2Sv=False" \
  fields primaryemail,name,suspended,orgunitpath \
  > "$NOT_ENROLLED"

gam print users query "isEnforcedIn2Sv=False" \
  fields primaryemail,name,suspended,orgunitpath \
  > "$NOT_ENFORCED"

report "$ALL"          "all users (2SV state)"
report "$NOT_ENROLLED" "NOT enrolled in 2SV"
report "$NOT_ENFORCED" "NOT enforced for 2SV"

echo
echo "Triage: filter NOT-enrolled by orgunitpath. Staff OUs = findings."
echo "        Students, /Service Accounts, /Shared Devices = expected."
