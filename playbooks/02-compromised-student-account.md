# Playbook 02 — Compromised Student Account

**Trigger:** alert, teacher report, student report, or a student account sending spam.

Same structure as [Playbook 01](01-compromised-staff-account.md), four differences that
matter:

1. **Student safety first.** If content suggests grooming, sextortion, self-harm, or threats
   → §6. That takes precedence over every containment step below.
2. **Internal reach.** A student account is a trusted internal sender. Mail from it bypasses
   every external-sender control the district has.
3. **Parent communication** may be required by policy.
4. **Lower privilege, higher volume.** Frequently many accounts at once (shared/guessed
   passwords, a class that all clicked the same link).

---

## 1. Contain (0–10 min)

### 1.1 Reset the password
`Admin console > Directory > Users` → **Reset password**, require change at next sign-in.

Prefer reset over suspend for students — suspension blocks schoolwork, and the instructional
cost is real. **Suspend instead if** the account is actively sending, or content indicates a
safety concern.

**Verify:** reset confirmed.

### 1.2 Sign out all sessions
User → **Security** → **Sign out user**

**Verify:** login audit shows termination.

### 1.3 Remove persistence
```bash
gam user <account> delete tokens
gam user <account> delete asps all
gam user <account> show forward
gam user <account> print filters
gam user <account> show delegates
```
**Verify:** all clean. Forwarding and POP/IMAP should already be off per
[docs/01](../docs/01-gmail.md) §5 — **if you find them enabled, that is a configuration
finding**: check whether the OU policy is applied correctly.

---

## 2. Scope (10–30 min)

### 2.1 What did it send — internally?
Investigation tool → **Gmail log events** → Sender = account.

**Check internal recipients first.** Student-to-student and student-to-staff phishing is the
main risk here, and it is invisible to every external-sender control.

**Verify:** all outbound reviewed.

### 2.2 Purge
→ [Playbook 03](03-post-delivery-phish-purge.md)

### 2.3 Pivot — how many students?
Investigation tool → **Login audit** → filter by attacker IP across all users.

**Expect multiple accounts.** Student credentials are commonly harvested in batches — one
class, one game lure, one shared password pattern.

**Verify:** full list built. Bulk-reset if large:
[audit/gam/remediation/](../audit/gam/remediation/).

### 2.4 Check Drive
Investigation tool → **Drive log events** → Actor = account. Look for mass sharing or
downloads.

---

## 3. Restore (30–60 min)

### 3.1 Deliver the new password
**In person, through the school**, not by email. Coordinate with the school's front office
or media specialist.

**Verify:** student can sign in.

### 3.2 Brief the student
Age-appropriate, **non-punitive**. "This happens, you did the right thing telling us." A
student who fears consequences tells no one next time, and next time may be §6.

### 3.3 Notify the parent/guardian if policy requires
Coordinate with the school administration. **IT does not make this call alone.**

---

## 4. Configuration check

A compromised student account is often a symptom. Verify for the student OU:

- [ ] External forwarding **Off** — [docs/01](../docs/01-gmail.md) §5
- [ ] POP/IMAP **Off** — [docs/01](../docs/01-gmail.md) §5
- [ ] Self-service password recovery **Off** — [docs/06](../docs/06-accounts-mfa-admins.md) §9
- [ ] Takeout **Off** — [docs/05](../docs/05-other-services.md) §6
- [ ] External Chat **Off** — [docs/05](../docs/05-other-services.md) §2
- [ ] Drive external sharing restricted — [docs/03](../docs/03-drive.md) §2
- [ ] Third-party apps blocked — [docs/07](../docs/07-oauth-app-control.md) §2
- [ ] Age designation correct — [docs/05](../docs/05-other-services.md) §1

**If several of these are wrong, the incident is the configuration, not the account.**

---

## 5. Mass compromise (10+ accounts)

1. **Find the common factor** — same class? same lure? same weak password pattern from a
   bulk import?
2. **Bulk reset** the affected set — [audit/gam/remediation/](../audit/gam/remediation/).
3. **Purge the lure** — [Playbook 03](03-post-delivery-phish-purge.md).
4. **Notify schools** so front offices are ready for the password volume.
5. **Notify guardians** per policy, with a short "what happened / what we did" note.
6. **If a bulk-import default password pattern is the cause, fix the provisioning process.**
   Otherwise this recurs every August.

---

## 6. Safety escalation — takes precedence over everything above

If the compromise involves, or the mailbox contains, evidence of:

- Sextortion or solicitation of images
- Grooming by an adult
- Threats of violence, to self or others
- Sale or solicitation of drugs or weapons

**Then, immediately:**

1. **Preserve everything.** Vault hold. **Do not delete, do not purge** — you are now
   handling evidence.
2. **Notify the school principal and school counselor now.**
3. **Notify the SRO / law enforcement** per district policy.
4. **Notify the district's Title IX / student services lead** if applicable.
5. **Do not contact the external party. Do not investigate the external party.** That is law
   enforcement's role, and interference can compromise a case.
6. Report non-consensual intimate imagery at `ncii.ic3.gov`; FBI at `tips.fbi.gov` or
   1-800-CALL-FBI
   ([FBI/NCAA advisory](https://www.fbi.gov/news/press-releases/fbi-and-partners-warn-student-athletes-of-sexual-exploitation-schemes)).
7. If the student is the victim of sextortion, ensure they are told: **complying does not
   stop distribution — it produces more demands**
   ([IC3 PSA 260810](https://www.ic3.gov/PSA/2026/PSA260810)). Counselors deliver this, not IT.

> **Ownership:** student services and school administration own this from step 2 onward. IT
> supports with technical preservation. Do not let it default to being IT's incident.
