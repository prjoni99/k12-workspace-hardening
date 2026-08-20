# ASSUMPTIONS

The source prompt left the Context block unfilled. Per instruction, no questions were
asked — every gap below was filled with a reasonable assumption and logged here.
**Anything in this file is a guess until the district confirms it.** Correct
`config/district-profile.md` first; these docs reference tokens, not hard-coded values.

## A1 — District identity is tokenized, not invented

**Assumption:** Rather than invent a domain name, every doc uses replaceable tokens
(`<PRIMARY_DOMAIN>`, `<DISTRICT_NAME>`, `<SECONDARY_DOMAINS>`, `<SECURITY_ALIAS>`).
**Why:** Guessing a live district's mail domain and then publishing DNS records against
it is worse than a placeholder — a wrong `_dmarc` host silently does nothing, and a
*right-looking but wrong* one is worse still.
**Action required:** Fill in `config/district-profile.md` and run the substitution
snippet at the bottom of that file.

## A2 — Scale: ~1,200 staff / ~12,000 students

**Assumption:** A mid-size public district. Drives only two things in this repo:
quarantine-review staffing (assumed 2 reviewers, one primary) and the 2SV enrollment
window length (assumed 30 days). **Impact if wrong:** low — adjust the SLA table in
`docs/01-gmail.md` and the Phase 2 window in `checklists/rollout-phases.md`.

## A3 — OU structure

Assumed the structure suggested in the prompt:

```
/                          (root — most restrictive defaults inherit down)
├── /Staff
│   ├── /Staff/Finance-HR      ← payroll, AP, benefits, purchasing
│   └── /Staff/Admins          ← IT + super admin daily-driver accounts
├── /Students
│   ├── /Students/Elementary
│   ├── /Students/Middle
│   └── /Students/High
├── /Shared Devices            ← library/lab/kiosk, cart logins
└── /Service Accounts          ← SIS, relay, integrations (no interactive humans)
```

**Why it matters:** Every settings table in this repo has Staff / Students /
Finance-HR / Admins columns. If the real tree differs, the *columns* still map — they
are role archetypes, not literal OU paths. `/Shared Devices` and `/Service Accounts`
are called out individually where a setting would break them.

## A4 — Mail flow: Gmail direct MX, no third-party gateway

**Assumption:** MX points at Google; no Proofpoint/Mimecast/Barracuda in front.
**If a gateway exists this changes real things:** SPF must authorize the gateway,
inbound DMARC evaluation happens at the gateway not Gmail, and Gmail's spoofing
protections see the gateway as the sending IP — which usually means you must configure
an inbound gateway in Gmail so Google reads the *original* sender IP. Flagged inline in
`docs/01-gmail.md` and `docs/09-dmarc-spf-dkim.md`.

## A5 — Bulk senders that send as the district domain

The prompt calls this "critical for DMARC work" and it was blank. Assumed the typical
K-12 set, as a **starting inventory to verify, not a finished one**:

| Sender class | Typical product | Aligned by |
| --- | --- | --- |
| SIS | PowerSchool / Infinite Campus | SPF include + DKIM CNAME |
| Mass notification | SchoolMessenger / ParentSquare / Blackboard | SPF include + DKIM |
| LMS | Canvas / Schoology / Classroom | usually sends as vendor domain |
| Food service | Titan / LINQ / Nutrikids | often SPF-only — **DMARC risk** |
| Transportation | Zonar / Versatrans | often SPF-only |
| Copiers / MFP scan-to-email | Ricoh / Konica / Xerox | SMTP relay, **no DKIM** |
| Ticketing / helpdesk | Incident IQ / Freshservice | SPF include |
| Survey / forms | Qualtrics / Panorama | SPF include |
| SMTP relay users | scripts, alarm panels, HVAC, bells | relay, **no DKIM** |

**Why this is the single highest-risk assumption in the repo:** publishing
`p=reject` before this list is complete and aligned is the documented way to cut off
parent communication district-wide. `docs/09-dmarc-spf-dkim.md` gates enforcement on
completing this inventory.

## A6 — GAM7 configured with a super admin: assumed YES

Scripts in `audit/gam/` are written to run as-is. If GAM is not deployed they remain
valid documentation of *what to look at* — every script header names the Admin console
equivalent. Marked optional in `audit/gam/README.md`.

## A7 — Self-hosted Docker host available: assumed YES

`docs/09-dmarc-spf-dkim.md` ships a parsedmarc `compose.yaml`. Hosted alternatives are
listed for districts without a Docker host.

## A8 — Edition: Education Plus, district-wide

**Assumption:** Plus licensing covers *all* staff and students, not a subset.
**Common reality:** many districts license Plus for staff and Fundamentals/Standard for
students. Where a control needs Plus, this repo labels it and gives the
Fundamentals-tier fallback, so a split-license district can still execute.

## A9 — Parents/guardians are external users

Explicit in the prompt and treated as a hard constraint. No staff-side control in this
repo blocks external mail, external Drive sharing, or external Calendar invites
outright — staff settings warn, student settings restrict.

## A10 — No third-party MDM/identity layer assumed

Assumed Google as the IdP (no Okta/Entra SSO, no ClassLink/Clever as the auth source).
**If SSO is in front of Google,** 2SV enforcement and Context-Aware Access behave
differently — Google's 2SV policy does not apply to SSO-authenticated sessions, so the
phishing-resistant requirement must be enforced at the IdP instead. Flagged in
`docs/06-accounts-mfa-admins.md`.

## A11 — "Today" is 2026-08-20

All "as of" statements, the 12-month update window, and the Calendar control's rollout
status are anchored to this date.
