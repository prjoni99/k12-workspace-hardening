# 01 — Gmail

The core document. Research date **2026-08-20**.

All Gmail settings live under `Admin console > Apps > Google Workspace > Gmail` and
require the **Gmail Settings** administrator privilege
([source](https://knowledge.workspace.google.com/admin/gmail/advanced/advanced-phishing-and-malware-protection)).

**Read §8 before you touch anything else.** It is the rule that prevents the most common
self-inflicted K-12 email security failure.

---

## 1. Order of operations

Do these in order. §2–4 are no-user-impact and can ship the same day. §7 needs comms.

| Step | Section | User impact | Phase |
| --- | --- | --- | --- |
| 1 | Turn on all Safety protections at default action | None (warnings only) | 0 |
| 2 | Escalate spoofing/auth to Quarantine (§3) | Quarantine review workload begins | 1 |
| 3 | Escalate attachments to Quarantine (§2) | Some legitimate attachments delayed | 1 |
| 4 | Links & images (§4) | Click-through warning appears | 1 |
| 5 | Security sandbox (§6) | Delivery delay on attachments | 1 |
| 6 | Quarantine operations stood up (§9) | Requires named reviewers + SLA | 1 |
| 7 | End-user access lockdown (§5) | **Breaks POP/IMAP clients — check first** | 1–4 |
| 8 | Content compliance rules (§7) | Banners appear on external mail | 1 |

> **Do not enable quarantine actions before §9 exists.** A quarantine nobody reviews is
> a mail outage with extra steps.

---

## 2. Safety — Attachments

**Path:** `Admin console > Apps > Google Workspace > Gmail > Safety > Attachments`
**Edition:** All, including **[Fundamentals]**
**Available actions:** `Keep in inbox + warning` (default) · `Move to spam` · `Quarantine`
([source](https://knowledge.workspace.google.com/admin/gmail/advanced/advanced-phishing-and-malware-protection))

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Protect against encrypted attachments from untrusted senders | Gmail > Safety > Attachments | Quarantine | Quarantine | Quarantine | Quarantine | All | Password-protected ZIPs held. Legitimate use is rare and almost always a vendor sending student data badly — which is its own problem | [ref](https://knowledge.workspace.google.com/admin/gmail/advanced/advanced-phishing-and-malware-protection) |
| Protect against attachment with scripts from untrusted senders | Gmail > Safety > Attachments | Quarantine | Quarantine | Quarantine | Quarantine | All | `.js`, `.vbs`, macro-bearing files held. No legitimate K-12 inbound use case | same |
| Protect against anomalous attachment types in emails | Gmail > Safety > Attachments | Quarantine | Quarantine | Quarantine | **Keep in inbox + warning** | All | Uncommon extensions held. **Admins set to warning** so IT can still receive vendor diagnostic files without a self-inflicted quarantine loop | same |
| Apply future recommended settings automatically | Gmail > Safety > Attachments | On | On | On | On | All | Google enables new attachment protections as shipped. Accepts a small change-management risk in exchange for not falling behind | same |

**Allowlisting file types.** The console permits allowlisting uncommon extensions
(entered without periods, comma-separated). Use this only for a **specific extension a
specific business system needs** — e.g. a `.dat` export from the SIS. Never allowlist
an extension to silence a category of alerts.

**Impact + comms:** Staff will occasionally find an expected attachment missing. The comms
line is "attachments can now be held for review — if you're expecting one and it doesn't
arrive, contact the help desk, don't ask the sender to resend it another way." That last
clause matters: the natural workaround is a personal Gmail address, which is worse.

**Rollback:** Immediate. Change action back to `Keep in inbox + warning`. Already-quarantined
messages remain in quarantine and must be released manually — rollback does not auto-release.

---

## 3. Safety — Spoofing & authentication

**This section contains the single highest-value control in this repo.**

**Path:** `Admin console > Apps > Google Workspace > Gmail > Safety > Spoofing and authentication`
**Edition:** All, including **[Fundamentals]**
**Available actions:** `Keep in inbox + warning` (default) · `Move to spam` · `Quarantine`
([source](https://knowledge.workspace.google.com/admin/gmail/advanced/advanced-phishing-and-malware-protection))

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Protect against spoofing of employee names** | Gmail > Safety > Spoofing and authentication | **Quarantine** | Quarantine | **Quarantine** | Quarantine | All | **The superintendent-impersonation killer.** Catches `Jane Superintendent <random@gmail.com>` — display name matches a directory user, sender doesn't. Expect a small volume of legitimate hits from staff mailing from personal accounts; that behavior should stop anyway | [ref](https://knowledge.workspace.google.com/admin/gmail/advanced/advanced-phishing-and-malware-protection) |
| Protect against inbound emails spoofing your domain | same | **Quarantine** | Quarantine | Quarantine | Quarantine | All | Inbound mail claiming to be `<PRIMARY_DOMAIN>` that isn't. **Blast radius warning:** this is the one that catches misconfigured SIS/copier/relay senders — see the flag below | same |
| **Protect Groups from inbound emails spoofing your domain** | same | Quarantine | Quarantine | Quarantine | Quarantine | All | Same protection applied to Groups, which the per-user setting does not cover. Set scope to **all groups**, not private-only. Frequently missed; a spoofed message to `all-staff@` is the worst-case delivery | same |
| Protect against domain spoofing based on similar domain names | same | Quarantine | Quarantine | Quarantine | Quarantine | All | Catches lookalike domains (`rn` for `m`, `.net` for `.org`, added hyphens). Pairs with [playbooks/07](../playbooks/07-lookalike-domain-response.md) | same |
| Protect against any unauthenticated emails | same | **Keep in inbox + warning** | Move to spam | Keep in inbox + warning | Keep in inbox + warning | All | **Deliberately not quarantined for staff.** Small vendors, PTA/booster lists, individual parents on niche providers, and youth-sports organizers routinely send unauthenticated mail. Quarantining this for staff generates enormous review volume and buries real detections | same |
| Apply future recommended settings automatically | same | On | On | On | On | All | Future spoofing protections auto-enable | same |

### ⚠ Blast radius: "inbound emails spoofing your domain"

**Flag this before it enters a rollout phase.** This setting quarantines anything claiming
to be from `<PRIMARY_DOMAIN>` that does not authenticate as such. That includes:

- Copier / MFP **scan-to-email** sending as the walk-up user's address
- SIS notifications sending as `noreply@<PRIMARY_DOMAIN>`
- SMTP relay users — alarm panels, HVAC, bell systems, scripts
- Any third-party product configured with a district From: address but no DKIM

**Sequence it correctly:** run §11's inventory and
[docs/09-dmarc-spf-dkim.md](09-dmarc-spf-dkim.md) §2 *first*, confirm each sender is
authenticating, then escalate this setting. If you escalate first you will find out which
systems were misconfigured by way of the help desk queue.

Legitimate senders are fixed by making them authenticate (SPF include + DKIM), **not by
allowlisting them** (§8).

### Why employee-name spoofing is the highest-value setting

T1 in [docs/00-threat-landscape.md](00-threat-landscape.md) has no other technical
control. The attacker's account is real, the domain is real, SPF/DKIM/DMARC all pass
legitimately. The *only* anomaly available to a filter is that the display name matches
a person in your directory while the address does not. This setting is the only thing in
Workspace that looks at that.

**Rollback:** Immediate, per-setting. Note that quarantined mail stays quarantined.

---

## 4. Safety — Links & external images

**Path:** `Admin console > Apps > Google Workspace > Gmail > Safety > Links and external images`
**Edition:** All, including **[Fundamentals]**
**These are toggles — there is no quarantine action available in this section**
([source](https://knowledge.workspace.google.com/admin/gmail/advanced/advanced-phishing-and-malware-protection)).

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Identify links behind shortened URLs | Gmail > Safety > Links and external images | On | On | On | On | All | bit.ly-style links resolved and scanned. No visible impact | [ref](https://knowledge.workspace.google.com/admin/gmail/advanced/advanced-phishing-and-malware-protection) |
| Scan linked images | same | On | On | On | On | All | Images fetched and scanned. **Partial QR-code mitigation (T5)** — a scanned image can be assessed, though a code photographed off a wall never touches Gmail | same |
| Show warning prompt for any click on links to untrusted domains | same | On | On | On | On | All | Interstitial warning on click. **Does not work in IMAP/POP clients** — which is an independent argument for §5 | same |
| Apply future recommended settings automatically | same | On | On | On | On | All | — | same |

> **The IMAP/POP interaction is the point.** This protection is unavailable to users on
> third-party mail clients. Every staff member left on Outlook-via-IMAP is a user for whom
> this control silently does not exist. §5 and this section reinforce each other.

**Impact + comms:** Users see an "are you sure?" page on some links. Low friction, high
recognition value. Comms line: "if you see this warning, it means the destination isn't
one we recognize — that's your cue to slow down, not to click through faster."

**Rollback:** Immediate toggle.

---

## 5. End-user access

**Path:** `Admin console > Apps > Google Workspace > Gmail > End User Access`
([source](https://knowledge.workspace.google.com/admin/gmail/advanced/working-with-gmail-admin-settings-in-google-workspace))

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| POP and IMAP access | Gmail > End User Access > POP and IMAP access | **Off** *(see note)* | **Off** | **Off** | Off | All | Removes the blind spot where link warnings don't apply. **Check for legitimate users first** — see below | [ref](https://support.google.com/a/answer/105694) |
| Automatic forwarding | Gmail > End User Access > Automatic forwarding | **Off** | **Off** | **Off** | Off | All | On by default. Off removes the forwarding option from Gmail settings entirely. **The #1 attacker persistence mechanism** — survives a password reset | [ref](https://support.google.com/a/answer/14724207) |
| Comprehensive mail storage | Gmail > End User Access > Comprehensive mail storage | **On** | On | On | On | All | Ensures all messages land in Gmail mailboxes, including SMTP-relay and non-Gmail-mailbox traffic. **Required for the investigation tool and Vault to see everything** — without it, IR has gaps | [ref](https://knowledge.workspace.google.com/admin/gmail/advanced/working-with-gmail-admin-settings-in-google-workspace) |
| Warn for external recipients | Gmail > End User Access > Warn for external recipients | On | On | On | On | All | Warns when composing to an external address. Reduces accidental student-data disclosure; costs nothing | [ref](https://support.google.com/a/answer/7380041) |

### Automatic forwarding — why this is not optional

When an account is compromised, the attacker's first move is persistence. A forwarding
rule to an external address survives the password reset, survives the "we've secured the
account" email, and keeps delivering the CFO's mail for months. Turning the feature off at
the OU level means it cannot be set.

If the district cannot turn forwarding off for all staff, the **minimum** is
Finance-HR and Students, and the fallback is Gmail's setting to restrict automatic
forwarding to a list of approved domains rather than allowing arbitrary external addresses.
Either way, [audit/gam/02-forwarding-and-filters.sh](../audit/gam/02-forwarding-and-filters.sh)
runs monthly regardless — the setting prevents *new* rules; it does not remove existing ones.

### ⚠ Blast radius: POP/IMAP

Before turning POP/IMAP off, run
[audit/gam/README.md](../audit/gam/README.md) → the IMAP usage check, and look for:

- Staff using Outlook or Apple Mail against Gmail (common with long-tenured staff)
- **Copier / MFP scan-to-email** configured with an SMTP account
- Legacy scripts and applications polling a mailbox via IMAP
- Alarm/HVAC/bell systems with a mailbox
- Third-party archiving or e-signature tools reading a shared mailbox

**Recommended sequencing:** Students off first (Phase 4 — near-zero legitimate use), then
Finance-HR, then general staff last with a 30-day notice and a migration path to the Gmail
web/mobile client. **Service accounts get their own OU with POP/IMAP left on**, scoped to
exactly the accounts that need it, rather than leaving it on district-wide.

**Impact + comms:** Real. This is the setting most likely to generate tickets. Template in
[comms/](../comms/).

**Rollback:** Immediate per-OU toggle. Client reconfiguration is not needed on rollback.

---

## 6. Security sandbox

**Path:** `Admin console > Apps > Google Workspace > Gmail > Spam, Phishing and Malware`
→ scroll to **Security sandbox** / **Security sandbox rules**
([source](https://knowledge.workspace.google.com/admin/gmail/advanced/gmail-security-sandbox-overview))

Attachments are detonated in an isolated VM to catch malware that signature-based scanning
misses — including zero-day and targeted payloads. This is the control that helps against
**T8 (compromised trusted partner)**, where the sender's reputation is genuinely good.

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Enable virtual execution of attachments in a sandbox | Gmail > Spam, Phishing and Malware > Security sandbox | On | On | On | On | **[Standard]/[Plus]** | Delivery delay of up to a few minutes on attachment-bearing mail | [ref](https://knowledge.workspace.google.com/admin/gmail/advanced/gmail-security-sandbox-overview) |
| Security sandbox rules | same section > Security sandbox rules > Configure | See below | — | See below | — | **[Standard]/[Plus]** | Scopes sandboxing to specific senders/recipients rather than everything | [ref](https://support.google.com/a/answer/7676854) |

**Deployment recommendation:** enable **blanket sandboxing** (leave "Enable virtual
execution of attachments in a sandbox" checked) rather than rule-scoping. Rule-scoping
exists to manage delivery latency; in a district the latency is acceptable and the
coverage gap is not. If latency complaints arrive from a specific workflow, *then* clear
the blanket checkbox and write rules — attachments are sandboxed only if they match a
rule once the blanket box is cleared, so **clearing it without writing rules disables
sandboxing entirely.** That is an easy and silent mistake.

If you do rule-scope, prioritize: Finance-HR (all inbound), the superintendent's office,
and anything inbound from outside `<PRIMARY_DOMAIN>` bearing Office documents.

> **`[VERIFY]` — edition eligibility.** Google's Education edition comparison lists
> "Malware detection in email attachments (Security Sandbox)" under **Education Standard**
> ([source](https://knowledge.workspace.google.com/admin/getting-started/editions/compare-education-editions)),
> but the Security Sandbox article's own supported-editions list enumerates Frontline Plus,
> Business Standard/Plus, and Enterprise Standard/Plus **without naming Education editions
> explicitly** ([source](https://knowledge.workspace.google.com/admin/gmail/advanced/gmail-security-sandbox-overview)).
> These two Google pages disagree. Confirm in your own console before promising it to
> leadership: if the section is present and configurable, you have it.
>
> **[Fundamentals] fallback:** none. Fundamentals gets standard attachment scanning plus
> the §2 anomalous-attachment controls. If students are on Fundamentals, §2 at
> `Quarantine` is doing the work.

**Impact + comms:** A few minutes of delay on attachments. Worth pre-announcing to
Finance-HR only; general staff will not notice.

**Rollback:** Immediate. Uncheck; note the trap above about rules.

---

## 7. Content compliance — banners and tripwires

**Path:** `Admin console > Apps > Google Workspace > Gmail > Compliance > Content compliance`
([source](https://knowledge.workspace.google.com/admin/gmail/advanced/set-up-rules-for-advanced-email-content-filtering))

Rules can reject, quarantine, or **modify** messages before delivery — including
prepending body text and adding custom headers
([source](https://support.google.com/a/answer/1346936)).

### Rule 7.1 — Cabinet display-name warning banner

**The highest-value custom rule.** Complements §3's employee-name protection with a
visible, human-readable warning for the near-miss cases.

| Field | Value |
| --- | --- |
| **Name** | `EXT — Cabinet display name impersonation warning` |
| **Affects** | Inbound |
| **Match** | Envelope sender is **external** AND `From:` header display name matches any cabinet/principal role name |
| **Expression** | Metadata match on `From` header, simple content match, one entry per name |
| **Action** | Prepend to message body: a high-contrast warning block |
| **OU** | All staff (Students not required — cabinet impersonation targets staff) |

Suggested banner text:

```
⚠ CAUTION — EXTERNAL SENDER USING A DISTRICT LEADER'S NAME
This message came from OUTSIDE <DISTRICT_NAME> but the sender's display name
matches a district leader. District leaders will NEVER ask you by email to buy
gift cards, send a wire, change banking details, or share your password.
Do not reply. Report it: <ABUSE_ALIAS>
```

**PII discipline:** the actual name list lives **only in the Admin console rule**. Do not
commit it to this repo (see [CLAUDE.md](../CLAUDE.md)). Track *roles* in
[config/district-profile.md](../config/district-profile.md).

**Maintenance:** this rule goes stale. It must be reviewed when leadership changes —
added to the quarterly cadence in [checklists/rollout-phases.md](../checklists/rollout-phases.md).

### Rule 7.2 — Financial-request tripwire

| Field | Value |
| --- | --- |
| **Name** | `EXT — Financial request tripwire` |
| **Affects** | Inbound |
| **Match** | Envelope sender external AND body/subject contains any of: `gift card`, `giftcard`, `wire transfer`, `direct deposit`, `routing number`, `ACH change`, `bank change`, `update my payment`, `change my payroll`, `are you at your desk`, `are you available` |
| **Action — Staff** | Prepend warning banner + add custom header `X-District-FinTripwire: staff` |
| **Action — Finance-HR** | **Quarantine** to a dedicated `Finance-Tripwire` quarantine |
| **OU** | Staff = banner; Finance-HR = quarantine |

The split matters. Banner-only for general staff keeps volume manageable and preserves
normal business. Quarantine for Finance-HR accepts review workload on the small population
where the loss would be six figures.

The custom header is not decoration — it makes these messages findable in the
investigation tool and email log search later, which is how you answer "has this campaign
hit us before?" during an incident.

**Tuning warning:** `direct deposit` and `are you available` will hit legitimate mail —
benefits open enrollment, scheduling. Expect to tune the Finance-HR quarantine over the
first two weeks. Start with banner-only everywhere for one week, count the hits, *then*
escalate Finance-HR to quarantine with real numbers in hand.

### Rule 7.3 — Generic external-sender banner

Optional and **deliberately not recommended as the first move.** A banner on every
external message trains staff to ignore banners, which then blunts 7.1 and 7.2. If the
district already has one, keep it; if not, ship 7.1 and 7.2 first and evaluate after a
term. The narrow banners are the ones people still read.

**Impact + comms:** Banners are visible on day one. Announce before enabling or the help
desk absorbs the confusion. Template in [comms/](../comms/).

**Rollback:** Disable the rule; effect is immediate for new mail. Already-modified messages
keep their banner — the body was rewritten at delivery and cannot be un-rewritten.

---

## 8. The allowlisting rule — read this one

**Never create a broad IP, sender, or domain allowlist that bypasses spam classification.**

This is the most common self-inflicted email security failure in K-12. It always starts
reasonably: a vendor's legitimate mail lands in spam, the vendor says "just allowlist our
IP range", and the district adds it. Six months later that vendor is compromised (T8) and
their mail arrives **pre-authorized to skip classification entirely** — the district
disabled its own filtering for exactly the sender most likely to be used against it.

**Do not use, for the purpose of fixing false positives:**

- `Gmail > Spam, Phishing and Malware > Email allowlist` (IP allowlist) — this bypasses
  spam classification, which is precisely the thing you want applied to a trusted partner
- Approved-senders lists scoped to whole domains
- Inbound gateway settings used to mark broad IP ranges as trusted

### What to do instead

| Problem | Correct fix |
| --- | --- |
| Vendor mail lands in spam | Get the vendor to fix SPF/DKIM. Most "we need allowlisting" requests are an unauthenticated sender. |
| Vendor genuinely can't authenticate | Narrow content compliance rule: specific envelope sender + specific expected subject/header → deliver. **Not** a classification bypass. |
| Internal system mail flagged | Authenticate it — [docs/09](09-dmarc-spf-dkim.md). This is the real fix and it's usually a 30-minute DNS change. |
| One-off legitimate quarantined message | Release it from quarantine. That is what quarantine is for. |

### Narrow exception process

When an exception is genuinely unavoidable:

1. **Written request** naming the business system, the exact sender address (not a
   domain, not a range), and why authentication cannot be fixed.
2. **Technology Director approval**, recorded.
3. **Narrowest possible scope** — single envelope sender address; add a subject or header
   match where the traffic is predictable.
4. **Expiry date, maximum 90 days.** No permanent exceptions.
5. **Logged** in an exceptions register with owner and review date.
6. **Quarterly review** — expired entries are removed, not renewed by default. Renewal
   requires a fresh request.

If an exception has been renewed twice, the answer is to replace the vendor or escalate
to the vendor's leadership, not to renew a third time.

---

## 9. Admin quarantine operations

**Path:** `Admin console > Apps > Google Workspace > Gmail > Manage quarantines`
([source](https://support.google.com/a/answer/6104172))

**A quarantine without an owner and an SLA is an outage.** Stand this up *before* setting
any action to `Quarantine`.

### Quarantines to create

| Quarantine | Fed by | Reviewer | SLA |
| --- | --- | --- | --- |
| `Spoofing-Auth` | §3 spoofing/auth settings | Primary + backup admin | 4 business hours |
| `Attachments` | §2 attachment settings | Primary + backup admin | 4 business hours |
| `Finance-Tripwire` | §7.2 Finance-HR rule | Primary admin **and** Finance Director | 2 business hours |
| `Default` | anything unrouted | Primary admin | 1 business day |

### Operating rules

- **Two named reviewers minimum**, one primary. Single-reviewer quarantines fail during
  illness, leave, and summer.
- **Coverage during breaks.** Summer, winter break, and spring break are exactly when BEC
  campaigns run, precisely because review lapses. Assign explicit coverage or lower the
  quarantine actions to `Move to spam` for the break period — a documented, deliberate
  downgrade is far better than an unmonitored quarantine.
- **Release ≠ allowlist.** Releasing a message delivers that message. It does not, and
  must not, create a standing rule (§8).
- **Record every release**: date, message, why. This becomes the evidence base for whether
  a setting is mis-tuned.
- **Weekly metric:** quarantined count, released count, release rate. A release rate above
  ~20% for a given quarantine means the setting is mis-tuned — fix the tuning, do not
  abandon the control.

**End-user quarantine access:** Google supports giving users visibility into their own
quarantined mail ([source](https://support.google.com/a/answer/14175289)).
**Not recommended for students.** For staff, consider it only after quarantine volumes are
understood — self-release by users defeats the purpose for the exact category
(convincing-looking impersonation) the quarantine exists to catch.

---

## 10. Hosted S/MIME

**Path:** `Admin console > Apps > Google Workspace > Gmail > User settings > S/MIME`
**Edition:** Available for **Education Fundamentals, Standard, and Plus**
([source](https://support.google.com/a/answer/6374496))

**Recommendation: leave it.** Hosted S/MIME provides message-level signing and encryption,
which is genuinely strong, but it requires certificate issuance and lifecycle management
for every participating user, and it only helps between parties who both have it deployed.

For a district, the realistic use case is a handful of Finance-HR or legal-adjacent staff
exchanging sensitive material with a specific counterparty who already runs S/MIME. If
that counterparty exists, deploy it for those users only. Otherwise the effort buys
essentially nothing against the threats in
[docs/00-threat-landscape.md](00-threat-landscape.md) — none of T1–T12 is prevented by
S/MIME.

**Better use of the same effort:** confidential mode for sensitive outbound, and
[docs/03-drive.md](03-drive.md) DLP for student data. Take-it-or-leave-it, genuinely.

---

## 11. Pre-flight inventory

Complete before Phase 1. This is the list that prevents §3's blast radius from landing on
the help desk.

- [ ] Every system sending as `<PRIMARY_DOMAIN>` identified —
      [config/district-profile.md](../config/district-profile.md)
- [ ] Copier / MFP scan-to-email method documented (SMTP relay? user auth? which account?)
- [ ] SMTP relay users enumerated
- [ ] POP/IMAP users enumerated — [audit/gam/](../audit/gam/)
- [ ] Existing external forwarding rules enumerated —
      [audit/gam/02-forwarding-and-filters.sh](../audit/gam/02-forwarding-and-filters.sh)
- [ ] Existing allowlists and approved-sender lists documented **and justified**, or removed (§8)
- [ ] Existing content compliance rules reviewed for conflicts
- [ ] Quarantine reviewers named, backups named, break coverage assigned (§9)
- [ ] Third-party gateway present? If yes, [ASSUMPTIONS.md](../ASSUMPTIONS.md) §A4 applies
      and inbound gateway config must be verified first

---

## Rollback summary

| Section | Rollback | Speed | Residue |
| --- | --- | --- | --- |
| §2 Attachments | Reset action to warning | Immediate | Quarantined mail stays quarantined |
| §3 Spoofing/auth | Reset action to warning | Immediate | Same |
| §4 Links/images | Toggle off | Immediate | None |
| §5 POP/IMAP | Toggle on per OU | Immediate | None — clients reconnect |
| §5 Forwarding | Toggle on per OU | Immediate | Existing rules unaffected either way |
| §6 Sandbox | Uncheck | Immediate | **Trap: clearing the blanket box without rules disables sandboxing** |
| §7 Compliance rules | Disable rule | Immediate for new mail | Delivered banners are permanent |
| §9 Quarantines | Lower actions first, then delete | Minutes | Release held mail *before* deleting a quarantine |
