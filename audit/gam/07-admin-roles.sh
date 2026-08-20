#!/usr/bin/env bash
# 07 - Administrator role assignments.
#
# Admin console equivalent: Account > Admin roles
# Doc: docs/06-accounts-mfa-admins.md section 5
#
# READ-ONLY.
#
# Target: 2-4 super admins. Expect to find more. Vendor accounts left over from
# completed projects are the most common orphan - check for those specifically.

source "$(dirname "${BASH_SOURCE[0]}")/_lib.sh"
need_gam
banner "Admin role assignments"

ADMINS="$OUT_DIR/$STAMP-admins.csv"
ROLES="$OUT_DIR/$STAMP-admin-roles.csv"

gam print admins > "$ADMINS"
gam print adminroles > "$ROLES" 2>/dev/null || echo "  (adminroles unsupported in this GAM build - skipped)"

report "$ADMINS" "admin role assignments"
[[ -f "$ROLES" ]] && report "$ROLES" "role definitions"

banner "Super admin count"
grep -ci '_SEED_ADMIN_ROLE\|super' "$ADMINS" 2>/dev/null || echo "  (grep found no super-admin marker - inspect the CSV directly)"

echo
echo "For each super admin, confirm: is this a dedicated admin account, or someone's"
echo "daily driver? A super admin account that reads email can be phished."
echo "See docs/06 section 5 for the delegated-role alternatives."
