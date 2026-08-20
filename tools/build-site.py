#!/usr/bin/env python3
"""Build the single-file shareable HTML edition from the markdown sources.

Usage:  python3 tools/build-site.py [output.html]

The site is generated, never hand-edited: edit the markdown, rerun this.
No third-party dependencies - python3 alone.
"""
import html
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import md as mdlib  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'site' / 'index.html'

# (file, slug, nav label, track)
MANIFEST = [
    ('docs/10-exec-summary.md',            'exec',      'Executive summary',            'lead'),
    ('docs/00-threat-landscape.md',        'threats',   '00 · Threat landscape',        'tech'),
    ('docs/01-gmail.md',                   'gmail',     '01 · Gmail',                   'tech'),
    ('docs/02-calendar.md',                'calendar',  '02 · Calendar',                'tech'),
    ('docs/03-drive.md',                   'drive',     '03 · Drive & Docs',            'tech'),
    ('docs/04-groups.md',                  'groups',    '04 · Groups',                  'tech'),
    ('docs/05-other-services.md',          'services',  '05 · Other services',          'tech'),
    ('docs/06-accounts-mfa-admins.md',     'identity',  '06 · Accounts, MFA & admins',  'tech'),
    ('docs/07-oauth-app-control.md',       'oauth',     '07 · OAuth & app control',     'tech'),
    ('docs/08-monitoring-response.md',     'monitor',   '08 · Monitoring & response',   'tech'),
    ('docs/09-dmarc-spf-dkim.md',          'dmarc',     '09 · SPF, DKIM & DMARC',       'tech'),
    ('checklists/rollout-phases.md',       'rollout',   'Rollout phases',               'run'),
    ('playbooks/00-index.md',              'pb-index',  'Playbooks · index',            'run'),
    ('playbooks/01-compromised-staff-account.md',   'pb-01', '01 · Compromised staff account',   'run'),
    ('playbooks/02-compromised-student-account.md', 'pb-02', '02 · Compromised student account', 'run'),
    ('playbooks/03-post-delivery-phish-purge.md',   'pb-03', '03 · Post-delivery phish purge',   'run'),
    ('playbooks/04-payroll-diversion-attempt.md',   'pb-04', '04 · Payroll diversion',           'run'),
    ('playbooks/05-vendor-invoice-fraud.md',        'pb-05', '05 · Vendor invoice fraud',        'run'),
    ('playbooks/06-mass-calendar-spam-cleanup.md',  'pb-06', '06 · Mass calendar spam',          'run'),
    ('playbooks/07-lookalike-domain-response.md',   'pb-07', '07 · Lookalike domain',            'run'),
    ('audit/gam/README.md',                'gam',       'GAM audit scripts',            'run'),
    ('audit/gam/remediation/README.md',    'gam-rem',   'GAM remediation',              'run'),
    ('comms/README.md',                    'comms',     'Communication templates',      'run'),
    ('config/district-profile.md',         'profile',   'District profile (fill first)','ref'),
    ('ASSUMPTIONS.md',                     'assume',    'Assumptions',                  'ref'),
    ('CLAUDE.md',                          'conv',      'Repo conventions',             'ref'),
]

TRACKS = [
    ('lead', 'Leadership', 'Read this one. One page, no jargon.'),
    ('tech', 'The controls', 'Setting-by-setting, per OU, with sources.'),
    ('run',  'Run it',      'Rollout order, incident procedures, audit tooling.'),
    ('ref',  'Reference',   'Fill-in-first, assumptions, conventions.'),
]

