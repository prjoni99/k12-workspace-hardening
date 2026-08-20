#!/usr/bin/env python3
"""Build print-optimised HTML for PDF export.

Usage:  python3 tools/build-print.py exec|full  [out.html]

Separate from build-site.py because print wants different things: a cover page,
no navigation chrome, a light-only palette, and page-break control. Rendered to
PDF by tools/make-pdfs.sh via headless Chrome.
"""
import html
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import md as mdlib  # noqa: E402
from importlib import import_module  # noqa: E402

site = import_module('build-site'.replace('-', '_')) if False else None
ROOT = pathlib.Path(__file__).resolve().parent.parent

EXEC = [('docs/10-exec-summary.md', 'exec', 'Executive summary')]

FULL = [
    ('docs/10-exec-summary.md',            'exec',     'Executive summary'),
    ('docs/00-threat-landscape.md',        'threats',  'Threat landscape'),
    ('docs/01-gmail.md',                   'gmail',    'Gmail'),
    ('docs/02-calendar.md',                'calendar', 'Calendar'),
    ('docs/03-drive.md',                   'drive',    'Drive & Docs'),
    ('docs/04-groups.md',                  'groups',   'Groups'),
    ('docs/05-other-services.md',          'services', 'Other services'),
    ('docs/06-accounts-mfa-admins.md',     'identity', 'Accounts, MFA & admins'),
    ('docs/07-oauth-app-control.md',       'oauth',    'OAuth & app control'),
    ('docs/08-monitoring-response.md',     'monitor',  'Monitoring & response'),
    ('docs/09-dmarc-spf-dkim.md',          'dmarc',    'SPF, DKIM & DMARC'),
    ('checklists/rollout-phases.md',       'rollout',  'Rollout phases'),
    ('playbooks/00-index.md',              'pb-index', 'Playbooks'),
    ('playbooks/01-compromised-staff-account.md',   'pb-01', 'Playbook 01 · Compromised staff account'),
    ('playbooks/02-compromised-student-account.md', 'pb-02', 'Playbook 02 · Compromised student account'),
    ('playbooks/03-post-delivery-phish-purge.md',   'pb-03', 'Playbook 03 · Post-delivery phish purge'),
    ('playbooks/04-payroll-diversion-attempt.md',   'pb-04', 'Playbook 04 · Payroll diversion'),
    ('playbooks/05-vendor-invoice-fraud.md',        'pb-05', 'Playbook 05 · Vendor invoice fraud'),
    ('playbooks/06-mass-calendar-spam-cleanup.md',  'pb-06', 'Playbook 06 · Mass calendar spam'),
    ('playbooks/07-lookalike-domain-response.md',   'pb-07', 'Playbook 07 · Lookalike domain'),
    ('audit/gam/README.md',                'gam',      'GAM audit scripts'),
    ('audit/gam/remediation/README.md',    'gam-rem',  'GAM remediation scripts'),
    ('comms/README.md',                    'comms',    'Communication templates'),
    ('comms/01-phase1-staff-notice.md',    'cm-01',    'Template 01 · Phase 1 staff notice'),
    ('comms/02-phase2-2sv.md',             'cm-02',    'Template 02 · 2SV rollout'),
    ('comms/03-phase2-apps.md',            'cm-03',    'Template 03 · Third-party apps'),
    ('comms/04-phase3-vendor-notice.md',   'cm-04',    'Template 04 · Vendor authentication'),
    ('comms/05-phase4-students.md',        'cm-05',    'Template 05 · Student notice'),
    ('comms/06-phase4-guardians.md',       'cm-06',    'Template 06 · Guardian notice'),
    ('comms/07-incident-staff-notice.md',  'cm-07',    'Template 07 · Post-incident notice'),
    ('comms/08-service-sweep-notice.md',   'cm-08',    'Template 08 · Service sweep notice'),
    ('config/district-profile.md',         'profile',  'District profile'),
    ('ASSUMPTIONS.md',                     'assume',   'Assumptions'),
]

