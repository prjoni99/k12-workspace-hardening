#!/usr/bin/env bash
# Point git at the repo's tracked hooks. Run once per clone.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
git config core.hooksPath tools/hooks
echo "hooks installed (core.hooksPath = tools/hooks)"
echo "pre-commit will now block district-identifying data. Bypass with --no-verify."