# Residual risk after every control in the package is applied. Hand-maintained
# from docs/00 coverage matrix - the honest headline of the whole package.
RISK = [
    ('T1',  'Leadership impersonation',    'low',  'Employee-name spoofing → Quarantine'),
    ('T2',  'Payroll diversion',           'med',  'Needs a payroll process change'),
    ('T3',  'Vendor invoice fraud',        'high', 'Authenticates cleanly. Process only'),
    ('T4',  'AiTM credential phishing',    'low',  'Only if phishing-resistant 2SV'),
    ('T5',  'QR-code phishing',            'high', 'Physical vector uncontrolled'),
    ('T6',  'Calendar-invite phishing',    'low',  'New 2026-08-14 admin control'),
    ('T7',  'Google-service abuse',        'med',  'Structural. Shrink the surface'),
    ('T8',  'Trusted-partner compromise',  'high', 'Passes SPF, DKIM and DMARC'),
    ('T9',  'Student ATO / internal',      'med',  'Internal mail is unfiltered'),
    ('T10', 'Sextortion / student scams',  'high', 'Mostly off-platform'),
    ('T11', 'Ransomware initial access',   'med',  'Hands off to EDR and backup'),
    ('T12', 'MFA fatigue / deepfakes',     'med',  'Procedure-dependent'),
]


def build():
    link_map = {pathlib.Path(f).name: f'doc-{slug}' for f, slug, _, _ in MANIFEST}
    # files that exist but are not their own section resolve to the nearest home
    for extra, target in [('README.md', 'top'), ('TODO.md', 'top'),
                          ('00-index.md', 'doc-pb-index')]:
        link_map.setdefault(extra, target)
    for p in (ROOT / 'comms').glob('*.md'):
        link_map.setdefault(p.name, 'doc-comms')
    for p in (ROOT / 'audit/gam').rglob('*.sh'):
        link_map.setdefault(p.name, 'doc-gam')

    sections, navs = [], {t: [] for t, _, _ in TRACKS}
    for f, slug, label, track in MANIFEST:
        src = (ROOT / f).read_text()
        body, toc = mdlib.render(src, slug, link_map)
        subs = [(i, t) for lvl, i, t in toc if lvl == 2][:14]
        navs[track].append((slug, label, subs))
        sections.append(
            f'<section class="doc" id="doc-{slug}">'
            f'<div class="doc-meta"><span class="doc-src">{html.escape(f)}</span></div>'
            f'{body}</section>')

    nav = []
    for key, name, blurb in TRACKS:
        nav.append(f'<div class="nav-track"><p class="nav-h">{name}</p>'
                   f'<p class="nav-blurb">{html.escape(blurb)}</p><ul>')
        for slug, label, subs in navs[key]:
            sub = ''.join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in subs)
            nav.append(f'<li><a class="nav-doc" href="#doc-{slug}">{html.escape(label)}</a>'
                       + (f'<ul class="nav-sub">{sub}</ul>' if sub else '') + '</li>')
        nav.append('</ul></div>')

    counts = {k: sum(1 for _, _, s, _ in RISK if s == k) for k in ('high', 'med', 'low')}
    risk_rows = ''.join(
        f'<tr class="r-{sev}"><td class="r-id">{tid}</td>'
        f'<td class="r-name">{html.escape(name)}</td>'
        f'<td class="r-note">{html.escape(note)}</td>'
        f'<td class="r-sev"><span class="pill p-{sev}">{sev.upper()}</span></td></tr>'
        for tid, name, sev, note in RISK)

    page = TEMPLATE
    for key, val in (('@@NAV@@', ''.join(nav)),
                     ('@@SECTIONS@@', '\n'.join(sections)),
                     ('@@RISK@@', risk_rows),
                     ('@@HIGH@@', str(counts['high'])),
                     ('@@MED@@', str(counts['med'])),
                     ('@@LOW@@', str(counts['low']))):
        page = page.replace(key, val)
    return page


