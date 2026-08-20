# 07 — OAuth & Third-Party App Control

Research date **2026-08-20**. Paths under
`Admin console > Security > Access and data control > API controls` and
`Admin console > Apps > Google Workspace Marketplace apps`.

---

## 1. Why this document exists

Phishing gets an attacker one account. **An OAuth grant gets them persistent, password-
independent, MFA-independent access to data** — and it survives every remediation step in
[playbooks/01](../playbooks/01-compromised-staff-account.md) *except* explicit token
revocation.

The consent-phishing pattern: the victim is shown a real Google consent screen for an app
named something plausible ("Classroom Sync Helper", "District Docs Backup"), clicks Allow,
and the attacker holds a refresh token with whatever scopes were requested. **The password
reset doesn't matter. The 2SV doesn't matter. The token still works.**

Two district-specific amplifiers:

- **Teachers install things.** The ed-tech ecosystem runs on "click here to connect your
  Google account", and teachers are trained by every legitimate vendor to do exactly what a
  consent phish asks.
- **Domain-wide delegation is the largest blast radius in the tenant** — a single
  compromised delegated service account can impersonate *every user in the domain*
  simultaneously. There is nothing else in Workspace with that reach.

---

## 2. App access control — the core setting

**Path:** `Admin console > Security > Access and data control > API controls > App access control`
([source](https://knowledge.workspace.google.com/admin/apps/control-which-third-party-and-internal-apps-access-google-workspace-data))

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Unconfigured third-party apps — access to **restricted scopes** | Security > Access and data control > API controls > App access control | **Blocked** | **Blocked** | Blocked | Blocked | All | Apps must be explicitly trusted before touching Gmail/Drive/Calendar data. **This is the control** | [ref](https://knowledge.workspace.google.com/admin/apps/control-which-third-party-and-internal-apps-access-google-workspace-data) |
| Unconfigured third-party apps — **all other scopes** | same | **Blocked** | **Blocked** | Blocked | Blocked | All | Sign-in-only scopes included. Blocking here is stricter but avoids a long tail of unreviewed grants | same |
| Internal apps (same-domain) | same | Trusted | Trusted | Trusted | Trusted | All | District-built Apps Script and internal tooling keeps working | same |
| Google services access | same | Reviewed per service | Restricted | Reviewed | Reviewed | All | Overlaps [docs/05](05-other-services.md) §7 | same |

### What "restricted scopes" means and why it's the line

Google classifies the highest-sensitivity scopes — Gmail read/send, full Drive access,
Calendar, contacts — as **restricted**. These are exactly the scopes a consent phish wants,
and exactly the scopes a legitimate ed-tech tool sometimes genuinely needs.

Blocking unconfigured apps from restricted scopes means: **a user clicking Allow on an
unknown app gets nothing.** The consent screen may appear; the grant fails. That single
setting neutralizes the consent-phishing class.

### ⚠ Blast radius — this one is big, plan for it

Turning this on **will break currently-working integrations**. Before enabling:

1. **Inventory every app with an existing grant:**
   [audit/gam/04-oauth-tokens.sh](../audit/gam/04-oauth-tokens.sh), or
   `API controls > App access control > Manage Google Services / third-party apps`.
2. Sort by **number of users** and by **scopes requested**. An app with 400 teachers and
   Drive scope is a Tier 1 review; an app with 1 user and profile scope is not.
3. For each, decide: **Trusted** (district-approved, contract in place, DPA signed),
   **Limited**, or **Blocked**.
4. **Trust the approved list before flipping the default to Blocked.** In that order. Doing
   it the other way round takes down instruction on a school day.
5. Announce with the request workflow (§5) already live.

**Expect to find:** grade-book integrations, Chrome extensions with Drive access, e-signature
tools, PDF converters, "free" classroom utilities that teachers found themselves, and at
least one app nobody can identify. That last category is the point of the exercise.

**Impact + comms:** High if sequenced wrong, low if sequenced right. Two-week notice with
the app request form live. Template in [comms/](../comms/).

**Rollback:** Set unconfigured apps back to allowed — immediate. **Grants made while
blocked are not retroactively created**, so nothing is restored automatically; users
re-consent.

---

## 3. Marketplace allowlist mode

**Path:** `Admin console > Apps > Google Workspace Marketplace apps > Settings` and
`> Apps list` (requires **Google Workspace Marketplace** admin privilege)
([source](https://support.google.com/a/answer/6089179))

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Manage access to apps | Marketplace apps > Settings | **Allow users to install and run allowlisted apps** | **Don't allow users to install any apps** | Allowlisted only | Allowlisted only | All | Staff install from a curated list; students install nothing | [ref](https://support.google.com/a/answer/6089179) |
| Allowlist contents | Marketplace apps > Apps list | Reviewed, contracted, DPA'd apps only | — | — | — | All | The allowlist *is* the district's approved ed-tech list | same |

**Important interaction:** the allowlist only affects users set to
*"Allow users to install and run allowlisted apps."* It has **no effect** on users allowed
to install anything, or on users blocked from installing entirely
([source](https://support.google.com/a/answer/6089179)). Setting an allowlist while users
are on "install anything" accomplishes nothing — a genuinely easy misconfiguration.

**And:** API controls override the allowlist. An app allowlisted here but blocked in §2 **is
blocked** ([source](https://support.google.com/a/answer/6089179)). Configure both; §2 wins.

---

## 4. Under-18 users and the confirmed-apps requirement

**Path:** `Admin console > Security > Access and data control > API controls > App access control`
→ **Apps pending review**
([source](https://support.google.com/a/answer/13288950),
[source](https://support.google.com/a/answer/13437370))

Google applies additional protections to users designated **under 18**: they are **blocked
from unconfigured third-party apps**, and see a message offering to **request access**
([source](https://support.google.com/a/answer/13288950)). Requests appear in the **Apps
pending review** list on the App access control page, where an admin allows or dismisses
each one
([source](https://knowledge.workspace.google.com/admin/apps/review-and-manage-third-party-app-access-requests)).

**This is Education-editions only** and depends entirely on correct age designation —
see [docs/05-other-services.md](05-other-services.md) §1. **If students are mis-designated
as 18+, none of this applies to them.** Verify first.

### Parental consent

> Your organization is responsible for obtaining parental consent, if required by
> applicable law, before allowing under-18 users to access third-party apps
> ([source](https://support.google.com/a/answer/13288950)).

**This is a district legal obligation, not an IT preference.** Loop in whoever owns COPPA
and FERPA compliance. The approval workflow in §5 should have a consent checkpoint, and the
answer to "do we have consent for this app" needs an owner who is not the technology
department.

---

## 5. Teacher app-request workflow

Google supports educators requesting access to third-party apps **on behalf of their
students** ([Workspace Updates, 2024-11](https://workspaceupdates.googleblog.com/2024/11/request-access-to-third-party-apps-on-behalf-of-students.html)).

**Build the process before you turn on the restrictions.** Without it, blocking apps looks
like IT saying no, and teachers route around it with personal accounts — which is worse than
where you started.

### Recommended workflow

| Step | Owner | SLA |
| --- | --- | --- |
| 1. Teacher submits request (app name, URL, instructional purpose, grade levels, data collected) | Teacher | — |
| 2. Triage — already reviewed? already blocked? | Tech dept | 1 business day |
| 3. Privacy review — DPA in place? student PII collected? COPPA/FERPA posture? | Data privacy owner | 5 business days |
| 4. Security review — scopes requested vs. scopes needed | Tech dept | 3 business days |
| 5. Instructional review — does it duplicate something already approved? | Curriculum | 5 business days |
| 6. Decision → allowlist + API controls trusted, or denied with reason | Tech dept | 1 business day |
| 7. Published to the approved-apps list | Tech dept | — |

**Target: 10 business days end to end.** Publish that number. A predictable two weeks is
something a teacher can plan a unit around; an unpredictable process is one they bypass.

**Scope review is where the security value is.** A flashcard app requesting full Drive
access is asking for far more than it needs. "What does it need vs. what does it ask for"
is the single highest-signal question in the whole workflow, and it's usually answerable in
five minutes.

**Fast path:** pre-approve a standing list of major platforms the district already has
contracts with, so the queue holds genuinely new requests rather than re-litigating Canvas.

---

## 6. Domain-wide delegation — highest blast radius in the domain

**Path:** `Admin console > Security > Access and data control > API controls > Manage Domain Wide Delegation`
**Requires super admin**
([source](https://knowledge.workspace.google.com/admin/apps/control-api-access-with-domain-wide-delegation))

DWD lets a service account **impersonate any user in the domain** for the granted scopes.
No user consent. No user awareness. No 2SV. If a DWD client with Gmail scope is compromised,
the attacker reads every mailbox in the district.

### Audit — do this now, not in Phase 2

For each entry:

| Check | Question |
| --- | --- |
| **Identify** | What is this Client ID? If nobody can say, that alone is the finding |
| **Owner** | Named person and named system. "Probably the SIS" is not an owner |
| **Scopes** | Read-only where read-only suffices? `gmail.readonly` not `mail.google.com`? |
| **Necessity** | Is the integration still in use? Vendors change; grants don't |
| **Provenance** | Who created it, when, under what project? |
| **Key hygiene** | Where does the service account key live? Rotated when? Who has a copy? |

**Common findings, in order of frequency:**

- Grants from **vendors no longer under contract** — the integration ended, the grant didn't
- **Over-scoped** grants: full `mail.google.com` where `gmail.readonly` would do
- **Unidentifiable** Client IDs from a migration years ago
- **Service account keys** sitting in a shared drive, a git repo, or a former admin's Downloads
- Grants created by a **departed administrator** with no documentation

**Remove anything you cannot positively identify and justify.** The recovery path — a broken
integration and a support ticket — is bounded and obvious. The alternative is an unmonitored
key with domain-wide mailbox access held by someone unknown.

**Best practice per Google:** grant the **narrowest possible scopes**
([source](https://knowledge.workspace.google.com/admin/apps/domain-wide-delegation-best-practices)).

**⚠ Before removing:** notify the integration owner, and schedule for a **low-impact window**
— not during grade reporting, state testing, or the first week of school. A removed DWD
grant breaks the integration immediately and completely.

**Script:** [audit/gam/04-oauth-tokens.sh](../audit/gam/04-oauth-tokens.sh) covers user
tokens. **DWD must be reviewed in the console** — GAM's visibility here is limited and the
console is authoritative.

---

## 7. Quarterly token review

| Task | Frequency | Where |
| --- | --- | --- |
| Review granted OAuth tokens by app, sorted by user count | **Quarterly** | API controls > App access control |
| Review new apps appearing since last review | Quarterly | same |
| Review Marketplace allowlist for departed/unrenewed vendors | Quarterly | Marketplace apps > Apps list |
| **Domain-wide delegation full audit** | **Quarterly** | API controls > Manage Domain Wide Delegation |
| Apps pending review queue | **Weekly** | App access control > Apps pending review |
| Revoke tokens for departed staff | At offboarding | [audit/gam/remediation/](../audit/gam/remediation/) |

**Offboarding is the leak.** Suspending an account does not revoke its OAuth grants in every
case. Explicit token revocation belongs in the offboarding checklist —
[audit/gam/remediation/revoke-tokens.sh](../audit/gam/remediation/revoke-tokens.sh).

**Weekly, not quarterly, for pending review.** A teacher waiting three months for an app
decision has already worked around you.

---

## 8. Incident interaction

When an account is compromised, **token revocation is mandatory and it is not optional
cleanup** — it is the step that determines whether the attacker still has access tomorrow.
Password reset, sign-out-everywhere, and 2SV re-enrollment **do not invalidate an OAuth
refresh token.**

Order matters — see [playbooks/01-compromised-staff-account.md](../playbooks/01-compromised-staff-account.md):

1. Suspend / reset password
2. Sign out all sessions
3. **Revoke all OAuth tokens** ← this one
4. Remove app-specific passwords
5. Check filters, forwarding, delegates, send-as

Steps 3–5 are the persistence mechanisms. Skipping them means doing the whole incident
again in a week, which is a thing that genuinely happens.

---

## Rollback summary

| Section | Rollback | Speed | Residue |
| --- | --- | --- | --- |
| §2 App access control | Set unconfigured apps to allowed | Immediate | Users must re-consent; grants aren't restored |
| §3 Marketplace | Widen install permission | Immediate | Uninstalled apps must be reinstalled |
| §4 Under-18 | Tied to age designation | Immediate | — |
| §6 DWD removal | **Re-create the grant** | Minutes — **if you recorded the Client ID and scopes first** | **Record before removing. There is no undo button.** |