CSS = r"""
@page{size:letter; margin:16mm 15mm 18mm}
@page:first{margin:0}
:root{
  --ink:#0E1618; --ink-2:#42534F; --ink-3:#6E807D;
  --rule:#C9D4D3; --rule-2:#AEBDBB; --surface:#F4F7F7; --surface-2:#EAEFEF;
  --accent:#0F4C5C; --amber:#8A5C13; --amber-bg:#F6EEDD;
  --brick:#8F3134; --brick-bg:#F5E3E3; --moss:#2F6446;
  --sans:"Archivo",-apple-system,"Helvetica Neue",sans-serif;
  --serif:"Source Serif 4",Georgia,serif;
  --mono:"IBM Plex Mono",Menlo,monospace;
}
*{box-sizing:border-box}
body{margin:0; background:#fff; color:var(--ink); font-family:var(--serif);
  font-size:9.6pt; line-height:1.5; -webkit-print-color-adjust:exact; print-color-adjust:exact}

/* cover */
.cover{height:246mm; padding:26mm 22mm 0; page-break-after:always; position:relative;
  background:var(--accent); color:#fff}
.cover .rule{width:44mm; height:3pt; background:#fff; opacity:.55; margin-bottom:12mm}
.cover .kicker{font-family:var(--sans); font-size:8pt; font-weight:600; letter-spacing:.22em;
  text-transform:uppercase; opacity:.72; margin:0 0 6mm}
.cover h1{font-family:var(--sans); font-size:34pt; font-weight:700; letter-spacing:-.025em;
  line-height:1.04; margin:0 0 8mm; max-width:150mm}
.cover .sub{font-size:12pt; line-height:1.5; opacity:.9; max-width:130mm; margin:0 0 14mm}
.cover .facts{display:flex; flex-wrap:wrap; gap:5mm 12mm; font-family:var(--sans); font-size:8.5pt;
  opacity:.85; padding-top:6mm; border-top:1px solid rgba(255,255,255,.28); max-width:150mm}
.cover .facts b{display:block; font-size:15pt; font-weight:700; margin-bottom:1mm; opacity:1}
.cover .foot{position:absolute; left:22mm; right:22mm; bottom:18mm; font-family:var(--sans);
  font-size:8pt; opacity:.72; display:flex; justify-content:space-between;
  border-top:1px solid rgba(255,255,255,.28); padding-top:4mm}

/* contents */
.toc{page-break-after:always}
.toc h2{font-family:var(--sans); font-size:16pt; font-weight:700; margin:0 0 6mm;
  letter-spacing:-.02em}
.toc ol{list-style:none; margin:0; padding:0; font-family:var(--sans); font-size:10pt;
  columns:1}
.toc li{padding:2.2mm 0; border-bottom:1px solid var(--rule); display:flex; gap:5mm}
.toc .n{color:var(--ink-3); font-variant-numeric:tabular-nums; min-width:9mm}

h1{font-family:var(--sans); font-size:19pt; font-weight:700; letter-spacing:-.022em;
  line-height:1.12; margin:0 0 5mm; page-break-after:avoid}
h2{font-family:var(--sans); font-size:12.5pt; font-weight:700; letter-spacing:-.012em;
  margin:8mm 0 3mm; padding-top:3mm; border-top:1px solid var(--rule); page-break-after:avoid}
h3{font-family:var(--sans); font-size:10.5pt; font-weight:600; margin:6mm 0 2mm; page-break-after:avoid}
h4{font-family:var(--sans); font-size:8.6pt; font-weight:700; text-transform:uppercase;
  letter-spacing:.07em; color:var(--ink-2); margin:5mm 0 2mm; page-break-after:avoid}
p{margin:0 0 3mm; orphans:3; widows:3}
ul,ol{margin:0 0 3.5mm; padding-left:5mm}
li{margin:1mm 0}
li.task{list-style:none; display:flex; gap:2mm; margin-left:-5mm}
.box{flex:0 0 auto; width:8pt; height:8pt; margin-top:2.6pt; border:.8pt solid var(--rule-2); border-radius:1pt}
.box.done{background:var(--accent); border-color:var(--accent)}
a{color:var(--ink); text-decoration:none; border-bottom:.5pt solid var(--rule-2)}
a.ext{color:var(--accent); border-bottom-color:var(--accent)}
strong{font-weight:600}
code{font-family:var(--mono); font-size:.86em; background:var(--surface-2);
  padding:.3pt 1.4pt; border-radius:1.5pt; color:var(--accent)}
hr{border:none; border-top:1px solid var(--rule); margin:6mm 0}

.doc{page-break-before:always}
.doc-meta{font-family:var(--mono); font-size:7pt; color:var(--ink-3); margin-bottom:2mm}

.code{background:var(--surface); border:1px solid var(--rule); border-radius:2pt;
  margin:0 0 4mm; page-break-inside:avoid}
.code pre{margin:0; padding:3mm 3.5mm; overflow:hidden; white-space:pre-wrap; word-break:break-word}
.code code{font-family:var(--mono); font-size:7.4pt; line-height:1.5; background:none;
  padding:0; color:var(--ink-2)}
.code-lang{display:none}

blockquote{margin:0 0 4mm; padding:2.6mm 3.4mm; background:var(--surface);
  border-left:2.4pt solid var(--rule-2); page-break-inside:avoid}
blockquote :last-child{margin-bottom:0}
blockquote.warn{background:var(--amber-bg); border-left-color:var(--amber)}
blockquote.verify{background:var(--surface-2); border-left-color:var(--accent)}

.table-wrap{margin:0 0 4mm; border:1px solid var(--rule); border-radius:2pt; overflow:hidden}
table{border-collapse:collapse; width:100%; font-family:var(--sans); font-size:7.4pt;
  line-height:1.35; table-layout:fixed; font-variant-numeric:tabular-nums}
th{background:var(--surface-2); text-align:left; font-weight:700; font-size:6.6pt;
  text-transform:uppercase; letter-spacing:.04em; color:var(--ink-2);
  padding:1.8mm 1.6mm; border-bottom:.8pt solid var(--rule-2)}
td{padding:1.6mm; border-top:.5pt solid var(--rule); vertical-align:top; color:var(--ink-2);
  word-wrap:break-word; overflow-wrap:anywhere}
td strong{color:var(--ink)}
td.sev-high{color:var(--brick); font-weight:700}
td.sev-med{color:var(--amber); font-weight:700}
td.sev-low{color:var(--moss); font-weight:700}
table,blockquote{page-break-inside:avoid}
"""

