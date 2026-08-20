# K-12 Google Workspace Anti-Phishing Hardening Package

An execution-ready hardening package for a public school district on **Google Workspace
for Education Plus**. Written to be worked setting-by-setting by a district IT team, not
read as a whitepaper.

**Research date: 2026-08-20.** Console paths move. Anything not verifiable against a
current Google support article on that date is tagged `[VERIFY]` rather than guessed.

---

## Read it without cloning anything

Not everyone who needs this reads markdown. Three editions, same source:

| Edition | Who it's for | Notes |
| --- | --- | --- |
| **[Web edition](https://k12.jonvargas.net/)** | Anyone | Full package, sidebar navigation, searchable, works on a phone. Prints to PDF from the browser. |
| **[Exec summary PDF](https://k12.jonvargas.net/K-12-Workspace-Hardening-Exec-Summary.pdf)** | Superintendent, cabinet, board | 5 pages. Threat picture, what changes, what it costs, what we need. |
| **[Full package PDF](https://k12.jonvargas.net/K-12-Workspace-Hardening-Full-Package.pdf)** | District IT | 136 pages, everything, with a contents page. |

The web and PDF editions are **generated** from the markdown — edit the markdown, then
`python3 tools/build-site.py` and `./tools/make-pdfs.sh`. Never edit them by hand; they
will be overwritten.

---

## Start here

0. **Install the commit guard: `./tools/install-hooks.sh`** — it blocks committing
   real district values into a shared repo. Do this before step 1.
1. Fill in **[config/district-profile.md](config/district-profile.md)** *(keep the
   filled-in copy out of any public repo — see [CONTRIBUTING.md](CONTRIBUTING.md))* — nothing else
   works until the OU map and bulk-sender inventory exist.
2. Read **[ASSUMPTIONS.md](ASSUMPTIONS.md)** — 11 assumptions were made in place of the
   unfilled Context block. Confirm or correct each.
3. Work **[checklists/rollout-phases.md](checklists/rollout-phases.md)** in order.
   Do not jump to Phase 3 (DMARC); it is the only phase that can break parent
   communication district-wide.

## What's here

| Path | What it is |
| --- | --- |
| [docs/00-threat-landscape.md](docs/00-threat-landscape.md) | Current K-12 phishing catalog, each threat mapped to the controls that mitigate it |
| [docs/01-gmail.md](docs/01-gmail.md) | The core. Gmail Safety, sandbox, quarantine, end-user access, content compliance |
| [docs/02-calendar.md](docs/02-calendar.md) | External sharing, and the **2026-08-14** invitation admin control |
| [docs/03-drive.md](docs/03-drive.md) | Per-OU sharing, link defaults, trust rules, DLP |
| [docs/04-groups.md](docs/04-groups.md) | The control that stops one spoofed email reaching every employee |
| [docs/05-other-services.md](docs/05-other-services.md) | Chat, Meet, Classroom, Gemini, Takeout, and the unused-service sweep |
| [docs/06-accounts-mfa-admins.md](docs/06-accounts-mfa-admins.md) | 2SV, phishing-resistant methods, APP, super admin hygiene, CAA |
| [docs/07-oauth-app-control.md](docs/07-oauth-app-control.md) | API controls, Marketplace, under-18 app requests, domain-wide delegation |
| [docs/08-monitoring-response.md](docs/08-monitoring-response.md) | Alert center, activity rules, investigation tool, log retention |
| [docs/09-dmarc-spf-dkim.md](docs/09-dmarc-spf-dkim.md) | Inventory → SPF → DKIM → staged DMARC ramp, with parsedmarc |
| [docs/10-exec-summary.md](docs/10-exec-summary.md) | One page, cabinet-ready, no jargon |
| [playbooks/](playbooks/) | Numbered, 2am-executable incident procedures |
| [audit/gam/](audit/gam/) | Read-only GAM7 audit scripts. Write commands isolated in `remediation/` |
| [checklists/rollout-phases.md](checklists/rollout-phases.md) | Phase 0–4 plus ongoing ops cadence |
| [comms/](comms/) | Staff/parent communication templates referenced by the rollout phases |

## The rules this package holds to

1. **No broad allowlisting.** No IP range, sender, or domain is ever added to a list that
   bypasses spam classification. The narrow exception process is in
   [docs/01-gmail.md](docs/01-gmail.md) §8. This is the most commonly self-inflicted
   K-12 email security wound and it is not negotiable here.
2. **Never weaken a Google default.** Every recommendation moves a setting toward
   stricter, or leaves it alone.
3. **Students default stricter than staff.** Staff settings must preserve
   parent/guardian communication — parents are external users and always will be.
4. **Instruction does not break.** A student-facing restriction that stops teaching gets
   rolled back, not defended.
5. **Cite or flag.** Every console path traces to a current Google article, or carries
   `[VERIFY]`.

## Documentation contract

Every recommended setting, in every doc, carries all six of:

| Field | Meaning |
| --- | --- |
| **Path** | Exact current Admin console navigation |
| **Value per OU** | Staff / Students / Finance-HR / Admins |
| **Edition** | Fundamentals, Standard, or Plus — with the lower-tier fallback if one exists |
| **Impact + comms** | What users notice, and what you tell them beforehand |
| **Rollback** | How to undo, and how fast |
| **Source** | URL to the Google article the path came from |

Settings tables use this column order:

`Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source`

## A note on Google's documentation URLs

As of 2026-08-20, `support.google.com/a/answer/<id>` **301-redirects** to
`knowledge.workspace.google.com/admin/<section>/<slug>`. This repo cites the
`knowledge.workspace.google.com` URLs where the redirect was followed and confirmed.
Old `support.google.com` links still resolve; they are not dead, just no longer canonical.

## Scope boundary

This package covers Google Workspace configuration, monitoring, and response. It does
**not** cover: endpoint/EDR, network segmentation, backup and recovery architecture,
cyber insurance, or the ed-tech vendor risk program. Those matter as much — phishing is
initial access, and the controls here shrink the front door, not the whole house.
See [docs/00-threat-landscape.md](docs/00-threat-landscape.md) §T11 for where this
package hands off.