TEMPLATE = r"""<title>K-12 Workspace Hardening</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="An anti-phishing hardening package for school districts on Google Workspace for Education.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --paper:#F5F7F7; --surface:#FFFFFF; --surface-2:#EAEFEF; --surface-3:#DFE7E6;
  --ink:#0E1618; --ink-2:#42534F; --ink-3:#6E807D;
  --rule:#D3DCDB; --rule-2:#BCC9C7;
  --accent:#0F4C5C; --accent-2:#16697A; --accent-soft:#DDEAEC;
  --amber:#A9711A; --amber-bg:#F6E9D2; --amber-line:#D98E28;
  --brick:#8F3134; --brick-bg:#F3DEDE; --brick-line:#A63D40;
  --moss:#2F6446; --moss-bg:#DDEBE2;
  --shadow:0 1px 2px rgba(14,22,24,.05),0 8px 24px -12px rgba(14,22,24,.14);
  --sans:"Archivo",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  --serif:"Source Serif 4",Georgia,"Times New Roman",serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#0A1113; --surface:#0F191C; --surface-2:#152225; --surface-3:#1C2C30;
    --ink:#E4EDEC; --ink-2:#A3B5B3; --ink-3:#788B89;
    --rule:#223437; --rule-2:#2E4448;
    --accent:#5CB8C9; --accent-2:#7FCDDB; --accent-soft:#14282E;
    --amber:#E7AC55; --amber-bg:#2C2312; --amber-line:#C98E33;
    --brick:#DD8A8C; --brick-bg:#2E1A1B; --brick-line:#B4585B;
    --moss:#7FBF98; --moss-bg:#16261D;
    --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 28px -14px rgba(0,0,0,.7);
  }
}
:root[data-theme="dark"]{
  --paper:#0A1113; --surface:#0F191C; --surface-2:#152225; --surface-3:#1C2C30;
  --ink:#E4EDEC; --ink-2:#A3B5B3; --ink-3:#788B89;
  --rule:#223437; --rule-2:#2E4448;
  --accent:#5CB8C9; --accent-2:#7FCDDB; --accent-soft:#14282E;
  --amber:#E7AC55; --amber-bg:#2C2312; --amber-line:#C98E33;
  --brick:#DD8A8C; --brick-bg:#2E1A1B; --brick-line:#B4585B;
  --moss:#7FBF98; --moss-bg:#16261D;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 28px -14px rgba(0,0,0,.7);
}

*{box-sizing:border-box}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:var(--serif); font-size:17px; line-height:1.65;
  -webkit-font-smoothing:antialiased;
}
.layout{display:grid; grid-template-columns:300px minmax(0,1fr); gap:0; align-items:start}

/* ---------- sidebar ---------- */
.side{
  position:sticky; top:0; height:100vh; overflow-y:auto;
  background:var(--surface); border-right:1px solid var(--rule);
  padding:1.6rem 1.1rem 3rem; font-family:var(--sans);
}
.brand{display:flex; flex-direction:column; gap:.15rem; margin-bottom:.4rem}
.brand b{font-size:.94rem; font-weight:700; letter-spacing:-.01em; color:var(--ink)}
.brand span{font-size:.68rem; text-transform:uppercase; letter-spacing:.1em; color:var(--ink-3)}
.filter{
  width:100%; margin:.9rem 0 1.1rem; padding:.5rem .65rem;
  font-family:var(--sans); font-size:.82rem; color:var(--ink);
  background:var(--surface-2); border:1px solid var(--rule); border-radius:5px;
}
.filter::placeholder{color:var(--ink-3)}
.filter:focus{outline:2px solid var(--accent); outline-offset:1px}
.nav-track{margin-bottom:1.5rem}
.nav-h{margin:0; font-size:.7rem; font-weight:700; text-transform:uppercase;
  letter-spacing:.13em; color:var(--accent)}
.nav-blurb{margin:.2rem 0 .6rem; font-size:.72rem; line-height:1.4; color:var(--ink-3)}
.side ul{list-style:none; margin:0; padding:0}
.nav-doc{
  display:block; padding:.3rem .5rem; border-radius:4px; text-decoration:none;
  font-size:.82rem; line-height:1.35; color:var(--ink-2); border-left:2px solid transparent;
}
.nav-doc:hover{background:var(--surface-2); color:var(--ink)}
.nav-doc.active{color:var(--accent); background:var(--accent-soft); border-left-color:var(--accent); font-weight:600}
.nav-sub{max-height:0; overflow:hidden; transition:max-height .25s ease}
li:has(.nav-doc.active) .nav-sub{max-height:34rem}
.nav-sub a{
  display:block; padding:.15rem .5rem .15rem 1.15rem; font-size:.75rem;
  color:var(--ink-3); text-decoration:none; border-left:1px solid var(--rule);
  margin-left:.5rem;
}
.nav-sub a:hover{color:var(--accent); border-left-color:var(--accent)}

/* ---------- main ---------- */
main{padding:0 clamp(1.2rem,4vw,4rem) 8rem; max-width:none; min-width:0}
.wrap{max-width:78ch; margin:0 auto}
.doc :is(p,ul,ol,blockquote){max-width:70ch}

/* ---------- hero ---------- */
.hero{padding:clamp(3rem,7vw,5.5rem) 0 2.5rem; border-bottom:1px solid var(--rule)}
.eyebrow{
  font-family:var(--sans); font-size:.7rem; font-weight:600; text-transform:uppercase;
  letter-spacing:.15em; color:var(--accent); margin:0 0 1rem;
}
h1.title{
  font-family:var(--sans); font-weight:700; letter-spacing:-.03em; line-height:1.02;
  font-size:clamp(2.3rem,5.6vw,4rem); margin:0 0 1.1rem; text-wrap:balance; color:var(--ink);
}
.standfirst{font-size:1.16rem; line-height:1.55; color:var(--ink-2); margin:0 0 1.6rem; max-width:60ch}
.meta{
  display:flex; flex-wrap:wrap; gap:.5rem 1.6rem; font-family:var(--sans);
  font-size:.76rem; color:var(--ink-3); padding-top:1.1rem; border-top:1px solid var(--rule);
}
.meta b{color:var(--ink-2); font-weight:600}

/* ---------- risk board ---------- */
.board{margin:2.6rem 0 0; background:var(--surface); border:1px solid var(--rule);
  border-radius:8px; box-shadow:var(--shadow); overflow:hidden}
.board-head{padding:1.1rem 1.3rem; border-bottom:1px solid var(--rule);
  display:flex; flex-wrap:wrap; gap:.8rem 1.4rem; align-items:baseline; justify-content:space-between}
.board-head h2{font-family:var(--sans); font-size:.98rem; font-weight:700; margin:0; letter-spacing:-.01em}
.board-head p{margin:.25rem 0 0; font-size:.82rem; color:var(--ink-3); font-family:var(--sans)}
.tally{display:flex; gap:1.2rem; font-family:var(--sans)}
.tally div{text-align:right}
.tally b{display:block; font-size:1.5rem; font-weight:700; line-height:1; font-variant-numeric:tabular-nums}
.tally span{font-size:.64rem; text-transform:uppercase; letter-spacing:.1em; color:var(--ink-3)}
.t-high b{color:var(--brick)} .t-med b{color:var(--amber)} .t-low b{color:var(--moss)}
table.risk{width:100%; border-collapse:collapse; font-family:var(--sans); font-size:.83rem}
table.risk td{padding:.55rem 1.3rem; border-top:1px solid var(--rule); vertical-align:middle}
table.risk tr:first-child td{border-top:none}
.r-id{color:var(--ink-3); font-variant-numeric:tabular-nums; width:3.2rem; font-size:.76rem}
.r-name{font-weight:600; color:var(--ink)}
.r-note{color:var(--ink-3); font-size:.79rem}
.r-sev{text-align:right; width:5.5rem}
.pill{display:inline-block; padding:.12rem .5rem; border-radius:99px; font-size:.65rem;
  font-weight:700; letter-spacing:.07em}
.p-high{background:var(--brick-bg); color:var(--brick)}
.p-med{background:var(--amber-bg); color:var(--amber)}
.p-low{background:var(--moss-bg); color:var(--moss)}
.board-foot{padding:.9rem 1.3rem; background:var(--surface-2); border-top:1px solid var(--rule);
  font-size:.82rem; color:var(--ink-2); font-family:var(--sans); line-height:1.5}

/* ---------- doors ---------- */
.doors{display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:1rem; margin:2.2rem 0 0}
.door{
  display:block; padding:1.15rem 1.25rem; text-decoration:none; background:var(--surface);
  border:1px solid var(--rule); border-top:3px solid var(--accent); border-radius:6px;
  font-family:var(--sans); transition:border-color .15s, transform .15s;
}
.door:hover{border-color:var(--rule-2); border-top-color:var(--accent-2); transform:translateY(-2px)}
.door b{display:block; font-size:.95rem; color:var(--ink); margin-bottom:.25rem}
.door span{font-size:.8rem; color:var(--ink-3); line-height:1.45; display:block}
.door em{display:block; margin-top:.55rem; font-style:normal; font-size:.72rem;
  text-transform:uppercase; letter-spacing:.1em; color:var(--accent); font-weight:600}

/* ---------- documents ---------- */
.doc{padding:3.5rem 0 1rem; border-top:1px solid var(--rule)}
.doc:first-of-type{border-top:none}
.doc-meta{margin-bottom:.7rem}
.doc-src{font-family:var(--mono); font-size:.68rem; color:var(--ink-3);
  background:var(--surface-2); padding:.16rem .45rem; border-radius:3px}
.doc h1{font-family:var(--sans); font-size:clamp(1.7rem,3.6vw,2.5rem); font-weight:700;
  letter-spacing:-.025em; line-height:1.1; margin:.2rem 0 1.1rem; text-wrap:balance}
.doc h2{font-family:var(--sans); font-size:1.32rem; font-weight:700; letter-spacing:-.015em;
  margin:2.6rem 0 .8rem; padding-top:1.1rem; border-top:1px solid var(--rule); text-wrap:balance}
.doc h3{font-family:var(--sans); font-size:1.05rem; font-weight:600; margin:1.9rem 0 .6rem; text-wrap:balance}
.doc h4{font-family:var(--sans); font-size:.88rem; font-weight:600; margin:1.4rem 0 .5rem;
  text-transform:uppercase; letter-spacing:.07em; color:var(--ink-2)}
.doc p{margin:0 0 1rem}
.doc p.defrun{line-height:1.9}
.doc :is(ul,ol){margin:0 0 1.1rem; padding-left:1.3rem}
.doc li{margin:.3rem 0}
.doc li.task{list-style:none; display:flex; gap:.55rem; align-items:flex-start; margin-left:-1.3rem}
.box{flex:0 0 auto; width:.92rem; height:.92rem; margin-top:.34rem; border-radius:3px;
  border:1.5px solid var(--rule-2); background:var(--surface)}
.box.done{background:var(--accent); border-color:var(--accent); position:relative}
.box.done::after{content:""; position:absolute; left:.26rem; top:.08rem; width:.22rem; height:.46rem;
  border:solid var(--surface); border-width:0 2px 2px 0; transform:rotate(42deg)}
.doc a{color:var(--accent); text-underline-offset:2px; text-decoration-thickness:1px}
.doc a:hover{color:var(--accent-2)}
.doc a.ext::after{content:"↗"; font-size:.7em; vertical-align:super; margin-left:.1em; opacity:.6}
.doc strong{font-weight:600; color:var(--ink)}
.doc code{font-family:var(--mono); font-size:.85em; background:var(--surface-2);
  padding:.1rem .32rem; border-radius:3px; color:var(--accent); word-break:break-word}
.doc hr{border:none; border-top:1px solid var(--rule); margin:2.2rem 0}

.code{position:relative; margin:0 0 1.3rem; background:var(--surface);
  border:1px solid var(--rule); border-radius:6px; overflow:hidden}
.code-lang{position:absolute; top:0; right:0; font-family:var(--sans); font-size:.62rem;
  text-transform:uppercase; letter-spacing:.1em; color:var(--ink-3);
  background:var(--surface-2); padding:.2rem .55rem; border-radius:0 0 0 5px}
.code pre{margin:0; padding:1rem 1.1rem; overflow-x:auto}
.code code{font-family:var(--mono); font-size:.79rem; line-height:1.6;
  background:none; padding:0; color:var(--ink-2); white-space:pre}

blockquote{margin:0 0 1.3rem; padding:.9rem 1.1rem; background:var(--surface);
  border-left:3px solid var(--rule-2); border-radius:0 5px 5px 0}
blockquote :last-child{margin-bottom:0}
blockquote.warn{background:var(--amber-bg); border-left-color:var(--amber-line)}
blockquote.verify{background:var(--surface-2); border-left-color:var(--accent)}
blockquote p{font-size:.94rem}

.table-wrap{overflow-x:auto; margin:0 0 1.4rem; border:1px solid var(--rule);
  border-radius:6px; background:var(--surface)}
/* Wide settings tables break out of the reading column: prose stays at ~70ch,
   tables take the width that is actually available. --bo is the breakout width. */
@media (min-width:1150px){
  .doc .table-wrap{
    --bo:min(calc(100vw - 300px - 9rem), calc(100% + 20rem));
    width:var(--bo); margin-left:calc((100% - var(--bo)) / 2);
  }
}
table{border-collapse:collapse; width:100%; font-family:var(--sans); font-size:.8rem;
  line-height:1.45; font-variant-numeric:tabular-nums}
th{background:var(--surface-2); font-weight:700; text-align:left; padding:.6rem .75rem;
  border-bottom:1px solid var(--rule-2); white-space:nowrap; font-size:.72rem;
  text-transform:uppercase; letter-spacing:.05em; color:var(--ink-2)}
td{padding:.55rem .75rem; border-top:1px solid var(--rule); vertical-align:top; color:var(--ink-2)}
td strong{color:var(--ink)}
td code{font-size:.92em}
td.sev-high{color:var(--brick); font-weight:600}
td.sev-med{color:var(--amber); font-weight:600}
td.sev-low{color:var(--moss); font-weight:600}

/* ---------- chrome ---------- */
.topbar{display:none}
.tools{position:fixed; right:1rem; bottom:1rem; display:flex; gap:.4rem; z-index:40}
.tool{
  font-family:var(--sans); font-size:.72rem; font-weight:600; cursor:pointer;
  background:var(--surface); color:var(--ink-2); border:1px solid var(--rule-2);
  border-radius:99px; padding:.5rem .85rem; box-shadow:var(--shadow);
}
.tool:hover{color:var(--accent); border-color:var(--accent)}
.tool:focus-visible{outline:2px solid var(--accent); outline-offset:2px}
a:focus-visible,button:focus-visible{outline:2px solid var(--accent); outline-offset:2px; border-radius:3px}
.hidden{display:none !important}

@media (max-width:900px){
  .layout{grid-template-columns:1fr}
  .side{position:fixed; inset:0 auto 0 0; width:min(86vw,320px); z-index:50;
    transform:translateX(-101%); transition:transform .2s ease; box-shadow:var(--shadow)}
  .side.open{transform:none}
  .topbar{display:flex; position:sticky; top:0; z-index:30; align-items:center; gap:.7rem;
    padding:.6rem 1rem; background:var(--surface); border-bottom:1px solid var(--rule);
    font-family:var(--sans); font-weight:700; font-size:.85rem}
  .topbar button{font:inherit; font-size:1.1rem; background:none; border:none;
    color:var(--ink); cursor:pointer; padding:.1rem .3rem}
  main{padding-left:1.1rem; padding-right:1.1rem}
}
@media (prefers-reduced-motion:reduce){*{animation:none !important; transition:none !important}}

@media print{
  .side,.tools,.topbar,.doors{display:none !important}
  .layout{display:block}
  body{background:#fff; color:#000; font-size:10.5pt}
  main{padding:0}
  .doc{page-break-before:always; border-top:none}
  .hero{page-break-after:always}
  h1,h2,h3{page-break-after:avoid} table,blockquote,.code{page-break-inside:avoid}
  a{color:#000; text-decoration:none} .doc a.ext::after{content:""}
  .board{box-shadow:none}
}
</style>

<div class="topbar"><button id="menu" aria-label="Toggle navigation">☰</button><span>K-12 Workspace Hardening</span></div>
<div class="layout">
<aside class="side" id="side">
  <div class="brand"><b>K-12 Workspace Hardening</b><span>Anti-phishing package</span></div>
  <input class="filter" id="filter" type="search" placeholder="Filter sections…" aria-label="Filter sections">
  <nav id="nav">@@NAV@@</nav>
</aside>

<main>
<div class="wrap">
<header class="hero">
  <p class="eyebrow">Field package · Research date 20 August 2026</p>
  <h1 class="title">Hardening a district against the phishing that actually works</h1>
  <p class="standfirst">A complete, setting-by-setting anti-phishing package for a public school
  district on Google Workspace for Education — the console paths, the per-OU values, the rollout
  order, and the incident procedures. Built to be executed, not admired.</p>
  <div class="meta">
    <span><b>11</b> control documents</span>
    <span><b>7</b> incident playbooks</span>
    <span><b>15</b> audit &amp; remediation scripts</span>
    <span><b>86</b> cited sources</span>
    <span><b>~40,000</b> words</span>
  </div>

  <div class="board">
    <div class="board-head">
      <div>
        <h2>Residual risk after every control here is applied</h2>
        <p>The honest version. Four threats stay High — and three of those close only with process, not configuration.</p>
      </div>
      <div class="tally">
        <div class="t-high"><b>@@HIGH@@</b><span>High</span></div>
        <div class="t-med"><b>@@MED@@</b><span>Medium</span></div>
        <div class="t-low"><b>@@LOW@@</b><span>Low</span></div>
      </div>
    </div>
    <table class="risk"><tbody>@@RISK@@</tbody></table>
    <div class="board-foot"><strong>Read that column before presenting this to a cabinet.</strong>
    “We closed the configurable gaps, and here are the three that need people” is accurate.
    “We fixed phishing” is not.</div>
  </div>

  <div class="doors">
    <a class="door" href="#doc-exec"><b>If you run the district</b>
      <span>One page. What's changing, what it costs staff, what it prevents, and the five things we need from you.</span>
      <em>Executive summary →</em></a>
    <a class="door" href="#doc-rollout"><b>If you're implementing it</b>
      <span>Phase 0 through 4, with prerequisites, blast-radius warnings and rollback triggers. Phase 1 carries most of the benefit.</span>
      <em>Rollout phases →</em></a>
    <a class="door" href="#doc-threats"><b>If you want the reasoning</b>
      <span>Twelve threat classes with 2026 sourcing, each mapped to the controls that mitigate it.</span>
      <em>Threat landscape →</em></a>
  </div>
</header>

@@SECTIONS@@
</div>
</main>
</div>

<div class="tools">
  <button class="tool" id="theme">Theme</button>
  <button class="tool" id="print">Save as PDF</button>
  <button class="tool" id="top">↑ Top</button>
</div>

<script>
(function(){
  var side=document.getElementById('side');
  document.getElementById('menu').onclick=function(){side.classList.toggle('open')};
  side.addEventListener('click',function(e){
    if(e.target.tagName==='A'&&window.innerWidth<=900) side.classList.remove('open');
  });
  document.getElementById('top').onclick=function(){window.scrollTo({top:0,behavior:'smooth'})};
  document.getElementById('print').onclick=function(){window.print()};

  var root=document.documentElement;
  document.getElementById('theme').onclick=function(){
    var cur=root.getAttribute('data-theme');
    if(!cur){
      cur=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
    }
    root.setAttribute('data-theme',cur==='dark'?'light':'dark');
  };

  // filter
  var filter=document.getElementById('filter'), nav=document.getElementById('nav');
  filter.addEventListener('input',function(){
    var q=this.value.trim().toLowerCase();
    nav.querySelectorAll('.nav-doc').forEach(function(a){
      var li=a.parentElement;
      li.classList.toggle('hidden', q!=='' && a.textContent.toLowerCase().indexOf(q)<0);
    });
    nav.querySelectorAll('.nav-track').forEach(function(t){
      var any=Array.prototype.some.call(t.querySelectorAll('.nav-doc'),function(a){
        return !a.parentElement.classList.contains('hidden')});
      t.classList.toggle('hidden', !any);
    });
  });

  // scroll spy
  var links={}, docs=[].slice.call(document.querySelectorAll('section.doc'));
  nav.querySelectorAll('.nav-doc').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      var a=links[en.target.id]; if(!a) return;
      if(en.isIntersecting){
        nav.querySelectorAll('.nav-doc.active').forEach(function(x){x.classList.remove('active')});
        a.classList.add('active');
        if(a.getBoundingClientRect().top<0||a.getBoundingClientRect().bottom>innerHeight)
          a.scrollIntoView({block:'center'});
      }
    });
  },{rootMargin:'-15% 0px -75% 0px'});
  docs.forEach(function(d){io.observe(d)});
})();
</script>
"""

if __name__ == '__main__':
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build())
    kb = OUT.stat().st_size / 1024
    print(f'wrote {OUT}  ({kb:.0f} KB)')
