#!/usr/bin/env bash
# Shared helpers for remediation scripts. Dry-run by default - always.
set -euo pipefail

R_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="${OUT_DIR:-$(cd "$R_DIR/.." && pwd)/out}"
LOG="$OUT_DIR/remediation-log.txt"
mkdir -p "$OUT_DIR"

COMMIT=0
for a in "$@"; do [[ "$a" == "--commit" ]] && COMMIT=1; done

banner() { echo; echo "=== $* ==="; }

need_gam() {
  command -v gam >/dev/null 2>&1 || {
    echo "ERROR: gam not found on PATH. Cannot remediate without it." >&2
    exit 127
  }
}

mode_notice() {
  if (( COMMIT )); then
    echo "*** MODE: COMMIT - changes WILL be made ***"
  else
    echo "MODE: DRY-RUN. Nothing will change. Pass --commit to apply."
  fi
}

# run <description> <command...>
run() {
  local desc="$1"; shift
  if (( COMMIT )); then
    echo "  APPLY: $desc"
    "$@" && logit "APPLIED: $desc" || { logit "FAILED: $desc"; return 1; }
  else
    echo "  would run: $desc"
    echo "             \$ $*"
  fi
}

logit() {
  printf '%s  %s  %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "${USER:-unknown}" "$*" >> "$LOG"
}

confirm() {
  (( COMMIT )) || return 0
  echo
  read -r -p "Type YES to proceed with real changes: " ans
  [[ "$ans" == "YES" ]] || { echo "Aborted."; exit 1; }
}
