# 08 — Monitoring & Response

Research date **2026-08-20**. Paths under `Admin console > Security` and
`Admin console > Reporting`.

**Every control in docs 01–07 will eventually be bypassed by something.** This document is
how you find out, and how fast you can undo it.

---

## 1. What "good" looks like

| Metric | Target |
| --- | --- |
| Time to know a phish was delivered | **< 1 hour** during school hours |
| Time to purge a phish from all inboxes | **< 30 minutes** from decision |
| Time to contain a compromised account | **< 15 minutes** from detection |
| % of phish first reported by users, not tooling | **> 50%** — a healthy sign, not a failure |
| Alert center backlog | **Zero unreviewed > 24h** |

That fourth metric is deliberately counter-intuitive. Users reporting first means the
reporting culture works. Tooling catching everything first usually means users have stopped
looking.

---

## 2. Alert center

**Path:** `Admin console > Security > Alert center`
([source](https://support.google.com/a/answer/9105276))

### Routing — do this first

**Route to `<SECURITY_ALIAS>`, a monitored Google Group, never an individual.** Personal
routing dies with leave, illness, and resignation, and it dies silently.

Configure notification recipients per alert type. For high-severity alerts also configure a
**webhook** to whatever the district actually watches — ticketing system, Chat space, or
SIEM. An alert nobody sees on a Saturday is not a control.

### High-value alerts to enable and route

| Alert | Why | Route | SLA |
| --- | --- | --- | --- |
| **Government-backed attack warning** | Google believes a state actor is targeting this user. Rare, extremely high signal | Immediate — page someone | 1 hour |
| **Leaked password** | Credential appeared in a breach corpus | Immediate | 4 hours |
| **Suspicious login** | Anomalous location/device | Immediate | 4 hours |
| **Phishing message detected post-delivery** | Google reclassified after delivery — **the single most actionable alert here** | Immediate | 1 hour |
| **User-reported phishing** | A human flagged it | Immediate | 4 hours |
| **Malware message detected post-delivery** | Same as above, malware | Immediate | 1 hour |
| **Suspicious device activity** | Device compromise indicator | Daily review | 1 business day |
| **Account suspension warning** | Google auto-suspended for suspicious activity | Immediate | 1 hour |
| **App outage / service disruption** | Operational, not security | Daily | — |
| **Drive settings changed / Gmail settings changed** | **Detects an attacker weakening your controls** — or an admin doing it undocumented | Immediate | 4 hours |

That last row matters more than it looks. An attacker with admin access turns off the
protections in doc 01 before doing anything else. Alerting on your own settings changing is
how you notice.

### Recommended actions

Some alerts support direct action from the alert center: **Mark as phishing**, **Delete
message**, **Quarantine message**
([source](https://knowledge.workspace.google.com/admin/security/recommended-actions-take-action-in-response-to-alerts)).

For a single message this is faster than the investigation tool. **For anything that hit
more than one user, go to the investigation tool (§5)** — the alert-center action addresses
the message that triggered the alert, not the campaign around it.

---

## 3. Activity rules **[Standard]/[Plus]**

**Path:** `Admin console > Security > Security center > Activity rules`
([source](https://support.google.com/a/answer/9275024))

An activity rule is a set of conditions and actions; if the conditions are met, the rule
triggers and the actions execute automatically. Rules can be built from **any investigation
tool search**, and can alert or act
([source](https://support.google.com/a/answer/9275024)).

### Recommended rules

| # | Rule | Trigger | Action | Notes |
| --- | --- | --- | --- | --- |
| 1 | **External forwarding created** | Gmail settings change: forwarding to external address | Alert + investigate | The #1 persistence mechanism. Highest-value rule here |
| 2 | **Mail delegate added** | Delegate added | Alert | Quiet, persistent mailbox access |
| 3 | **Send-as alias added** | Send-as added and verified | Alert | Enables sending as another identity |
| 4 | **Super admin role granted** | Admin role change | Alert immediately | Should be ~never. Any hit is worth a phone call |
| 5 | **Mass file sharing** | > N files shared externally in a short window | Alert | Exfiltration indicator |
| 6 | **Mass download** | > N files downloaded in a short window | Alert | Same |
| 7 | **Login from anomalous location for admin accounts** | Admin sign-in outside expected geography | Alert | Small population, so low noise |
| 8 | **Finance-HR tripwire header** | Message with `X-District-FinTripwire` ([docs/01](01-gmail.md) §7.2) | Alert | Ties the content rule into monitoring |

**Auto-remediation:** available, and **use it sparingly.** An auto-remediation rule that
misfires during state testing is its own incident. Recommended posture: **auto-remediate
nothing initially.** After 90 days of clean alerting, consider auto-action for the narrowest
and highest-confidence rules only — rule 1 (external forwarding) is the strongest candidate,
because a legitimate false positive costs one user one setting.

**[Fundamentals] fallback:** no activity rules. Substitute the monthly GAM audits in
[audit/gam/](../audit/gam/) — slower detection (days, not minutes) but the same findings.
Increase to weekly for forwarding and delegates if on Fundamentals.

---

## 4. Security dashboard and health page

**Security dashboard:** `Admin console > Security > Security center > Dashboard`
**[Standard]/[Plus]** ([source](https://support.google.com/a/answer/7492330))

**Security health page:** `Admin console > Security > Security center > Security health`
([source](https://support.google.com/a/answer/7491656))

The health page compares current settings against Google's recommendations and flags gaps.
**Use it as a change-detection tool, not a scorecard** — the valuable signal is a setting
that *used to* be green and now isn't. That means someone changed something.

| Review | Frequency | Owner | Output |
| --- | --- | --- | --- |
| Security health page — full pass | **Monthly** | Tech director | Deviations documented and justified or fixed |
| Security dashboard — spam/phishing trend | **Weekly** | Security admin | Volume anomalies |
| Dashboard — external sharing trend | Monthly | Security admin | Spikes investigated |
| Dashboard — OAuth grant activity | Monthly | Security admin | Feeds [docs/07](07-oauth-app-control.md) §7 |
| Dashboard — user report volume | Monthly | Security admin | Health of reporting culture |

**Capture a baseline snapshot in Phase 0** ([checklists/rollout-phases.md](../checklists/rollout-phases.md)).
Without a before, you cannot show an after — and the after is what funds next year's work.

**[Fundamentals] fallback:** health page availability is limited; use the GAM audits as the
monthly configuration-drift check.

---

## 5. Investigation tool — the workflow that matters

**Path:** `Admin console > Security > Security center > Investigation tool`
**[Standard]/[Plus]** ([source](https://support.google.com/a/answer/7575955))

### Bulk post-delivery purge

This is the capability that turns a district-wide phish from a two-day incident into a
twenty-minute one. Full procedure:
**[playbooks/03-post-delivery-phish-purge.md](../playbooks/03-post-delivery-phish-purge.md)**

Summary:

1. **Search** Gmail log events by message ID, subject, or sender to find every recipient
   ([source](https://knowledge.workspace.google.com/admin/security/investigate-reports-of-malicious-emails)).
2. **Verify scope** — confirm the result set is the campaign and nothing else. Over-broad
   deletion is its own incident.
3. **Actions > Delete messages**, enter a justification (e.g. "Suspected malicious emails"),
   confirm ([source](https://knowledge.workspace.google.com/admin/security/investigate-reports-of-malicious-emails)).
4. Other available actions: mark as spam, **mark as phishing**, send to inbox.
5. **Prefer "mark as phishing" over plain delete** where you want Google's classifier to
   learn from the sample and where you want the message preserved for investigation.
   Delete removes evidence.

**Justification text is not a formality** — it is the audit record of an administrator
reaching into user mailboxes. Write it as though it will be read by counsel, because it may be.

### Other investigation workflows

| Goal | Data source | Filter |
| --- | --- | --- |
| Who else got this phish? | Gmail log events | Subject / sender / message ID |
| What did a compromised account send? | Gmail log events | Sender = account, date range |
| What did they access? | Drive log events | Actor = account |
| What was shared externally? | Drive log events | Visibility = external / public |
| Where did they sign in from? | Login audit / User log events | Actor = account |
| Which accounts share this login IP? | Login audit | IP address — **finds the rest of the campaign** |
| What settings did they change? | Admin audit / User log events | Actor = account |

That IP pivot is the highest-value one. If one account is compromised, the same attacker
infrastructure usually touched others, and the login IP is how you find them before they're
used.

**[Fundamentals] fallback:** no investigation tool. **Email log search** (§6) locates
messages but **cannot bulk-delete**. Purge then means per-user action or GAM scripting —
materially slower. If the district is on Fundamentals for any population, know this gap
before an incident, not during one.

---

## 6. Email log search and long retention

### Email log search

**Path:** `Admin console > Reporting > Email log search`

Retains Gmail data for **30 days**
([source](https://knowledge.workspace.google.com/admin/gmail/advanced/about-gmail-reports-and-bigquery)).
Best for basic queries against predefined reports. Answers: was it delivered, where did it
go, was it quarantined, what did the receiving server say.

**The 30-day limit is the operative constraint.** BEC investigations routinely reach back
further — a payroll diversion discovered on payday may have started six weeks earlier. If
the district's only log source is email log search, that investigation cannot be completed.

### BigQuery log export **[Standard]/[Plus]**

**Path:** `Admin console > Reporting > BigQuery export`
([source](https://support.google.com/a/answer/9079365))

Supported editions include **Education Standard and Education Plus**
([source](https://knowledge.workspace.google.com/admin/gmail/advanced/about-gmail-reports-and-bigquery)).

| Consideration | Detail |
| --- | --- |
| **Why** | Admin console keeps Gmail data 30 days; BigQuery keeps it as long as you want |
| **Cost** | BigQuery storage + query. Modest at district scale, **but it is a real GCP bill** — get it approved, don't surprise finance |
| **Retention** | 13 months minimum recommended; 24 preferred (covers a full cycle plus comparison) |
| **Access** | Restrict the dataset. It contains metadata about every message in the district |
| **Value** | Historical BEC investigation, campaign correlation, "has this sender ever contacted us?" |

**Recommendation:** enable it. It is optional right up until the day it isn't, and it cannot
be enabled retroactively — the data you didn't export doesn't exist.

**[Fundamentals] fallback:** none. 30 days is the ceiling. Compensate with a documented
procedure to **export email log search results monthly** to district storage. Manual and
imperfect, and far better than nothing.

### Vault

**Path:** `vault.google.com` ([source](https://support.google.com/vault/answer/2990828))

Retention rules govern how long data is kept and purge it when no longer needed. Vault
retains data users deleted where it's subject to a hold or retention rule.

| Use | Setting |
| --- | --- |
| Mail retention | Per district records-retention policy — **coordinate with the records officer, not IT alone** |
| **Litigation/IR hold** | Place a hold on a compromised account **before** remediation |
| Coverage | Requires Vault licenses; verify coverage for all relevant users |

**The IR-relevant instruction:** place a Vault hold on a compromised account **before** you
start remediation. Remediation deletes evidence — that is what remediation is. A hold
preserves it. This is step 2 in
[playbooks/01](../playbooks/01-compromised-staff-account.md) for exactly that reason.

Comprehensive mail storage ([docs/01](01-gmail.md) §5) must be **On** for Vault and the
investigation tool to see SMTP-relay and non-Gmail-mailbox traffic. Without it there are
silent gaps in what you can investigate.

---

## 7. Build the reporting culture

**The highest-value detection capability in the district is 1,200 people who report things.**
No configuration in this repo beats it, and it is the cheapest thing here.

### Mechanics

- **Gmail's "Report phishing"** is built in. Use it — it feeds Google's classifier and the
  user-reported-phishing alert. Teach it as the default action.
- **`<ABUSE_ALIAS>`** for forwarding anything that doesn't fit, including QR flyers and text
  messages. Accept photos; a picture of a suspicious flyer is a legitimate report.
- **Acknowledge every report.** An auto-reply within seconds and a human note within a day
  for anything real. Silence trains people to stop.
- **Close the loop publicly.** "Fourteen of you reported the fake HR message this morning —
  we removed it from 340 inboxes in eleven minutes." That single sentence generates more
  future reports than any training module.

### Culture rules

| Rule | Why |
| --- | --- |
| **Never punish a click.** Ever. | Punishment produces silence, and silence is how a 20-minute incident becomes a 3-day one |
| **Thank every report, including wrong ones.** | False positives are the cost of a working sensor network. A user who reports 10 legitimate newsletters is a user who will report the real one |
| **Report first, delete second.** | Deleted mail is harder to investigate |
| **Make it one click.** | Any friction and reporting stops |
| **Report on personal devices too.** | QR codes, SMS, and voice all arrive off-platform |

### Students specifically

For **T10 (sextortion, scholarship scams)** the reporting path must be **usable by a
frightened 15-year-old**:

- **Non-punitive, explicitly.** A student who sent an image needs to believe they will not
  be disciplined for reporting. If they don't believe it, they pay the extortion instead.
- **No parent-notification precondition to reporting.** Parents get involved through the
  proper channel; requiring it *before* a report is a barrier at the worst possible moment.
- Counselors and the SRO in the loop by design, with a documented escalation path.
- Publicize the national routes: `ncii.ic3.gov` for non-consensual imagery, `tips.fbi.gov`,
  1-800-CALL-FBI ([FBI](https://www.fbi.gov/news/press-releases/fbi-and-partners-warn-student-athletes-of-sexual-exploitation-schemes)).
- Teach the one fact that changes outcomes: **complying with demands does not stop
  distribution — it reliably produces more demands**
  ([IC3 PSA 260810](https://www.ic3.gov/PSA/2026/PSA260810)).

> This procedure belongs to student services with IT support, not to IT with student
> services consulted. Get that ownership right on paper before you need it.

---

## 8. Monitoring cadence

| Task | Frequency | Owner |
| --- | --- | --- |
| Alert center triage | **Daily, school days** | Security admin |
| Quarantine review ([docs/01](01-gmail.md) §9) | **Daily**, per SLA | Named reviewers |
| Apps pending review ([docs/07](07-oauth-app-control.md)) | Weekly | Tech dept |
| Security dashboard — spam/phishing trend | Weekly | Security admin |
| **Security health page — full pass** | **Monthly** | Tech director |
| GAM audit suite | Monthly | Security admin |
| External sharing / OAuth trend review | Monthly | Security admin |
| **OAuth token + DWD audit** | **Quarterly** | Tech director |
| Group settings audit ([docs/04](04-groups.md)) | Quarterly | Security admin |
| Admin role review | Quarterly | Tech director |
| Cabinet name-rule refresh ([docs/01](01-gmail.md) §7.1) | Quarterly | Security admin |
| Phishing simulation | Quarterly | Tech dept + HR |
| **Tabletop exercise** | **2× per year** | Cabinet + IT |
| Full package review against current Google docs | Annually | Tech director |

**Break coverage is a named assignment.** Summer, winter, and spring break are when BEC
campaigns run, precisely because review lapses. Assign it or explicitly lower quarantine
actions for the period — both are defensible; an unmonitored quarantine is not.
