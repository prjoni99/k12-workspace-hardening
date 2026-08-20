# 00 — Threat Landscape: What Is Actually Hitting K-12 Right Now

Research date **2026-08-20**. Every threat below maps to the specific controls in this
repo that mitigate it. If a threat has no control, that is stated plainly rather than
papered over.

## Why the K-12 threat model is its own thing

Three structural facts make districts different from a same-sized business:

1. **The org chart is public.** Superintendent, principals, CFO, board members, their
   titles, their photos, often their direct email — all published on the district site by
   law or by convention. Attackers do not need reconnaissance; they need a browser.
2. **Guardians are external users who must stay reachable.** A business can block or
   heavily restrict external mail and sharing. A district cannot — that is the parent
   communication channel. Every control here is shaped by that constraint.
3. **Minors are account holders.** Students are targets for categories (sextortion,
   grooming, scholarship fraud) that have no enterprise analogue, and student accounts
   are a lateral-movement path into staff mailboxes.

Baseline volume: **82% of reporting K-12 organizations experienced cyber threat impacts**
between July 2023 and December 2024, across more than 8,100 confirmed incidents
([CIS/MS-ISAC K-12 report, via K12 SIX](https://www.k12six.org/)). In the first half of
2026 there were **34 ransomware attacks** against US K-12 and higher-ed institutions
([Sedara, 2026](https://www.sedarasecurity.com/k-12-cybersecurity-in-2026-what-districts-need-to-watch-plan-for-and-prove/)).

---

## T1 — AI-written leadership impersonation (gift card / wire / "are you at your desk")

**How it runs.** Attacker scrapes the district website for the superintendent's or a
principal's name, title, and writing style, then sends from a free webmail account with
the *display name* set to that person. Opening line is low-commitment — "Are you at your
desk?", "I need a quick favor, I'm in a board meeting" — to elicit a reply before any
ask. The ask follows: gift cards, a wire, a "confidential" purchase. Generative AI removed
the grammatical tells that used to make these obvious, and lets the attacker match tone
from published newsletters and board minutes.

**Why it beats filters.** There is no spoofed domain to catch. `principal.name@gmail.com`
is a real, authenticated Gmail account that passes SPF, DKIM, and DMARC perfectly. The
only anomaly is the display name.

**Controls:**
- **Protect against spoofing of employee names** → `Quarantine` for staff.
  The single highest-value setting in this repo — [docs/01-gmail.md](01-gmail.md) §3
- Display-name content compliance rule for cabinet/principal roles —
  [docs/01-gmail.md](01-gmail.md) §7
- Keyword tripwires: "gift card", "wire transfer", "are you at your desk" from external
  senders — [docs/01-gmail.md](01-gmail.md) §7
- Groups locked so one message can't reach all staff — [docs/04-groups.md](04-groups.md)
- Out-of-band verification procedure — [playbooks/04-payroll-diversion-attempt.md](../playbooks/04-payroll-diversion-attempt.md)

---

## T2 — Payroll / direct-deposit diversion

**How it runs.** Staff member receives a spoofed HR or self-service-portal message:
"annual direct deposit verification", "your payroll profile needs re-confirmation".
Credentials are harvested, the attacker signs into the SIS/ERP employee portal and
changes the deposit routing number, usually to a prepaid debit account. Discovery happens
on payday — one full cycle later. Frequently the mailbox is also configured with a filter
that auto-archives anything containing "direct deposit" so the confirmation email is never
seen.

Attackers move from stolen credentials to payroll changes as a routine escalation path
([SENKI payroll diversion analysis](https://www.senki.org/payroll-diversion-fraud/)).

**Controls:**
- Phishing-resistant 2SV (passkey/security key) required for Finance-HR —
  [docs/06-accounts-mfa-admins.md](06-accounts-mfa-admins.md) §3
- "direct deposit" / "routing number" keyword tripwire — [docs/01-gmail.md](01-gmail.md) §7
- External forwarding disabled for Finance-HR — [docs/01-gmail.md](01-gmail.md) §5
- Filter/forwarding/delegate audit — [audit/gam/02-forwarding-and-filters.sh](../audit/gam/02-forwarding-and-filters.sh)
- **Non-Workspace control that matters more than any of the above:** the payroll system
  must require out-of-band verification for any banking change. Documented as a hand-off
  in [playbooks/04-payroll-diversion-attempt.md](../playbooks/04-payroll-diversion-attempt.md).

---

## T3 — Vendor email compromise / invoice fraud

**How it runs.** A real vendor's mailbox is compromised. The attacker reads the existing
thread with district AP, then replies **in that thread** with updated remittance details.
Everything authenticates because it genuinely is the vendor's account. This is the highest
per-incident loss category in K-12 — phishing against accounts-payable staff has produced
some of the largest direct financial losses districts have experienced
([K-12 Cybersecurity Resource Center](https://k12cybersecure.com/tag/phishing/)).

**Why most controls fail here.** SPF/DKIM/DMARC all pass. Display name is correct. Domain
is correct. Thread history is real. **No email authentication control detects this.**

**Controls:**
- Banking-change keyword tripwire on external mail — [docs/01-gmail.md](01-gmail.md) §7
- Finance-HR OU with tighter everything — [docs/01-gmail.md](01-gmail.md), [docs/06](06-accounts-mfa-admins.md)
- **Primary mitigation is a business process, not a setting:** callback verification to a
  vendor phone number *on file from before the request*, never a number in the email —
  [playbooks/05-vendor-invoice-fraud.md](../playbooks/05-vendor-invoice-fraud.md)

---

## T4 — Credential phishing with AiTM proxy kits (MFA-defeating)

**How it runs.** Kits like **Tycoon 2FA** run a reverse proxy between the victim and the
real Google sign-in page. The victim sees a genuine Google login (because it *is* one,
proxied), enters a password, completes the 2SV challenge — and the kit captures the
resulting **session cookie**. The attacker replays the cookie and is inside the account
without ever needing the password or a second factor again.

Tycoon 2FA at peak accounted for roughly **62% of phishing attempts blocked by Microsoft**,
reaching over 500,000 organizations monthly. A March 2026 takedown led by Microsoft and
Europol seized 300+ domains, **but operators adapted and the technique persists**
([Group-IB](https://www.group-ib.com/masked-actors/tycoon2fa/),
[Bridewell](https://www.bridewell.com/insights/blogs/detail/the-rise-and-fall-of-tycoon-2fa-inside-the-mfa-bypassing-phishing-empire)).
Google's own June 2026 advisory lists AiTM first among current threats
([Google](https://blog.google/innovation-and-ai/technology/safety-security/fraud-scams-advisory-june-2026/)).

**The load-bearing fact for this entire package:** *SMS, TOTP, and push MFA are all
proxyable.* **FIDO2 security keys and passkeys are the only methods immune to AiTM session
theft** ([Proofpoint](https://www.proofpoint.com/us/blog/email-and-cloud-threats/tycoon-2fa-phishing-kit-mfa-bypass)).
This is why [docs/06](06-accounts-mfa-admins.md) treats "we have MFA" as insufficient for
admins and finance, and why "2SV enforced" is a Phase 2 milestone rather than the finish
line.

**Controls:**
- Phishing-resistant 2SV for super admins, Finance-HR, payroll-touching roles —
  [docs/06-accounts-mfa-admins.md](06-accounts-mfa-admins.md) §3
- Advanced Protection Program for super admins — [docs/06](06-accounts-mfa-admins.md) §4
- Shorter session length for admins/finance (shrinks stolen-cookie value) — [docs/06](06-accounts-mfa-admins.md) §7
- Context-Aware Access on Admin console — [docs/06](06-accounts-mfa-admins.md) §8 **[Plus]**
- Link warning for untrusted domains — [docs/01-gmail.md](01-gmail.md) §4
- "Suspicious login" and "Leaked password" alerts — [docs/08](08-monitoring-response.md) §2
- Token revocation is mandatory in compromise response — a password reset alone does
  **not** invalidate a stolen session — [playbooks/01-compromised-staff-account.md](../playbooks/01-compromised-staff-account.md)

---

## T5 — QR-code phishing (quishing), including physical flyers

**How it runs.** The malicious URL is rendered as an image, so URL-based filtering has
nothing to scan. The victim scans with a **personal phone** — off the district network,
outside district DNS filtering, off any managed browser policy. Physical variants exist:
QR flyers taped in staff lounges, on parking notices, or over legitimate codes on
book-fair and fundraiser posters.

**Quishing rose 146% in Q1 2026**, with ~18.7 million incidents in March alone; 12–12.4%
of all phishing now uses image-based payloads. Small and midsize organizations — the
district size band — see **up to 19× more QR attacks** than large enterprises
([Acronis](https://www.acronis.com/en/blog/posts/qr-code-phishing-evasive-threats-2026/),
[AP via Watauga Democrat](https://www.wataugademocrat.com/ap/state/quishing-surges-146-in-q1-2026-as-attackers-hide-behind-the-code/article_121840ac-c8d4-5e08-8c97-7cadd00ed686.html)).

**Controls (partial — be honest about this one):**
- **Scan linked images** `On` — [docs/01-gmail.md](01-gmail.md) §4
- Phishing-resistant 2SV makes a harvested credential far less useful — [docs/06](06-accounts-mfa-admins.md) §3
- **No Workspace setting mitigates a QR code taped to a wall.** That is training and
  physical-space awareness — [checklists/rollout-phases.md](../checklists/rollout-phases.md)
  "Ongoing", plus the reporting culture in [docs/08](08-monitoring-response.md) §7.

---

## T6 — Calendar-invite phishing

**How it runs.** Attacker sends a Google Calendar invitation with a malicious link in the
event body or location field. Historically Calendar **auto-added invitations from anyone**,
so the malicious event appeared on the victim's calendar without any click — complete with
a notification and a reminder. A variant *cancels* the event, because cancellation notices
also carry attacker-supplied text. Check Point observed one campaign hitting **300 brands
with 4,000+ emails in four weeks**; the invites **passed DKIM, SPF, and DMARC** because
they genuinely originated from Google
([BleepingComputer](https://www.bleepingcomputer.com/news/security/ongoing-phishing-attack-abuses-google-calendar-to-bypass-spam-filters/)).
Google's June 2026 advisory documents fake renewal notices delivered directly as Calendar
invites ([Google](https://blog.google/innovation-and-ai/technology/safety-security/fraud-scams-advisory-june-2026/)).

**What changed, and it is recent.** On **2026-08-14** Google began rolling out admin-level
control over invitation handling, settable per OU or group. It **defaults to "From
everyone"** — the permissive behavior — so this does nothing until a district changes it
([Workspace Updates, 2026-08-14](https://workspaceupdates.googleblog.com/2026/08/new-admin-controls-for-adding-invitations-to-Google-Calendar.html)).

**Controls:**
- Invitation control set to known-senders at admin level — [docs/02-calendar.md](02-calendar.md) §2
- External sharing limited to free/busy — [docs/02-calendar.md](02-calendar.md) §3
- Bulk cleanup of already-delivered calendar spam — [playbooks/06-mass-calendar-spam-cleanup.md](../playbooks/06-mass-calendar-spam-cleanup.md)

---

## T7 — Abuse of legitimate Google services to pass authentication

**How it runs.** The lure is hosted *on Google*. Google Forms, Google Drawings, Google
Sites, Drive share notifications, Google Groups invitations, Google Tasks. The notification
email is genuinely from Google, authenticates cleanly, and comes from trusted Google
infrastructure — so domain reputation, SPF, DKIM, and DMARC are all working exactly as
designed and all of them say "legitimate."

Documented chains: Calendar invite → Google Forms or Drawings → fake reCAPTCHA/support
button → credential harvest ([Abnormal](https://abnormal.ai/attack-library/google-calendar-invite-phishing-google-drawings)).
A late-2025 campaign abused **Google Tasks** to generate authentic Google notification
emails that bypassed email security entirely
([Optery](https://www.optery.com/data-privacy-week-and-google-tasks-abuse/)). Google's
June 2026 advisory names "reputation bypass" — hosting payloads on trusted cloud
properties — as a current tactic, alongside ClickFix lures served from Google Sites.

**Why this is structurally hard.** You cannot block Google notifications inside Google
Workspace without breaking Workspace. The mitigation is to shrink the *services* that can
be abused and to catch the *destination*, not the sender.

**Controls:**
- Turn OFF unused Google services per OU — the service-hygiene sweep. AppSheet is the
  standard example: if the district doesn't use it, it is pure attack surface —
  [docs/05-other-services.md](05-other-services.md) §7
- Link warning for untrusted domains — [docs/01-gmail.md](01-gmail.md) §4
- Drive share-notification handling and external Drive warnings — [docs/03-drive.md](03-drive.md)
- Calendar invitation control — [docs/02-calendar.md](02-calendar.md) §2
- Groups locked against external posting — [docs/04-groups.md](04-groups.md)
- Post-delivery purge when one lands — [playbooks/03-post-delivery-phish-purge.md](../playbooks/03-post-delivery-phish-purge.md)

> **`[VERIFY]`** — I did not find current reporting specifically documenting AppSheet
> abuse in phishing chains, despite it being named in the source brief. It is recommended
> here on **attack-surface-reduction grounds** (an unused service with data access and
> app-publishing capability), not because a campaign is documented. Do not cite an
> AppSheet campaign to leadership; cite the general reputation-bypass pattern instead.

---

## T8 — Compromised trusted-partner accounts

**How it runs.** Another district, an ed-tech vendor, a state agency, a regional
consortium — a mailbox there is compromised, and the phish arrives from a real, trusted,
fully-authenticating account, often into an established thread. Districts trust each other
by convention; a message from a neighboring district's technology director carries
enormous implicit credibility.

**Why authentication controls do nothing.** SPF, DKIM, and DMARC all pass. They are
supposed to. The sender is who they claim to be — they are just not in control of the
account.

**Controls:**
- Security sandbox detonates attachments regardless of sender reputation —
  [docs/01-gmail.md](01-gmail.md) §6 **[Standard/Plus]**
- Link warning for untrusted domains — [docs/01-gmail.md](01-gmail.md) §4
- **The anti-control:** allowlisting partner districts or vendors to "stop the false
  positives" converts this from survivable to catastrophic. Explicitly forbidden —
  [docs/01-gmail.md](01-gmail.md) §8
- Post-delivery purge — [playbooks/03-post-delivery-phish-purge.md](../playbooks/03-post-delivery-phish-purge.md)

---

## T9 — Student account takeover and student-to-student phishing

**How it runs.** Two distinct patterns. **External:** a student credential is phished
(often via a game, "free V-Bucks", or a fake Classroom notification) and the account
becomes a foothold *inside* the domain — internal mail from a real student account
bypasses every external-sender control the district has. **Internal:** students phish each
other directly, for social reasons (impersonation, harassment) or to reach a teacher
account and alter grades.

The internal case is under-modeled in most districts: every "external sender" warning,
every content-compliance rule scoped to external mail, and the entire DMARC apparatus is
blind to a message from one real student to another.

**Controls:**
- Student external forwarding and POP/IMAP off — [docs/01-gmail.md](01-gmail.md) §5
- Student Chat restricted to internal — [docs/05-other-services.md](05-other-services.md) §2
- Classroom membership restricted to domain — [docs/05](05-other-services.md) §4
- Self-service password recovery **disabled** for students (admin-mediated resets) —
  [docs/06-accounts-mfa-admins.md](06-accounts-mfa-admins.md) §9
- Takeout off for students — [docs/05](05-other-services.md) §6
- Student Drive sharing domain-restricted — [docs/03-drive.md](03-drive.md)
- [playbooks/02-compromised-student-account.md](../playbooks/02-compromised-student-account.md)

---

## T10 — Scams targeting students directly: sextortion and scholarship fraud

**How it runs.** **Financially-motivated sextortion** is the acute one. NCMEC received
**more than 50,000 reports in 2025 — ~137 per day**, up from 36,000 in 2024. The FBI and
NCAA issued a joint warning for student-athletes, who face compounded pressure from
scholarship and sponsorship exposure. Critically, **complying with demands does not stop
distribution — it reliably produces more demands**
([FBI](https://www.fbi.gov/news/press-releases/fbi-and-partners-warn-student-athletes-of-sexual-exploitation-schemes),
[IC3 PSA 260810](https://www.ic3.gov/PSA/2026/PSA260810)).

**Scholarship and student-aid fraud:** FinCEN issued alert **FIN-2026-Alert004
(2026-07-24)** on fraud rings using stolen identities to enroll and extract federal
student aid ([FinCEN](https://www.fincen.gov/system/files/2026-07/FinCEN-Alert-Fraud-Schemes-Targeting-Federal-Student-Aid.pdf)).
This lands on graduating seniors and their families.

**Controls — and the honest limit.** Almost none of this is a Workspace setting. Most
sextortion contact happens on platforms the district does not control (Instagram, Discord,
Snapchat, gaming voice chat), on personal devices, after hours.

What the district *can* do:
- Student Chat external off, Meet join controls — [docs/05](05-other-services.md) §2–3
- A **reporting path a 15-year-old will actually use** — this is the control that
  matters. Reporting to `<ABUSE_ALIAS>` must be non-punitive and must not require
  telling a parent first. Documented in [docs/08](08-monitoring-response.md) §7.
- Counselor and SRO escalation path, and the national reporting routes
  (`ncii.ic3.gov`, `tips.fbi.gov`, 1-800-CALL-FBI) — belongs in student services
  procedure, referenced from [docs/08](08-monitoring-response.md) §7.

> This is a student-safety issue that happens to touch IT. Do not let it sit only with IT.

---

## T11 — Ransomware / data extortion, with phishing as initial access

**How it runs.** Phishing is the front door; the damage is everything after it. Credential
theft → mailbox access → lateral movement → data staging → encryption and/or extortion
publication. Ed-tech vendor breaches provide a parallel path: the district's student data
is exfiltrated from a *vendor's* environment, and the district still owns the notification
obligation and the reputational damage.

34 ransomware attacks hit US K-12 and higher-ed in the first half of 2026 alone
([Sedara](https://www.sedarasecurity.com/k-12-cybersecurity-in-2026-what-districts-need-to-watch-plan-for-and-prove/)).

**Controls in this package (initial access only):** everything in T1–T9 — this package
narrows the front door.

**Where this package hands off — and these are not optional:**
- Endpoint detection and response
- Network segmentation, especially SIS/finance away from instructional VLANs
- **Offline, tested, immutable backups** — the only control that reliably beats encryption
- Ed-tech vendor risk review and data processing agreements
- Cyber insurance requirements and their control preconditions
- Incident response retainer and district legal/comms plan
- Emergency operations planning integration — CISA and the Department of Education now
  treat K-12 cyber as part of EOP, not an IT-only concern
  ([CISA K-12 toolkit](https://www.cisa.gov/topics/cybersecurity-best-practices/K12cybersecurity/online-toolkit-partnering-safeguard-k-12-organizations-cybsecurity-threats))

**Response controls that are here:** Vault retention supporting IR, BigQuery log export
for long-retention forensics, investigation tool workflows —
[docs/08-monitoring-response.md](08-monitoring-response.md).

---

## T12 — MFA fatigue and deepfake voice/video of leadership

**MFA fatigue (push bombing):** attacker with a valid password triggers repeated push
prompts until the user approves one to make it stop. **Mitigated structurally** by
phishing-resistant methods — a passkey has nothing to approve out of context
([docs/06](06-accounts-mfa-admins.md) §3). If the district uses push-based 2SV anywhere,
this is live.

**Deepfake voice/video:** synthesized audio of the superintendent calling a finance staffer,
or a video-call presence in a "quick approval" meeting. Google's June 2026 advisory
documents adjacent "digital arrest" video-call fraud where attackers impersonate officials
over live video ([Google](https://blog.google/innovation-and-ai/technology/safety-security/fraud-scams-advisory-june-2026/)).

**Controls — this one is almost entirely non-technical.** No Workspace setting detects a
synthesized voice.
- Meet join controls limit who reaches a district meeting — [docs/05](05-other-services.md) §3
- **The actual mitigation is a procedural rule:** financial authorization never completes
  on voice or video alone. A pre-agreed callback to a known number, or in-person
  confirmation, is required for any funds movement or banking change regardless of how
  convincing the requester is —
  [playbooks/04-payroll-diversion-attempt.md](../playbooks/04-payroll-diversion-attempt.md),
  [playbooks/05-vendor-invoice-fraud.md](../playbooks/05-vendor-invoice-fraud.md)
- Tell staff explicitly that leadership will **never** ask for gift cards, wires, or
  banking changes by phone, video, or email. A pre-authorized "it's okay to say no to the
  superintendent" is a security control — [comms/](../comms/)

---

## Coverage matrix

| # | Threat | Primary control | Doc | Residual risk |
| --- | --- | --- | --- | --- |
| T1 | Leadership impersonation | Employee-name spoofing → Quarantine | [01](01-gmail.md) | Low |
| T2 | Payroll diversion | Phishing-resistant 2SV + keyword tripwire | [06](06-accounts-mfa-admins.md), [01](01-gmail.md) | Med — needs payroll process change |
| T3 | Vendor invoice fraud | Keyword tripwire only | [01](01-gmail.md) | **High — process control required** |
| T4 | AiTM credential phishing | Passkeys/security keys + APP | [06](06-accounts-mfa-admins.md) | Low *if* phishing-resistant; High if OTP |
| T5 | QR-code phishing | Scan linked images + 2SV | [01](01-gmail.md) | **High — physical vector uncontrolled** |
| T6 | Calendar-invite phishing | 2026-08-14 invitation control | [02](02-calendar.md) | Low once enforced |
| T7 | Google-service abuse | Service hygiene + link warnings | [05](05-other-services.md) | Med — structural |
| T8 | Trusted-partner compromise | Sandbox + link warnings | [01](01-gmail.md) | **High — authenticates cleanly** |
| T9 | Student ATO / internal phish | Student OU restrictions | [01](01-gmail.md), [05](05-other-services.md) | Med — internal mail unfiltered |
| T10 | Sextortion / scholarship scams | Reporting path + Chat limits | [08](08-monitoring-response.md) | **High — mostly off-platform** |
| T11 | Ransomware initial access | All of T1–T9 | all | Med — hands off to EDR/backup |
| T12 | MFA fatigue / deepfakes | Passkeys + procedural rules | [06](06-accounts-mfa-admins.md) | Med — procedure-dependent |

**Read the residual-risk column honestly.** Four threats stay High after every control in
this repo is applied. Three of those four (T3, T5, T10) are only closable by process and
training, not configuration. Presenting this package to the cabinet as "we fixed phishing"
would be false; presenting it as "we closed the configurable gaps and here are the three
that need people" is accurate — see [docs/10-exec-summary.md](10-exec-summary.md).