HEAD = """<title>@@TITLE@@</title>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Mono:wght@400&display=swap">
<style>@@CSS@@</style>
"""


def build(mode):
    manifest = EXEC if mode == 'exec' else FULL
    link_map = {f: f'doc-{s}' for f, s, _ in manifest}
    is_exec = mode == 'exec'

    title = ('Email Security: What We’re Changing and Why' if is_exec
             else 'K-12 Google Workspace Anti-Phishing Hardening Package')
    sub = ('A one-page briefing for the superintendent and cabinet — the threat picture, '
           'what changes, what it costs staff, and what it prevents.'
           if is_exec else
           'A complete, setting-by-setting hardening package for a public school district on '
           'Google Workspace for Education — console paths, per-OU values, rollout order, '
           'and incident procedures.')
    facts = ([('12', 'threats assessed'), ('4', 'that stay high risk'), ('5', 'asks of the cabinet')]
             if is_exec else
             [('11', 'control documents'), ('7', 'incident playbooks'),
              ('15', 'audit scripts'), ('86', 'cited sources')])

    parts = [
        '<div class="cover"><div class="rule"></div>',
        '<p class="kicker">' + ('Cabinet briefing' if is_exec else 'Field package') + '</p>',
        f'<h1>{html.escape(title)}</h1><p class="sub">{html.escape(sub)}</p>',
        '<div class="facts">'
        + ''.join(f'<div><b>{n}</b>{html.escape(l)}</div>' for n, l in facts)
        + '</div>',
        '<div class="foot"><span>Research date 20 August 2026</span>'
        '<span>Console paths verified against current Google documentation</span></div></div>',
    ]

    if not is_exec:
        toc = ''.join(
            f'<li><span class="n">{i:02d}</span><span>{html.escape(label)}</span></li>'
            for i, (_, _, label) in enumerate(manifest))
        parts.append(f'<div class="toc"><h2>Contents</h2><ol>{toc}</ol></div>')

    for i, (f, slug, _label) in enumerate(manifest):
        body, _ = mdlib.render((ROOT / f).read_text(), slug, link_map, f)
        first = ' style="page-break-before:auto"' if (is_exec or i == 0) else ''
        parts.append(f'<section class="doc" id="doc-{slug}"{first}>'
                     f'<div class="doc-meta">{html.escape(f)}</div>{body}</section>')

    head = HEAD.replace('@@TITLE@@', html.escape(title)).replace('@@CSS@@', CSS)
    return head + '\n'.join(parts)


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'full'
    out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / 'site' / f'print-{mode}.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(mode))
    print(f'wrote {out} ({out.stat().st_size/1024:.0f} KB)')
