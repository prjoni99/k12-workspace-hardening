# 06 — Accounts, MFA & Admin Hardening

Research date **2026-08-20**. Paths under `Admin console > Security` and
`Admin console > Directory`.

---

## 1. The premise this document is built on

**"We have MFA" is no longer a sufficient statement.**

AiTM phishing kits proxy the entire sign-in — the victim sees a real Google login page,
enters a real password, completes a real 2SV challenge, and the kit captures the resulting
**session cookie**. The attacker replays the cookie and never needs the password or the
second factor again.

**SMS, TOTP, and push are all proxyable. FIDO2 security keys and passkeys are not**
([Proofpoint](https://www.proofpoint.com/us/blog/email-and-cloud-threats/tycoon-2fa-phishing-kit-mfa-bypass),
[Group-IB](https://www.group-ib.com/masked-actors/tycoon2fa/)). Passkeys and security keys
carry **the same level of phishing protection**, because passkeys use the same public-key
cryptography that underpins physical keys
([Google](https://knowledge.workspace.google.com/admin/security/protect-your-business-with-2-step-verification)).

The practical consequence, and the thing to say to leadership:

> Turning on 2SV for all staff is necessary and it is not the finish line. For the ~30
> accounts that can move money or change everything — super admins, Finance-HR, payroll —
> **only phishing-resistant methods actually stop the current attack.**

Maps to **T4** and **T12** in [docs/00-threat-landscape.md](00-threat-landscape.md).

---

## 2. 2SV enforcement for all staff

**Path:** `Admin console > Security > Authentication > 2-step verification`
([source](https://knowledge.workspace.google.com/admin/security/deploy-2-step-verification))

> Google is already enforcing 2SV for **administrator accounts**, and that enforcement
> covers organizations with Workspace for Education
> ([source](https://knowledge.workspace.google.com/admin/security/about-2sv-enforcement-for-admins)).
> Admin 2SV is not a choice you're making; it's a deadline you're meeting.

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Allow users to turn on 2SV | Security > Authentication > 2-step verification | On | On | On | On | All | Prerequisite for everything below | [ref](https://knowledge.workspace.google.com/admin/security/deploy-2-step-verification) |
| Enforcement | same | **On**, after enrollment window | Off *(see §10)* | **On** | **On** | All | Users without 2SV cannot sign in after the deadline | same |
| Enrollment period for new users | same | 1 week | — | **1 day** | 1 day | All | New hires must enroll quickly; a long grace window on a finance account is a gap | same |
| Allowed methods — general staff | same | Any except SMS/voice if achievable | — | — | — | All | SMS is the weakest method and SIM-swap-attackable | same |
| Allowed methods — Finance-HR & Admins | same | — | — | **Only security key / passkey** | **Only security key / passkey** | All | §3 | same |
| Frequency: allow "don't ask again on this device" | same | On | — | **Off** | **Off** | All | Trusted-device suppression is a stolen-cookie multiplier for high-value accounts | same |

### Rollout sequence that actually lands

1. **Weeks 1–2:** enable 2SV, communicate, **do not enforce**. Publish a how-to and hold
   drop-in sessions.
2. **Weeks 3–4:** targeted outreach to non-enrolled users. Expect ~60% voluntary enrollment.
3. **Week 5:** enforce for **IT staff first** — dogfood the support burden before it hits
   the district.
4. **Week 6:** enforce for Finance-HR (phishing-resistant only, §3).
5. **Weeks 7–8:** enforce for all staff, in school-sized waves rather than district-wide.

**Do not enforce district-wide on a single day.** The help desk cannot absorb 1,200 users
discovering simultaneously that their backup codes are in a drawer at home. Wave by school.

### ⚠ Blast radius

- **Shared/kiosk accounts** — library, lab, and cart logins in `/Shared Devices` cannot
  reasonably do per-user 2SV. Deal with this by removing shared accounts, not by exempting
  a broad OU. If they must persist, isolate them in their own OU with the tightest possible
  service set and no mail access.
- **Service accounts** — must not be caught by user enforcement. Confirm `/Service Accounts`
  is excluded.
- **Substitute teachers and seasonal staff** — high-churn, low-tech-contact populations
  that surface at the worst moment. Plan for them explicitly.
- **If SSO fronts Google** ([ASSUMPTIONS.md](../ASSUMPTIONS.md) §A10), Google's 2SV policy
  **does not apply** to SSO-authenticated sessions. The phishing-resistant requirement must
  then be enforced at the identity provider instead. Verify which applies before promising
  this control to anyone.

**Impact + comms:** The largest user-facing change in this package. Templates in
[comms/](../comms/).

**Rollback:** Disable enforcement — immediate. Enrolled users stay enrolled, which is fine.

---

## 3. Phishing-resistant methods for high-risk roles

**Required for:** super admins, all delegated admins, Finance-HR, anyone who can change
payroll banking, anyone with SIS write access to financial records.

**Path:** `Admin console > Security > Authentication > 2-step verification` → allowed
methods → **Only security key** (passkeys included)

| Role | Method | Backup | Rationale |
| --- | --- | --- | --- |
| Super admins | 2× hardware security keys | Second physical key, stored separately | Cannot be proxied. Two keys because losing the only one locks out the domain |
| Delegated admins | Hardware key or passkey | Second factor enrolled | Same attack surface, smaller scope |
| Finance-HR | Passkey (platform) or hardware key | Second passkey on a second device | T2/T3 loss magnitude justifies the friction |
| Payroll-touching | Passkey or hardware key | Second passkey | same |
| General staff | Any non-SMS method | Backup codes | Cost/benefit; escalate over time |

**Budget note for the cabinet.** Hardware keys are roughly $25–50 each. Two keys for ~30
high-risk accounts is **$1,500–3,000, one time**. Put that number next to the district's
last BEC loss, or the sector's typical one. It is the cheapest line item in any security
proposal you will make this year, and it is the one that stops the attack that's actually
running.

**Passkeys vs. hardware keys.** Same phishing resistance
([source](https://knowledge.workspace.google.com/admin/security/protect-your-business-with-2-step-verification)).
Passkeys are cheaper and more convenient (device biometric); hardware keys are portable
across devices and survive device loss/replacement cleanly. **Recommendation:** hardware
keys for super admins (portability and break-glass matter most there), passkeys for
Finance-HR (lower friction, better adoption, adoption is the real constraint).

Google also supports allowing users to **skip passwords at sign-in** where passkeys are
deployed ([source](https://knowledge.workspace.google.com/admin/users/allow-users-to-skip-passwords-at-sign-in)) —
worth evaluating once passkeys are established, since a password that is never typed is a
password that cannot be phished.

**Impact + comms:** Real friction for ~30 people. Brief them individually, in person. This
is a small enough population that a group email is the wrong tool.

**Rollback:** Widen allowed methods — immediate. **Don't**, without an explicit decision
recorded; this is the control that matters most.

---

## 4. Advanced Protection Program for super admins

**Path:** `Admin console > Security > Authentication > Advanced Protection Program`
([source](https://knowledge.workspace.google.com/admin/security/protect-users-with-the-advanced-protection-program))

APP is Google's strongest account protection tier. It:

- **Enforces security keys or passkeys** for sign-in
- Enables **enhanced pre-delivery scanning** of incoming email for phishing
- Applies stricter app-access and download protections
- **Takes precedence over 2SV policy settings** where both are configured
  ([source](https://knowledge.workspace.google.com/admin/security/protect-users-with-the-advanced-protection-program))

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Advanced Protection Program enrollment | Security > Authentication > Advanced Protection Program | Optional | Off | **Recommended** | **Required** | All | Strictest tier; some third-party apps will be blocked from these accounts | [ref](https://knowledge.workspace.google.com/admin/security/protect-users-with-the-advanced-protection-program) |

**Enhanced pre-delivery scanning** is available across editions and is enabled for APP
users ([source](https://knowledge.workspace.google.com/admin/security/advanced-protection-program-faq)) —
an extra deep scan before delivery for the accounts most likely to be targeted.

**⚠ Before enrolling:** APP restricts third-party app access. If a super admin's daily
workflow depends on a third-party tool, it may break. This is a strong argument for §5 —
super admin accounts should not have daily workflows at all.

**Rollback:** Un-enroll — immediate.

---

## 5. Super admin hygiene

**The highest-blast-radius accounts in the district.** A compromised super admin is not an
incident, it is the whole domain.

### Rules

| # | Rule | Why |
| --- | --- | --- |
| 1 | **2–4 dedicated super admin accounts.** Not more, not one. | Two is the minimum for break-glass. More than four and nobody knows who has what |
| 2 | **Never a daily driver.** Named accounts (`admin-firstname@`) used only for admin work | A super admin account that reads email is a super admin account that can be phished |
| 3 | **Every admin has a separate normal account** for mail, Drive, meetings | The actual mechanism for rule 2 |
| 4 | **Hardware security key required**, two per account | §3 |
| 5 | **APP enrolled** | §4 |
| 6 | **No third-party app grants**, ever | Highest-value token in the domain |
| 7 | **Recovery locked down** — recovery phone/email are district-controlled, never personal | Account recovery is an attack path. A personal recovery address outlives employment |
| 8 | **One break-glass account**, credentials in a physical safe, key in the safe, monitored for use, never used routinely | For when everything else fails or the admin is unavailable |
| 9 | **Quarterly review** of who holds super admin | Roles change; grants don't expire on their own |
| 10 | **Alert on every super admin sign-in** | ~30 sign-ins/month is a reviewable volume. An unexpected one is a real signal ([docs/08](08-monitoring-response.md)) |

### Delegated admin roles — use them

Most people with super admin do not need it. Google's predefined and custom roles cover the
realistic cases ([source](https://knowledge.workspace.google.com/admin/users/administrator-privilege-definitions)):

| Function | Role instead of super admin |
| --- | --- |
| Password resets, user creation | User Management Admin |
| Gmail settings | Custom role: Gmail settings only |
| Chromebook/device management | Services Admin (device scope) |
| Help desk tier 1 | Custom: reset password, view users, **no** OU or security changes |
| Reporting/audit access | Custom: reports + audit read-only |

**Audit:** [audit/gam/07-admin-roles.sh](../audit/gam/07-admin-roles.sh). Run it now. The
common finding is 8–15 super admins in a district that needs 3, usually accumulated from
past migrations and vendor engagements. **Vendor super admin accounts from a completed
project are the single most common orphan** — check for those specifically.

### Super admin password recovery

Google provides a specific mechanism for super admin self-recovery
([source](https://support.google.com/a/answer/9436964)). **Recommendation: leave it off**
and rely on the break-glass account plus a second super admin. Self-recovery for the
highest-privilege account in the domain is an attack surface that the break-glass procedure
already covers more safely.

---

## 6. Login challenges

**Path:** `Admin console > Security > Authentication > Login challenges`
([source](https://knowledge.workspace.google.com/admin/security/protect-google-workspace-accounts-with-security-challenges))

Google presents additional challenges — employee ID, recovery address — when a sign-in
looks risky.

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Employee ID challenge | Security > Authentication > Login challenges | **On** | On | On | On | All | Requires employee ID on suspicious sign-in. **Requires the employee ID field to be populated** in the directory — usually via SIS/HR sync | [ref](https://knowledge.workspace.google.com/admin/security/protect-google-workspace-accounts-with-security-challenges) |

**Populate the employee ID field first**, or the challenge cannot be presented and the
control is decorative. This is a directory-sync task, not a security-console task.

**Operational note for the help desk:** if a login challenge is blocking a user, **changing
their password does not fix it** — the challenge must be disabled for that user first
([source](https://knowledge.workspace.google.com/admin/support/troubleshooting/troubleshoot-login-challenges-2-step-verification-and-sign-in-issues)).
Put that sentence in the help desk runbook; it saves a recurring twenty-minute confusion.

---

## 7. Session length

**Path:** `Admin console > Security > Access and data control > Google Session control` →
**Web session duration**
([source](https://knowledge.workspace.google.com/admin/security/set-session-length-for-google-services))

**Why this is an anti-AiTM control.** A stolen session cookie is valuable exactly as long
as the session lives. Shortening the session shortens the attacker's window.

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Web session duration | Security > Access and data control > Google Session control | 14 days | 14 days | **8 hours** | **8 hours** | **[Plus]** for session control | High-risk roles re-authenticate daily; passkeys make that ~2 seconds | [ref](https://knowledge.workspace.google.com/admin/security/set-session-length-for-google-services) |

**The Admin console is already 1 hour and cannot be changed**
([source](https://knowledge.workspace.google.com/admin/security/set-session-length-for-google-services)).
Google made that decision for you; it's the right one.

**Why 8 hours and not 1 for Finance-HR.** One hour would mean re-authenticating repeatedly
through a workday, and the predictable result is staff finding workarounds. Eight hours
means one sign-in per day, and with a passkey that is a fingerprint touch. Friction people
accept is worth more than friction they route around.

**Edition note:** session-length control is a **[Plus]** capability
([source](https://knowledge.workspace.google.com/admin/getting-started/editions/compare-education-editions)).
**[Fundamentals] fallback:** none directly — rely on phishing-resistant 2SV (§3) plus
prompt token revocation during incident response ([playbooks/01](../playbooks/01-compromised-staff-account.md)).

**Rollback:** Immediate. Users are not signed out when the duration is lengthened.

---

## 8. Context-Aware Access **[Plus]**

**Path:** `Admin console > Security > Access and data control > Context-Aware Access`
([source](https://knowledge.workspace.google.com/admin/security/protect-your-business-with-context-aware-access))

CAA gates access on device and network context — not just "who are you" but "from where, on
what." **Supported in Education Plus.**

| Access level | Applies to | Condition | Rationale |
| --- | --- | --- | --- |
| `admin-console-restricted` | Super + delegated admins | District network **or** managed device, from US | The Admin console should never be reachable from an arbitrary device ([source](https://support.google.com/a/answer/11068433)) |
| `finance-restricted` | `/Staff/Finance-HR` | Managed device required | Payroll/AP from a personal laptop is the T2/T3 path |
| `student-basic` | `/Students/*` | Optional geographic restriction | Consider carefully — see below |

**Deploy in monitor mode first.** CAA can lock people out — including you — and the way that
usually happens is a legitimate condition nobody modeled. Run in monitor, review who *would*
have been blocked, then enforce.

### ⚠ Blast radius

- **Locking yourself out.** Always keep one super admin **exempt** from CAA, credentials in
  the safe, until the policy is proven. This is not optional.
- **Legitimate remote work** — snow days, after-hours, summer administration, staff
  travelling for PD. A network-only rule breaks all of it. Prefer *managed device* over
  *district network* as the primary condition.
- **Student geographic restrictions** — will break students travelling, military families,
  and any legitimate out-of-area access. Usually **not worth it**; the false-positive cost
  lands on families with the least ability to resolve it.
- **1:1 device programs** — if student devices aren't enrolled as managed, a managed-device
  condition blocks everyone.

**[Fundamentals]/[Standard] fallback:** CAA appears at **Standard** in the Education
comparison ([source](https://knowledge.workspace.google.com/admin/getting-started/editions/compare-education-editions)).
For Fundamentals there is no equivalent — rely on §3 and §7.

**Rollback:** Set the access level to monitor, or unassign it. Immediate. **Verify you can
still reach the Admin console before you close the browser tab** — this is the single most
common way an admin locks themselves out of their own tenant.

---

## 9. Password policy and recovery

**Path:** `Admin console > Security > Authentication > Password management` and
`> Account recovery`
([source](https://support.google.com/a/answer/33382))

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Minimum length | Security > Authentication > Password management | 12 | 8 (age-appropriate) | 14 | 14 | All | Length beats complexity | [VERIFY] |
| Enforce strong password | same | On | On | On | On | All | — | [VERIFY] |
| Expiration | same | **Never** | Never | Never | Never | All | Forced rotation produces `Spring2026!` → `Summer2026!`. NIST moved off it years ago; so should the district | [VERIFY] |
| Reuse | same | Off (no reuse) | Off | Off | Off | All | — | [VERIFY] |
| Enforce at next sign-in | same | On (at policy change) | On | On | On | All | — | [VERIFY] |
| **Non-admin password recovery** | Security > Authentication > Account recovery | On | **Off** | On | — | All | **Students: admin-mediated resets only** | [ref](https://support.google.com/a/answer/33382) |
| Super admin recovery | same | — | — | — | **Off** | All | §5 | [ref](https://support.google.com/a/answer/9436964) |

### Why self-service recovery is off for students

Self-service recovery requires a recovery phone or email
([source](https://support.google.com/a/answer/33382)). For minors, that recovery address is
typically a **personal account the district does not control** — often shared with a
sibling, sometimes compromised, frequently forgotten. It becomes an account-takeover path
into the district domain that bypasses every other control here.

Admin-mediated resets cost help desk time. **Budget for it explicitly** — this generates
real volume at the start of each school year, and the way it fails is that an overwhelmed
help desk quietly turns self-service back on in October.

**Rollback:** Immediate.

---

## 10. Student 2SV — deliberately not enforced

Students are the one population where this package does **not** recommend 2SV enforcement.

**Reasoning:** many students, especially younger ones, have no second device. Enforcement
would put a phone requirement between a child and their schoolwork, which is both an equity
problem and an instructional one. It would also generate a lockout volume no district help
desk can absorb.

**Instead, for students:** admin-mediated recovery (§9), no external forwarding, no POP/IMAP
([docs/01](01-gmail.md)), Takeout off ([docs/05](05-other-services.md)), and prompt
detection via the alert center ([docs/08](08-monitoring-response.md)).

**Reconsider for high school seniors** if the district issues devices with a platform
authenticator — passkeys on a district Chromebook remove the second-device problem entirely.
That is a genuinely good option worth piloting.

---

## Rollback summary

| Section | Rollback | Speed | Residue |
| --- | --- | --- | --- |
| §2 2SV enforcement | Disable enforcement | Immediate | Enrolled users stay enrolled |
| §3 Method restriction | Widen allowed methods | Immediate | None |
| §4 APP | Un-enroll | Immediate | None |
| §5 Admin roles | Re-grant | Immediate | Keep pre-change GAM output as the restore point |
| §7 Session length | Lengthen | Immediate | Users not signed out |
| §8 CAA | Set to monitor / unassign | Immediate | **Verify Admin console access before closing the tab** |
| §9 Password policy | Revert | Immediate | Changed passwords stay changed |
