#!/usr/bin/env python3
"""Audit every link in the repo, three ways.

A. Repo integrity   - does each relative link point at a file that exists?
                      (this is what GitHub readers follow)
B. Anchor integrity - does each in-document #anchor match a real heading?
C. Site fidelity    - in the generated site, does each link that NAMES a file
                      resolve to that file's own section, not merely to some
                      section? This is the class of bug that shipped twice:
                      links that resolve cleanly but resolve somewhere wrong.

Usage: python3 tools/check-links.py [--quiet]
Exit 1 on any finding.
"""
import posixpath
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import md as mdlib  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / 'site' / 'index.html'
LINK = re.compile(r'\[([^\]]*)\]\(([^)\s]+)\)')
SKIP_DIRS = {'.git', 'site', 'dist', 'node_modules'}

quiet = '--quiet' in sys.argv
A, B, C = [], [], []
STATS = {'files': 0, 'links': 0, 'rel_links': 0, 'anchors': 0, 'site_checked': 0}


def md_files():
    for p in sorted(ROOT.rglob('*.md')):
        if not (set(p.relative_to(ROOT).parts) & SKIP_DIRS):
            yield p


def headings(text):
    return {mdlib.gh_slug(m.group(2))
            for m in re.finditer(r'^(#{1,6})\s+(.*)$', text, re.M)}


# ---------- A + B ----------
for p in md_files():
    STATS['files'] += 1
    rel = str(p.relative_to(ROOT))
    text = p.read_text()
    heads = headings(text)
    for label, href in LINK.findall(text):
        STATS['links'] += 1
        if href.startswith(('http://', 'https://', 'mailto:')):
            continue
        STATS['rel_links'] += 1
        frag = ''
        if '#' in href:
            href, frag = href.split('#', 1)
        if not href:                                    # same-doc anchor
            STATS['anchors'] += 1
            if frag and frag not in heads:
                B.append(f'{rel}: #{frag} matches no heading in this file')
            continue
        target = posixpath.normpath(posixpath.join(posixpath.dirname(rel), href))
        tp = ROOT / target
        if not tp.exists():
            A.append(f'{rel}: [{label}]({href}) -> {target} DOES NOT EXIST')
        elif frag and tp.suffix == '.md':
            if frag not in headings(tp.read_text()):
                B.append(f'{rel}: [{label}]({href}#{frag}) -> no such heading in {target}')

# ---------- C ----------
if SITE.exists():
    html = SITE.read_text()
    ids = set(re.findall(r'\sid="([^"]+)"', html))
    # map: repo path -> section id, recovered from the rendered source labels
    path_to_id = {}
    for m in re.finditer(r'<section class="doc" id="(doc-[^"]+)">\s*'
                         r'<div class="doc-meta"><span class="doc-src">([^<]+)</span>', html):
        path_to_id[m.group(2)] = m.group(1)

    sections = re.findall(r'<section class="doc" id="(doc-[^"]+)">(.*?)</section>', html, re.S)
    src_of = {sid: src for src, sid in path_to_id.items()}

    for sid, body in sections:
        src = src_of.get(sid)
        if not src:
            continue
        srcdir = posixpath.dirname(src)

        # What the markdown intends: label -> {every anchor that label may point to}
        expected = {}
        for label, href in LINK.findall((ROOT / src).read_text()):
            if href.startswith(('http', 'mailto:')):
                continue
            hp = href.split('#')[0]
            key = re.sub(r'[*`_]', '', label).strip()
            if not hp:                                    # same-doc anchor
                frag = href.split('#', 1)[1] if '#' in href else ''
                expected.setdefault(key, set()).add(f'{sid[4:]}-{frag}')
                continue
            target = posixpath.normpath(posixpath.join(srcdir, hp))
            want = path_to_id.get(target)
            if want:
                frag = href.split('#', 1)[1] if '#' in href else ''
                expected.setdefault(key, set()).add(
                    f'{want[4:]}-{frag}' if frag else want)

        # Check every RENDERED link against that. Checking the other direction
        # and matching by label picks got[0], which silently compares the wrong
        # occurrence when a label repeats - it produced a false clean here.
        seen = {}
        for href, label in re.findall(r'<a href="#([^"]*)"[^>]*>(.*?)</a>', body, re.S):
            key = re.sub(r'<[^>]+>', '', label).strip()
            seen.setdefault(key, set()).add(href)
            want = expected.get(key)
            if want:
                STATS['site_checked'] += 1
            if want and href not in want:
                C.append(f'{src}: "{key}" renders as #{href}, '
                         f'markdown expects {" or ".join("#" + w for w in sorted(want))}')

        for key, want in expected.items():
            if key not in seen:
                C.append(f'{src}: "{key}" -> {" / ".join(sorted(want))} '
                         f'was DROPPED (no link in output)')

    dangling = sorted({a for a in re.findall(r'<a href="#([^"]*)"', html) if a and a not in ids})
    for d in dangling:
        C.append(f'dangling anchor: #{d}')
    for sid, body in sections:
        n = len(re.findall(r'<a href="#%s"' % re.escape(sid), body))
        if n:
            C.append(f'{sid}: {n} self-referential link(s)')
else:
    C.append('site/index.html not built - run tools/build-site.py first')

for name, items in (('A. repo link integrity', A),
                    ('B. heading anchors', B),
                    ('C. site fidelity', C)):
    print(f'{name}: {len(items)} finding(s)')
    for i in items[:40] if not quiet else []:
        print('   ', i)
    if len(items) > 40:
        print(f'    ... and {len(items)-40} more')

print('\nexamined: %(files)d md files, %(links)d links (%(rel_links)d relative, '
      '%(anchors)d same-doc anchors), %(site_checked)d site link checks' % STATS)
total = len(A) + len(B) + len(C)
print(f'\nTOTAL: {total}')
sys.exit(1 if total else 0)
