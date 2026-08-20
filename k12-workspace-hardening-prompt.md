# PROMPT — paste everything below this line into Claude Code in an empty repo

You are acting as a senior K-12 Google Workspace security engineer. Build a complete, current, actionable anti-phishing hardening package for a public school district running **Google Workspace for Education Plus**. The output is a documentation + audit repo that a district IT team can execute setting-by-setting.

## Context (fill in before running)

- District: [DISTRICT NAME], primary domain: [DOMAIN], secondary domains: [LIST OR NONE]
- Scale: ~[N] staff, ~[N] students
- OU structure: [e.g., /Staff, /Staff/Finance-HR, /Students/<school>, /Shared Devices, /Service Accounts — describe yours]
- Mail flow: Gmail direct MX [YES/NO — if a third-party gateway/filter exists, name it]
- Bulk senders that send AS the district domain (SIS, mass-notification like SchoolMessenger/ParentSquare, LMS, food service, copiers/scanners, SMTP relay users): [LIST — critical for DMARC work]
- GAM7 / GAMADV-XTD3 configured with super admin: [YES/NO]
- Optional self-hosted tooling available (Docker host for parsedmarc, etc.): [YES/NO]
- Compliance: FERPA/COPPA. Parents/guardians are EXTERNAL users — staff↔parent email and sharing must keep working. Student-facing restrictions must not break instruction.

## Step 1 — Research first (mandatory, use WebSearch/WebFetch)

Before writing anything, pull current information as of today's date from these sources, and cite them inline throughout the docs:

- Google Admin Help (support.google.com/a) — verify every Admin console path and setting name you reference. Paths move; do not trust memory. If a setting has moved or no longer exists, say so explicitly instead of guessing.
- Google Workspace Updates blog (workspaceupdates.googleblog.com) — anything shipped in the last 12 months affecting Gmail safety, Calendar invitations, Drive sharing, Groups, or admin controls. In particular verify the 2026 admin-level control restricting Calendar invitation auto-add to known senders.
- Google for Education edition matrix — confirm which features require Education Plus vs Education Standard vs Fundamentals. Label every premium feature with its required edition.
- CISA K-12 resources, MS-ISAC / K12 SIX publications, FBI IC3 alerts — current phishing/scam campaigns targeting school districts.
- Recent reporting on Google-service-abuse phishing (Calendar invite phishing, Google Forms/Drawings lures, AppSheet abuse, Drive share-notification spam, AiTM phishing kits such as Tycoon 2FA that defeat OTP-based MFA).

## Step 2 — Deliverables

Create this repo. Work from a todo list. One commit per numbered deliverable, conventional commit messages. Do not ask me questions — make reasonable assumptions and log every one in `ASSUMPTIONS.md`.

1. `README.md` + `CLAUDE.md` — repo conventions. Every recommended setting in every doc MUST include: (a) exact current Admin console path, (b) recommended value per OU (Staff / Students / Finance-HR / Admins), (c) required edition, (d) user impact + comms note, (e) rollback, (f) source URL.
2. `docs/00-threat-landscape.md` — current phishing/scam catalog targeting K-12, each mapped to the specific control(s) in this repo that mitigate it. Minimum coverage:
   - AI-written superintendent/principal impersonation (gift card, wire, "are you at your desk" lures) using real details scraped from district sites
   - Payroll / direct-deposit diversion targeting staff via spoofed HR
   - Vendor email compromise / invoice fraud against finance
   - Credential phishing incl. AiTM proxy kits that defeat SMS/OTP MFA
   - QR-code phishing (email + physical flyers) and SMS/voice multi-vector campaigns
   - Calendar-invite phishing (auto-added events with malicious links)
   - Abuse of legitimate Google services (Forms, Drawings, Drive share notifications, Groups, AppSheet) to pass authentication and filters
   - Compromised trusted-partner accounts (other districts, vendors) — passes SPF/DKIM/DMARC
   - Student account takeover and student-to-student internal phishing
   - Scholarship/job scams and sextortion targeting students
   - Ransomware/data-extortion initial access via phishing; ed-tech vendor breaches as an entry point
   - MFA fatigue, deepfake voice/video of leadership
3. `docs/01-gmail.md` — the core. Minimum coverage, all verified against current docs:
   - Apps > Google Workspace > Gmail > Safety: every Attachments, Links & external images, and Spoofing & authentication control set to strongest sensible action (quarantine for high-confidence spoofing/anomalous attachments; warn where quarantine breaks workflows). Enable "Apply future recommended settings automatically." Explicitly cover employee-name spoofing protection (the superintendent-impersonation killer) and groups spoofing.
   - Security sandbox + rules (Ed Standard/Plus) — enable, note OU targeting
   - Enhanced pre-delivery message scanning
   - Admin quarantines: set up, who reviews, SLA
   - End-user access: disable POP/IMAP where not needed (students), restrict automatic forwarding to external addresses (students + Finance-HR at minimum)
   - Comprehensive mail storage on
   - Content compliance ideas: warning-banner injection on external mail whose display name matches cabinet/principal names; keyword tripwires ("gift card", "direct deposit", "wire") from external senders routed to quarantine or banner
   - Hard rule: NO broad IP/domain allowlists that bypass spam classification; document the narrow exceptions process
   - Hosted S/MIME: note availability by edition, take-it-or-leave-it recommendation
