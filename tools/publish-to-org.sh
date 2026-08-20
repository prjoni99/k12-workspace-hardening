#!/usr/bin/env bash
# Publish this package to a different GitHub account or organization.
#
# Usage:  ./tools/publish-to-org.sh <owner>/<repo> [--private]
# e.g.    ./tools/publish-to-org.sh MooreCountySchools/workspace-hardening
#
# Run `gh auth switch` (or `gh auth login`) FIRST so the active account is the
# one that should own the repo. This script never handles credentials itself.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

TARGET="${1:-}"
VIS="--public"
[[ "${2:-}" == "--private" ]] && VIS="--private"
[[ -n "$TARGET" ]] || { echo "Usage: $0 <owner>/<repo> [--private]" >&2; exit 2; }

OWNER="${TARGET%%/*}"
ACTIVE=$(gh api user --jq .login 2>/dev/null || echo "")
[[ -n "$ACTIVE" ]] || { echo "Not authenticated. Run: gh auth login" >&2; exit 1; }

echo "Active GitHub account : $ACTIVE"
echo "Publishing to         : $TARGET ($VIS)"
echo

# 1. Refuse to publish district-identifying data.
echo "Checking for district-identifying data..."
python3 tools/check-no-district-data.py || {
  echo; echo "Aborted. Resolve the findings above before publishing." >&2; exit 1; }

# 2. Confirm the account can write to the owner.
if [[ "$OWNER" != "$ACTIVE" ]]; then
  gh api "orgs/$OWNER" >/dev/null 2>&1 || {
    echo "ERROR: '$OWNER' is not visible to $ACTIVE." >&2
    echo "  If it is an org, you need membership plus 'read:org' scope:" >&2
    echo "    gh auth refresh -s read:org,repo,workflow" >&2
    echo "  If it is another personal account, run: gh auth switch" >&2
    exit 1; }
fi

# 3. Rebuild the generated editions so they match the markdown.
echo "Rebuilding web edition..."
python3 tools/build-site.py
if [[ "${SKIP_PDF:-}" != "1" ]]; then
  ./tools/make-pdfs.sh || echo "  (PDF render skipped - Chrome not found)"
fi

# 4. Create the repo if it does not exist.
if gh repo view "$TARGET" >/dev/null 2>&1; then
  echo "Repo exists; pushing to it."
else
  gh repo create "$TARGET" $VIS \
    --description "Anti-phishing hardening package for K-12 districts on Google Workspace for Education - console paths, per-OU values, rollout phases, and incident playbooks."
fi

# 5. Point a remote at it and push main.
git remote remove upstream-org 2>/dev/null || true
git remote add upstream-org "https://github.com/$TARGET.git"
git add -A
git diff --cached --quiet || git commit -q -m "chore: rebuild generated editions before publish"
git push -u upstream-org main

# 6. Deploy the site branch.
if [[ "$VIS" == "--public" ]]; then
  TMP=$(mktemp -d)
  cp site/index.html "$TMP/"
  cp dist/*.pdf "$TMP/" 2>/dev/null || true
  touch "$TMP/.nojekyll"
  git -C "$TMP" init -q && git -C "$TMP" checkout -q -b gh-pages
  git -C "$TMP" add -A
  git -C "$TMP" commit -q -m "deploy: web edition and PDFs (generated - do not edit here)"
  git -C "$TMP" remote add origin "https://github.com/$TARGET.git"
  git -C "$TMP" push -q --force origin gh-pages
  rm -rf "$TMP"
  gh api -X POST "repos/$TARGET/pages" -f 'source[branch]=gh-pages' -f 'source[path]=/' >/dev/null 2>&1 || true
  echo
  echo "Pages: $(gh api "repos/$TARGET/pages" --jq .html_url 2>/dev/null || echo 'enable manually in Settings > Pages')"
else
  echo "Private repo - skipping GitHub Pages (Pages on private repos needs a paid plan)."
fi

echo
echo "Done: https://github.com/$TARGET"
