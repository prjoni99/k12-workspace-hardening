#!/usr/bin/env bash
# Run every read-only audit script. Safe to run any time.
#
# Output -> audit/gam/out/  (gitignored - contains PII, do not commit)
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

echo "=============================================="
echo " GAM read-only audit suite"
echo " $(date)"
echo "=============================================="

FAILED=()
for s in 0*.sh; do
  [[ "$s" == "run-all.sh" ]] && continue
  echo
  echo "----------------------------------------------"
  echo " RUNNING: $s"
  echo "----------------------------------------------"
  if ! bash "$s"; then
    echo "  !! $s exited non-zero"
    FAILED+=("$s")
  fi
done

echo
echo "=============================================="
if (( ${#FAILED[@]} )); then
  echo " COMPLETED WITH FAILURES: ${FAILED[*]}"
  echo " GAM syntax varies between GAM7 and GAMADV-XTD3 and across versions."
  echo " Check the failing script's commands against your GAM build."
else
  echo " All scripts completed."
fi
echo " Output: $(pwd)/out/"
echo
echo " Output contains PII. Do not commit. Do not email."
echo " Diff against last month's run - the diff is the useful part."
echo "=============================================="
