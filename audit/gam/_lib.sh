#!/usr/bin/env bash
# Shared helpers for the read-only GAM audit scripts.
set -euo pipefail

OUT_DIR="${OUT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/out}"
STAMP="$(date +%Y-%m-%d)"
mkdir -p "$OUT_DIR"

need_gam() {
  command -v gam >/dev/null 2>&1 || {
    echo "ERROR: gam not found on PATH." >&2
    echo "  Install GAM7 (https://github.com/GAM-team/GAM) or GAMADV-XTD3," >&2
    echo "  or work the Admin console path in this script's header manually." >&2
    exit 127
  }
}

# report <file> <label> - print a row count so an empty result is distinguishable
# from a silently failed command. Those look identical otherwise.
report() {
  local f="$1" label="$2" n=0
  [[ -f "$f" ]] && n=$(( $(wc -l < "$f") - 1 ))
  (( n < 0 )) && n=0
  printf '  %-38s %6s rows  -> %s\n' "$label" "$n" "$f"
  if (( n == 0 )); then
    echo "    NOTE: zero rows. Confirm this means 'no findings' and not 'command returned nothing'."
  fi
}

banner() { echo; echo "=== $* ==="; }
