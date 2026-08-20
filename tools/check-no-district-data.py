#!/usr/bin/env python3
"""Refuse to commit district-identifying values.

The package is a template. The moment someone fills in config/district-profile.md
with real domains, OU paths, and cabinet names and commits it, the repo becomes a
public map of exactly how the district is configured and who to target - and it
stays in git history even if reverted.

Usage:
  python3 tools/check-no-district-data.py --staged   # pre-commit hook
  python3 tools/check-no-district-data.py            # scan working tree
"""
import re
import subprocess
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROFILE = 'config/district-profile.md'

# Domains that legitimately appear: the fabricated example, and cited sources.
ALLOWED = re.compile(
    r'^(example\.k12\.st\.us|<[A-Z_]+>|.*\.?(google|googleblog|gstatic|googleapis)\.com'
    r'|support\.google\.com|knowledge\.workspace\.google\.com|workspaceupdates\.googleblog\.com'
    r'|cisa\.gov|k12six\.org|ic3\.gov|fbi\.gov|fincen\.gov|nist\.gov|datatracker\.ietf\.org'
    r'|github\.com|proofpoint\.com|group-ib\.com|bridewell\.com|elastic\.co|sekoia\.io'
    r'|cybereason\.com|malwarebytes\.com|bleepingcomputer\.com|abnormal\.ai|optery\.com'
    r'|acronis\.com|sedarasecurity\.com|k12cybersecure\.com|k12dive\.com|senki\.org'
    r'|wataugademocrat\.com|eccu\.edu|blog\.google|opensearch\.org|ghcr\.io'
    r'|imap\.gmail\.com|safebrowsing\.google\.com|vault\.google\.com|ncii\.ic3\.gov'
    r'|tips\.fbi\.gov|_spf\.google\.com)$', re.I)

DOMAIN = re.compile(r'\b([a-z0-9][a-z0-9-]*(?:\.[a-z0-9][a-z0-9-]*)+\.(?:us|org|net|com|edu|gov|io|k12))\b', re.I)


def staged_files():
    out = subprocess.run(['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
                         capture_output=True, text=True).stdout
    return [f for f in out.split('\n') if f.strip()]


def content(path, staged):
    if staged:
        r = subprocess.run(['git', 'show', f':{path}'], capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else ''
    p = ROOT / path
    return p.read_text() if p.exists() else ''


def check_profile(text):
    """The identity + bulk-sender tables must stay empty."""
    problems = []
    for line in text.split('\n'):
        if not line.strip().startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 2:
            continue
        label = cells[0]
        # Identity/scale rows: "| `<TOKEN>` | value | note |"
        if label.startswith('`<') and label.endswith('>`'):
            if cells[1] and cells[1] not in ('', '-'):
                problems.append(f'  {label} has been filled in: "{cells[1]}"')
        # OU map + bulk-sender rows: any non-empty cell past the first
        if label in ('Staff', 'Students', 'Finance-HR', 'Admins', 'Shared Devices',
                     'Service Accounts', 'SIS', 'Mass notification', 'LMS',
                     'Food service', 'Transportation', 'Copiers / scan-to-email',
                     'Helpdesk / ticketing', 'Survey tools', 'SMTP relay users'):
            filled = [c for c in cells[1:] if c and c not in ('☐', '☑', '-', '')]
            if filled:
                problems.append(f'  row "{label}" has been filled in: {filled}')
    return problems


def check_domains(path, text):
    hits = set()
    for m in DOMAIN.finditer(text):
        d = m.group(1)
        if not ALLOWED.match(d) and not d.lower().endswith(('.googleblog.com',)):
            hits.add(d)
    return [f'  {path}: real-looking domain "{d}"' for d in sorted(hits)]


def main():
    staged = '--staged' in sys.argv
    files = staged_files() if staged else [
        str(p.relative_to(ROOT)) for p in ROOT.rglob('*.md')
        if '.git' not in p.parts and 'site' not in p.parts and 'dist' not in p.parts]

    problems = []
    for f in files:
        text = content(f, staged)
        if not text:
            continue
        if f == PROFILE:
            problems += [f'{PROFILE}:{p}' for p in check_profile(text)]
            problems += check_domains(f, text)

    if problems:
        print('\n\033[1;31mBLOCKED: district-identifying data in a shared repo\033[0m\n')
        print('\n'.join(problems))
        print(f"""
This package is a public template. Filling in {PROFILE} and committing it
publishes your OU structure, mail domains, and vendor inventory - a targeting map
that survives in git history even if you revert it.

Keep real values OUT of this repo. Options:
  - keep the filled-in copy in an internal doc or a private repo
  - or:  git rm --cached {PROFILE} && echo '{PROFILE}' >> .gitignore

To override for a genuinely non-identifying change:
  git commit --no-verify
""")
        return 1

    print('district-data check: clean')
    return 0


if __name__ == '__main__':
    sys.exit(main())
