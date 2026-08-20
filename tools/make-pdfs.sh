#!/usr/bin/env bash
# Render the print editions to PDF with headless Chrome.
# Usage: ./tools/make-pdfs.sh
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[[ -x "$CHROME" ]] || CHROME="/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
[[ -x "$CHROME" ]] || { echo "No Chrome/Brave found. Open site/print-*.html and use Print > Save as PDF." >&2; exit 1; }

mkdir -p dist
render() {  # render <mode> <output-name>
  local mode="$1" out="dist/$2"
  python3 tools/build-print.py "$mode" >/dev/null
  "$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
    --virtual-time-budget=20000 \
    --print-to-pdf="$PWD/$out" "file://$PWD/site/print-$mode.html" 2>/dev/null
  printf '  %-46s %6s KB\n' "$out" "$(( $(stat -f%z "$out") / 1024 ))"
}

echo "Rendering PDFs..."
render exec "K-12-Workspace-Hardening-Exec-Summary.pdf"
render full "K-12-Workspace-Hardening-Full-Package.pdf"
echo "Done."
