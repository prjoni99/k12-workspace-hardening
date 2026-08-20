# CLAUDE.md — Repo Conventions

Instructions for any agent (or human) editing this repo. This file governs *how* content
is written here. It does not override the user's global CLAUDE.md.

## What this repo is

Documentation + audit tooling for hardening a K-12 Google Workspace for Education Plus
tenant against phishing. The audience is a district IT team executing setting-by-setting,
often under time pressure, sometimes at 2am. Optimize for **executability**, not prose.

## Hard rules

### 1. No PII. Ever.

FERPA context. Never commit a student, staff, or guardian name, email address, student
ID, phone number, or message body. Record the *pattern* and the *fix*, not the people.

- Cabinet impersonation rules reference **roles**, not names. The actual name list lives
  in the Admin console rule only.
- GAM output goes to `audit/gam/out/`, which is `.gitignore`d. Do not commit it.
- Incident examples in playbooks are archetypes, never real incidents.

### 2. Six fields or it doesn't ship

Every recommended setting must carry: **(a)** exact current Admin console path,
**(b)** recommended value per OU (Staff / Students / Finance-HR / Admins),
**(c)** required edition, **(d)** user impact + comms note, **(e)** rollback,
**(f)** source URL. A setting missing any of these is incomplete, not "good enough".

### 3. Cite or flag — never invent

Every console path must trace to a current Google support article, cited inline at the
point of use. If a path cannot be verified, tag it `[VERIFY]` with what specifically
needs checking. **A plausible-sounding invented path is the worst possible output** —
it costs an admin twenty minutes of hunting and destroys trust in the rest of the doc.

If a setting has moved or been removed, say so explicitly and cite the change.

### 4. Never weaken a default; never broadly allowlist

No recommendation may move a setting in the permissive direction. No IP range, sender, or
domain gets added to anything that bypasses spam classification. The narrow, documented
exception process in `docs/01-gmail.md` §8 is the only path, and it is time-boxed.

### 5. Students stricter than staff; parents stay reachable

Student OUs default tighter. Staff OUs must preserve staff↔guardian email and sharing —
parents are external users. Any control that would block staff↔external communication
gets downgraded to a warning for staff, not applied.

### 6. Flag integration blast radius before the rollout phase

Anything that could break SIS integration, copier scan-to-email, SMTP relay, or a
third-party gateway must be flagged **in the doc where it appears** and again in
`checklists/rollout-phases.md` before it lands in a phase. `docs/09` gates on this.

## Style

- **Tables for settings.** Column order is fixed:
  `Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source`
- Console paths in `code`, using Google's own arrow style:
  `Admin console > Apps > Google Workspace > Gmail > Safety`
- Values: `Quarantine`, `Move to spam`, `Keep in inbox + warning`, `On`, `Off` — use
  Google's exact strings so an admin can pattern-match against the screen.
- Edition labels: **[Fundamentals]** / **[Standard]** / **[Plus]**. When a control needs
  Standard or Plus, state the Fundamentals fallback or say plainly there isn't one.
- Lead with the answer. No "in this section we will explore".
- Playbooks are numbered imperative steps with a verification line per step. Assume the
  reader is tired and being watched.

## Editions in this tenant

Assumed **Education Plus** district-wide (`ASSUMPTIONS.md` §A8). Many districts run Plus
for staff and Fundamentals/Standard for students — so every Plus-only control still
carries its lower-tier fallback. Don't strip those.

## Source URL convention

As of 2026-08-20, `support.google.com/a/answer/<id>` 301-redirects to
`knowledge.workspace.google.com/admin/<section>/<slug>`. Prefer the
`knowledge.workspace.google.com` form. When citing an article whose redirect target was
not confirmed, cite the `support.google.com` form as-is rather than constructing a
`knowledge.` URL — **constructed URLs are invented URLs.**

## Commits

Conventional commits, one per numbered deliverable:

```
docs(gmail): add safety, sandbox, quarantine, and content compliance controls
feat(audit): add read-only GAM7 audit scripts
chore: scaffold repo, todo list, and logged assumptions
```

## When adding a new control

1. Verify the path against a live Google article; capture the URL.
2. Decide the value for all four OU archetypes — "same everywhere" is a decision, state it.
3. Determine the edition floor and the fallback.
4. Write the rollback *before* the recommendation. If you can't undo it fast, say so.
5. Map it back to a threat in `docs/00-threat-landscape.md` — a control that mitigates
   nothing in the catalog probably doesn't belong.
6. Add it to the relevant rollout phase, with its blast radius noted.
