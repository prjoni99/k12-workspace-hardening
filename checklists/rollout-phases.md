# Rollout Phases

**Work these in order.** Each phase has prerequisites, a change list, comms, success
criteria, and a rollback trigger.

**Total elapsed time: roughly one school year.** That is not slow — Phase 1 delivers most
of the risk reduction in the first month, and the remaining phases are gated on things that
genuinely take time (2SV adoption, vendor DKIM, instructional coordination).

| Phase | Focus | Duration | User impact |
| --- | --- | --- | --- |
| [0](#phase-0--baseline) | Baseline and inventory | 1–2 weeks | **None** |
| [1](#phase-1--quick-wins) | Quick wins | 2–3 weeks | Minimal |
| [2](#phase-2--2sv-and-oauth) | 2SV + OAuth lockdown | 6–8 weeks | **High** |
| [3](#phase-3--dmarc-ramp) | DMARC ramp | 8–12 weeks | None if done right, **severe if rushed** |
| [4](#phase-4--student-tightening-caa-dlp) | Students, CAA, DLP | 4–6 weeks | Moderate |
| [Ongoing](#ongoing-operations) | Operations | Forever | — |

> **Do not reorder.** Phase 1 before Phase 0 means changing settings you haven't baselined
> and can't prove improved anything. Phase 3 before its inventory breaks parent
> communication. Phase 4 before Phase 2 tightens students while staff accounts — the
> higher-value targets — are still soft.

---

## Phase 0 — Baseline

**Duration:** 1–2 weeks · **User impact:** none · **Can start today**

### Prerequisites
- Super admin access
- GAM installed and authorized (optional — [audit/gam/README.md](../audit/gam/README.md))
- Storage for audit output that is **not** this repo

### Do

- [ ] Fill in [config/district-profile.md](../config/district-profile.md) — **the gate for
      everything else**
- [ ] Review and correct [ASSUMPTIONS.md](../ASSUMPTIONS.md)
- [ ] Run the full GAM audit suite: `audit/gam/run-all.sh`
- [ ] **Security health page snapshot** — screenshot every section
      ([docs/08](../docs/08-monitoring-response.md) §4)
- [ ] Security dashboard snapshot — spam/phishing volume, external sharing, OAuth
- [ ] Export current Gmail Safety settings per OU (screenshots)
- [ ] Document current SPF, DKIM, DMARC records for **every** domain
- [ ] **Bulk-sender inventory** — the DMARC gate ([docs/09](../docs/09-dmarc-spf-dkim.md) §2)
- [ ] Enumerate POP/IMAP users, external forwarding, delegates
- [ ] Document existing allowlists — **and justify each or plan its removal**
      ([docs/01](../docs/01-gmail.md) §8)
- [ ] Name quarantine reviewers, backups, and break coverage
- [ ] Fill in the contact table in [playbooks/00-index.md](../playbooks/00-index.md)
- [ ] Confirm cyber insurance notification requirements and windows

### Success criteria
- Every audit script has produced output that has been *read*, not just generated
- The bulk-sender inventory has no blanks
- You can state today's baseline numerically: N staff without 2SV, N external forwarding
  rules, N super admins, N open groups

### Comms
None. Phase 0 is invisible.

---

## Phase 1 — Quick wins

**Duration:** 2–3 weeks · **User impact:** minimal

**This phase delivers the majority of the risk reduction in this package.** If the project
stalls after Phase 1, the district is still substantially better off.

### Prerequisites
- Phase 0 complete
- Quarantine reviewers named, with an SLA and break coverage
- **Bulk senders confirmed authenticating** — required before the domain-spoofing setting
  ([docs/01](../docs/01-gmail.md) §3 blast radius)

### Week 1 — no user impact

- [ ] **Alert center routing** to `<SECURITY_ALIAS>` + webhook
      ([docs/08](../docs/08-monitoring-response.md) §2)
- [ ] Enable the high-value alerts, including **settings-changed** alerts
- [ ] Set up admin quarantines ([docs/01](../docs/01-gmail.md) §9)
- [ ] **Super admin hardening** — reduce to 2–4, hardware keys, APP, separate daily drivers
      ([docs/06](../docs/06-accounts-mfa-admins.md) §5)
- [ ] **Calendar invitation control** ([docs/02](../docs/02-calendar.md) §2)
- [ ] Calendar external sharing → free/busy
- [ ] Enable security sandbox ([docs/01](../docs/01-gmail.md) §6)
- [ ] Links & external images all `On` ([docs/01](../docs/01-gmail.md) §4)
- [ ] Comprehensive mail storage `On`
- [ ] Default Drive link sharing → **Restricted** ([docs/03](../docs/03-drive.md) §2)
- [ ] **Remove existing broad allowlists** ([docs/01](../docs/01-gmail.md) §8)

### Week 2 — light user impact

- [ ] Gmail Safety attachments → `Quarantine` ([docs/01](../docs/01-gmail.md) §2)
- [ ] Gmail Safety spoofing/auth → `Quarantine`, incl. **employee-name** and **Groups**
      ([docs/01](../docs/01-gmail.md) §3)
- [ ] "Apply future recommended settings automatically" `On` everywhere
- [ ] **Groups org-wide policy** → admins-only creation, no external members/posting
      ([docs/04](../docs/04-groups.md) §2)
- [ ] **Tier 1 + Tier 2 group audit and lockdown** ([docs/04](../docs/04-groups.md) §3)
- [ ] `all-staff-senders@` created and applied ([docs/04](../docs/04-groups.md) §4)
- [ ] Warn for external recipients `On`

### Week 3 — needs comms

- [ ] Content compliance: cabinet display-name banner ([docs/01](../docs/01-gmail.md) §7.1)
- [ ] Content compliance: financial tripwire — **banner-only everywhere for one week**,
      then escalate Finance-HR to quarantine with real numbers
      ([docs/01](../docs/01-gmail.md) §7.2)
- [ ] Service hygiene sweep — announce two weeks ahead
      ([docs/05](../docs/05-other-services.md) §7)
- [ ] Drive: publish-to-web `Off` — **after** finding what's already public
      ([docs/03](../docs/03-drive.md) §3)

### Comms
[comms/01-phase1-staff-notice.md](../comms/01-phase1-staff-notice.md)

### Success criteria
- Quarantine reviewed daily within SLA; release rate under 20% per quarantine
- Zero broad allowlists remain
- Super admins: 2–4, all on hardware keys, all APP-enrolled
- Tier 1 and Tier 2 groups: no external posting, no external members
- Calendar invitation control set (or confirmed not yet rolled out to your tenant)
- Alert center backlog: zero unreviewed over 24h

### Rollback trigger
Quarantine release rate over 40% for a given setting → that setting is mis-tuned. Lower it
to `Move to spam`, investigate, re-escalate. **Do not abandon the control.**

---

## Phase 2 — 2SV and OAuth

**Duration:** 6–8 weeks · **User impact: high** — the hardest phase politically

### Prerequisites
- Phase 1 complete and stable for two weeks
- **Superintendent-level sponsorship, in writing.** Without it this phase stalls at the
  first complaint
- Help desk staffed for the volume, with a documented reset procedure
- Hardware keys purchased and received for high-risk roles
- **App request workflow live** ([docs/07](../docs/07-oauth-app-control.md) §5)
- App inventory complete, approved apps already marked Trusted

### Do

- [ ] Weeks 1–2: 2SV available, comms, drop-in sessions, **no enforcement**
- [ ] Week 3: targeted outreach to non-enrolled
- [ ] Week 4: **enforce for IT staff first** — dogfood the support burden
- [ ] Week 5: Finance-HR — **phishing-resistant methods only**
      ([docs/06](../docs/06-accounts-mfa-admins.md) §3)
- [ ] Weeks 6–7: enforce for all staff, **in school-sized waves**
- [ ] Week 6: API controls — block unconfigured apps from restricted scopes
      ([docs/07](../docs/07-oauth-app-control.md) §2)
- [ ] Week 6: Marketplace → allowlist mode
- [ ] Week 7: **domain-wide delegation audit** — record Client IDs and scopes before
      removing anything ([docs/07](../docs/07-oauth-app-control.md) §6)
- [ ] Week 8: POP/IMAP off for staff — after the migration notice
- [ ] Week 8: external forwarding off for staff and Finance-HR
- [ ] Login challenges on — **after** the employee ID field is populated
- [ ] Session length shortened for admins and Finance-HR **[Plus]**

### ⚠ Do not
- Enforce district-wide on a single day
- Enforce during the first two weeks of school or state testing
- Turn on API controls before the approved-app list is marked Trusted
- Remove a DWD grant without recording the Client ID and scopes

### Comms
[comms/02-phase2-2sv.md](../comms/02-phase2-2sv.md) ·
[comms/03-phase2-apps.md](../comms/03-phase2-apps.md)

### Success criteria
- 100% of active staff enrolled in 2SV
- 100% of admins and Finance-HR on **phishing-resistant** methods
- Zero unidentified DWD grants
- App request queue turning around within 10 business days
- No staff account with external forwarding

### Rollback trigger
Help desk cannot keep up → pause the wave schedule, don't reverse completed waves.
An instructional system broken by API controls → mark that specific app Trusted, don't
disable app controls wholesale.

---

## Phase 3 — DMARC ramp

**Duration:** 8–12 weeks · **User impact:** none if done right

> **This is the only phase that can break parent communication district-wide.**
> Read [docs/09](../docs/09-dmarc-spf-dkim.md) in full before starting.

### Prerequisites — all hard gates
- [ ] **Bulk-sender inventory 100% complete** — no blanks, no "probably"
- [ ] Every sender has a **named business owner**
- [ ] SPF under 10 lookups, single record, verified with a checker
- [ ] Google DKIM 2048-bit and authenticating on **every** domain
- [ ] **Every third-party sender DKIM-aligned — `d=` verified against From: domain**
- [ ] `dmarc@` mailbox created and **excluded from content compliance rules**
- [ ] parsedmarc (or alternative) running and readable
- [ ] `_dmarc` TTL lowered to 300s
- [ ] Vendors who cannot do DKIM identified and on a subdomain plan
      ([docs/09](../docs/09-dmarc-spf-dkim.md) §6)

### Do
Work the eight-stage ramp in [docs/09](../docs/09-dmarc-spf-dkim.md) §5.

- [ ] Parked and secondary domains → `p=reject` + `v=spf1 -all` + null MX **on day one**
- [ ] Stage 1 `p=none` — **14 days minimum, do not shorten**
- [ ] Stage 2 remediate — **100% aligned before advancing**
- [ ] Stages 3–5 quarantine, staged pct
- [ ] Stages 6–8 reject, staged pct

### Scheduling constraints
- **Advance on Tuesdays.** Never Fridays
- **Never** during: first two weeks of school, state testing, grade reporting, open
  enrollment, or a payroll week
- **Stage 5 must span a full mass-notification send and a payroll cycle** before advancing

### Comms
Mostly internal. Notify each bulk-sender owner of the timeline and their alignment deadline.
[comms/04-phase3-vendor-notice.md](../comms/04-phase3-vendor-notice.md)

### Success criteria
- `p=reject` on all sending domains
- Zero legitimate sources failing in `rua` reports for 30 consecutive days
- Every parked domain at `p=reject`
- No increase in parent "I didn't get the notification" reports

### Rollback trigger
**Any** legitimate mail flow breaking → drop `pct` or lower `p=` immediately. TTL is 300s,
so recovery is five minutes. **Then find the misaligned sender before re-advancing** — do
not simply retry.

---

## Phase 4 — Student tightening, CAA, DLP

**Duration:** 4–6 weeks · **User impact:** moderate

**Deliberately last.** Staff accounts are the higher-value target; tightening students first
optimizes the wrong thing. Also: student-facing changes need instructional coordination,
which takes lead time.

### Prerequisites
- Phases 1–2 complete
- **Instructional technology sign-off on every student-facing change**
- Guardian communication sent
- Help desk ready for student password volume

### Do

- [ ] Age designation verified for all student OUs
      ([docs/05](../docs/05-other-services.md) §1)
- [ ] Student external Drive sharing restricted — **allowlisted domains for high school**
      ([docs/03](../docs/03-drive.md) §2)
- [ ] Students: receive files from outside `Off`
- [ ] Student POP/IMAP and external forwarding `Off`
- [ ] Student Chat external `Off`; history admin-controlled
- [ ] Meet join scope domain-only
- [ ] Classroom membership domain-only both directions
- [ ] Takeout `Off` for students
- [ ] **Self-service password recovery `Off` for students**
      ([docs/06](../docs/06-accounts-mfa-admins.md) §9)
- [ ] Calendar invitation control → strictest tier for students
- [ ] **DLP rules in audit mode for 30 days**, then tune, then enforce
      ([docs/03](../docs/03-drive.md) §6) **[Standard]/[Plus]**
- [ ] **Context-Aware Access in monitor mode**, then enforce — Admin console first
      ([docs/06](../docs/06-accounts-mfa-admins.md) §8) **[Plus]**
- [ ] Trust rules for Drive ([docs/03](../docs/03-drive.md) §5) **[Standard]/[Plus]**
- [ ] BigQuery log export enabled ([docs/08](../docs/08-monitoring-response.md) §6)

### ⚠ Do not
- Enforce CAA without one super admin exempt and credentials in the safe
- Enforce DLP before 30 days of audit-mode data
- Apply student restrictions without instructional sign-off
- Apply geographic restrictions to students — the false-positive cost lands on the families
  least able to resolve it

### Comms
[comms/05-phase4-students.md](../comms/05-phase4-students.md) ·
[comms/06-phase4-guardians.md](../comms/06-phase4-guardians.md)

### Success criteria
- Student OU target state matches [docs/05](../docs/05-other-services.md) §8
- DLP enforcing with a manageable false-positive rate
- CAA enforced on the Admin console with no lockouts
- **No instructional workflow broken** — measured by asking teachers, not by absence of tickets

### Rollback trigger
Any instructional workflow broken → roll that setting back **same day**, then find a
narrower way to achieve the goal. This is the rule in [README.md](../README.md) and it is
not negotiable.

---

## Ongoing operations

### Cadence

| Task | Frequency | Owner | Reference |
| --- | --- | --- | --- |
| Alert center triage | Daily (school days) | Security admin | [08](../docs/08-monitoring-response.md) |
| Quarantine review | Daily, per SLA | Named reviewers | [01](../docs/01-gmail.md) §9 |
| App requests | Weekly | Tech dept | [07](../docs/07-oauth-app-control.md) §5 |
| Spam/phishing trend | Weekly | Security admin | [08](../docs/08-monitoring-response.md) §4 |
| **Security health page** | **Monthly** | Tech director | [08](../docs/08-monitoring-response.md) §4 |
| GAM audit suite + **diff vs last month** | Monthly | Security admin | [audit/gam](../audit/gam/README.md) |
| Forwarding/delegate audit | Monthly | Security admin | [audit/gam](../audit/gam/README.md) |
| **OAuth token + DWD audit** | **Quarterly** | Tech director | [07](../docs/07-oauth-app-control.md) §7 |
| Group settings audit | Quarterly | Security admin | [04](../docs/04-groups.md) §7 |
| Admin role review | Quarterly | Tech director | [06](../docs/06-accounts-mfa-admins.md) §5 |
| Cabinet name-rule refresh | Quarterly | Security admin | [01](../docs/01-gmail.md) §7.1 |
| Allowlist exception review | Quarterly | Tech director | [01](../docs/01-gmail.md) §8 |
| Service hygiene sweep | Quarterly | Tech dept | [05](../docs/05-other-services.md) §7 |
| Appointment schedule review | Per term | Security admin | [02](../docs/02-calendar.md) §5 |
| **Phishing simulation** | Quarterly | Tech dept + HR | below |
| **Tabletop exercise** | **2× per year** | Cabinet + IT | below |
| Package review vs current Google docs | Annually | Tech director | — |

### Phishing simulation — rules

- **Never punitive.** No discipline, no naming, no leaderboards of failure. The moment a
  simulation has consequences, real reporting stops
- Report the **report rate**, not just the click rate. Report rate is the metric that
  predicts real-incident outcomes
- Rotate scenarios against [docs/00-threat-landscape.md](../docs/00-threat-landscape.md):
  leadership impersonation, payroll, vendor invoice, QR code, Calendar invite
- Immediate, non-judgmental micro-training on click
- **Do not simulate sextortion or anything involving students.** Ever
- Coordinate with HR before each round — this touches employee relations

### Training rhythm

| Audience | Frequency | Focus |
| --- | --- | --- |
| All staff | Annually + at onboarding | Recognize, report, never punished |
| **Finance-HR** | **Quarterly** | Payroll diversion, invoice fraud, callback rule, AI-summary caution |
| Administrators | 2× per year | Impersonation, deepfakes, authorization discipline |
| IT staff | Quarterly | Playbooks, tooling, drills |
| Students | Annually, age-appropriate | Phishing, sextortion reporting, scams |
| **Guardians** | Annually | District will never ask X by email; how to verify |

### Tabletop exercises

Two per year, cabinet-level, 90 minutes. Rotate scenarios:

1. Superintendent impersonation → $40k gift card request nearly paid
2. Payroll diversion discovered on payday, 14 staff affected
3. Vendor invoice fraud, $180k wire sent
4. Ransomware via phished staff credential, SIS encrypted
5. Student data breach via a compromised ed-tech vendor
6. Deepfake voice of the CFO authorizing a transfer

**Test decisions and communication, not technical steps.** Who decides to notify parents?
Who talks to the press? Who calls the insurer? When does the board get told? Those are the
questions that go badly in a real incident, and they are free to rehearse.

### Annual review

- [ ] Re-verify every console path against current Google documentation — **paths move**
- [ ] Re-read [docs/00-threat-landscape.md](../docs/00-threat-landscape.md) against current
      MS-ISAC, K12 SIX, CISA, and IC3 reporting
- [ ] Review Workspace Updates for the last 12 months
- [ ] Resolve outstanding `[VERIFY]` tags
- [ ] Update [ASSUMPTIONS.md](../ASSUMPTIONS.md) against reality
- [ ] Re-baseline metrics against the Phase 0 snapshot — **this is what funds next year**