4. `docs/02-calendar.md` — external sharing of primary calendars limited to free/busy; warnings for external invitations; the invitation auto-add / known-senders control enforced at admin level (verify current location and exact behavior — this is a 2026 change); end-user guidance for "Only if the sender is known"; appointment schedule exposure review; cleanup steps for calendar spam already delivered.
5. `docs/03-drive.md` — per-OU sharing (students: domain-only or allowlisted domains; staff: allowed with warnings so parent communication survives); default link access Restricted; shared drive creation controls; trust rules (Standard/Plus) for granular cases; DLP rules for SSNs/sensitive data (note edition); third-party Drive app access; malicious-file handling and investigation-tool remediation of exposed files.
6. `docs/04-groups.md` — who can create groups (admins only); all-staff and school-wide lists locked to internal, authorized senders with moderation for anything external; audit of existing group posting permissions (this is the single control that stops one spoofed email from hitting every employee); directory visibility.
7. `docs/05-other-services.md` — Chat (external chat off for students), Meet join controls, Classroom membership restricted to domain, Gemini access by OU with a note on prompt-injection-style email abuse, Takeout off for students, and a service-hygiene pass: turn OFF unused Google services per OU (AppSheet if unused, etc.) to shrink attack surface.
8. `docs/06-accounts-mfa-admins.md` — 2SV enforcement for all staff with enrollment window; phishing-resistant methods (passkeys/security keys) required for super admins, Finance-HR, and payroll-touching roles, with explicit reasoning that OTP/push is proxyable by AiTM kits; Advanced Protection Program for super admins; super admin hygiene (2–4 dedicated accounts, hardware keys, no daily-driver use, locked-down recovery); login challenges; session lengths (shorter for admins/finance); password policy; disable self-service recovery for student OUs (admin-mediated resets); Context-Aware Access (Ed Plus) restricting Admin console and sensitive apps to district networks/managed devices.
9. `docs/07-oauth-app-control.md` — Security > API controls: app access control with trusted-app allowlisting, blocking unconfigured third-party apps from sensitive scopes; the under-18 confirmed-apps requirement and a teacher app-request workflow; Marketplace allowlist mode; quarterly review of granted tokens; domain-wide delegation audit (highest blast radius in the domain).
10. `docs/08-monitoring-response.md` — Alert center rules routed to a monitored address/webhook; the high-value predefined alerts (leaked password, suspicious login, gov-backed attack, phishing detected post-delivery, user-reported phishing); activity rules (Standard/Plus) for auto-alert/auto-remediate patterns; security dashboard + security health page review cadence; investigation tool workflows including bulk post-delivery purge of a phish from all inboxes; email log search forensics; BigQuery log export (Standard/Plus) as optional long-retention pipeline; Vault retention supporting IR; encourage-the-report-button culture.
11. `docs/09-dmarc-spf-dkim.md` — inventory of everything sending as [DOMAIN] (from Context above — SIS, mass-notification, copiers, relay); SPF consolidation under 10 lookups; DKIM 2048 for Gmail AND every third-party bulk sender; DMARC ramp plan none → quarantine (pct staged) → reject over 60–90 days with rua monitoring; parsedmarc self-hosted option (Docker compose snippet) or hosted alternatives; explicit warning that enforcing before third-party senders are aligned breaks parent communication.
12. `playbooks/` — numbered, 2am-executable: compromised staff account (reset, sign out everywhere, revoke OAuth tokens + app passwords, check filters/forwarding/delegates/send-as, investigation-tool purge of anything it sent, notify); compromised student account; post-delivery phish purge via investigation tool; payroll-diversion attempt (out-of-band verification, finance process hooks); vendor invoice fraud; mass calendar spam cleanup; lookalike-domain response.
13. `audit/gam/` — read-only GAM7 audit scripts with a README: users without 2SV enforcement, external forwarding + forwarding addresses, delegates, OAuth tokens, app-specific passwords, group posting/join/external-member settings, admin role assignments, per-OU service on/off state. Keep any write/remediation commands in a clearly separated `audit/gam/remediation/` with warnings. If GAM=NO in Context, still generate them but mark optional.
14. `checklists/rollout-phases.md` — Phase 0 baseline (GAM exports + security health snapshot); Phase 1 no-user-impact quick wins (Gmail safety max, sandbox, groups lockdown, calendar known-senders, alert routing, admin account hardening); Phase 2 staff 2SV enforcement + OAuth lockdown with request workflow; Phase 3 DMARC ramp; Phase 4 student tightening + CAA + DLP; Ongoing ops cadence (monthly security health, quarterly OAuth/token audit, phishing sims + training rhythm, 2x/yr tabletop). Each phase: prerequisites, comms templates for staff, success criteria.
15. `docs/10-exec-summary.md` — one page, cabinet-ready: the threat picture, what we're changing, what it costs users, what it prevents. No jargon.

## Rules

- Never recommend allowlisting/bypassing spam filtering broadly. Never weaken a default.
- Label every Ed Plus / Ed Standard-only feature; provide the Fundamentals-tier fallback where one exists.
- Student OUs default stricter than staff; staff settings must preserve parent/guardian communication.
- Every console path verified against a current Google support article, cited inline. Anything you cannot verify gets flagged `[VERIFY]`, not invented.
- Tables for settings: Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source.
- Flag any recommendation that could break SIS integrations, copier scan-to-email, or third-party relays before it appears in a rollout phase.

Start by writing the todo list, then ASSUMPTIONS.md, then work the deliverables in order.
