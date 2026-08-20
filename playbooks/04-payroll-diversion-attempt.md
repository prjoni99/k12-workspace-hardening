# Playbook 04 — Payroll / Direct-Deposit Diversion

**Trigger:** a request to change direct-deposit details, a Finance-HR tripwire hit
([docs/01](../docs/01-gmail.md) §7.2), or an employee reporting a missing paycheck.

**Money is moving. Speed matters more than tidiness.**

> **If a payroll run has already executed with changed banking details, go to §4 first,
> then come back.** Recovery windows are measured in hours.

---

## 1. Freeze (0–15 min)

### 1.1 Stop the change
Contact payroll **by phone**. Do not email — if the mailbox is compromised, you are talking
to the attacker.

- Has the banking change been entered? → **revert it now**
- Is a payroll run pending? → **hold it**
- Has the run executed? → §4, immediately

**Verify:** payroll confirms verbally that the change is reverted or blocked.

### 1.2 Verify out of band
Call the employee on a number **from the HR system**, not one in the email or the request.

Ask directly: *"Did you request a direct deposit change on [date]?"*

**Verify:** employee confirms or denies, by voice.

> **If they confirm they made the request:** it may still be fraud — they may have been
> phished into making it themselves. Ask what prompted it. A "your payroll profile needs
> re-verification" email is the tell.

### 1.3 If not legitimate — contain the account
→ [Playbook 01](01-compromised-staff-account.md), starting at step 1.

Also contain any **payroll or HR staff account** that processed the change.

---

## 2. Assess (15–60 min)

### 2.1 How did the change arrive?
| Path | Then |
| --- | --- |
| Email request to payroll | The requester's mailbox is likely compromised → Playbook 01 |
| Self-service portal | **The portal credential is compromised** — reset there too, not just Google |
| Phone request | Possible voice impersonation (**T12**) — note it, it changes the training story |
| Paper form | Check the signature and the delivery path |

**Verify:** origin documented with timestamps.

### 2.2 Is this one employee or many?
Query the payroll system for **all banking changes in the last 60 days**. Payroll diversion
campaigns hit many staff at once, and one detected change usually means several undetected ones.

**Verify:** every change in the window reviewed and confirmed with the employee by phone.

> Do this even when the first one turns out to be legitimate. The query costs ten minutes.

### 2.3 Was there a phishing campaign?
Investigation tool → search for the lure across all mailboxes →
[Playbook 03](03-post-delivery-phish-purge.md).

### 2.4 Check for mailbox persistence
On any affected mailbox, check filters specifically for rules matching `direct deposit`,
`payroll`, or `paycheck` that archive or delete. Attackers set these so the confirmation
email is never seen.

```bash
gam user <account> print filters
```

**Verify:** no suppression filters present.

---

## 3. Escalate (within 1 hour)

Notify, in this order:

1. **CFO / Finance Director** — funds at risk
2. **Superintendent** — district-level exposure
3. **Technology Director**
4. **District legal counsel** — if funds moved or PII was exposed
5. **Cyber insurance carrier** — often a contractual notification window
6. **HR Director** — employee impact

**Verify:** notifications logged with timestamps.

---

## 4. If money already moved

**Time-critical. The first 72 hours matter; the first 24 matter most.**

1. **Call the district's bank immediately.** Request a recall / reversal. Have the
   transaction details ready before you dial.
2. **File an IC3 complaint at `ic3.gov` immediately** — the FBI's Recovery Asset Team can
   attempt to freeze funds at the receiving institution, but only while they're still there.
   **Do not wait for internal review to file.**
3. Contact **local law enforcement** for a report number — insurance will require it.
4. Notify the **cyber insurance carrier** — many policies require notification within a
   defined window and will deny late claims.
5. **Make the affected employee whole** per district policy — the employee did not lose
   their own money through their own fault, and treating them as though they did guarantees
   the next incident goes unreported.

**Verify:** IC3 complaint number recorded. Bank case number recorded. Police report number
recorded.

---

## 5. Close the process gap

**This is the part that actually prevents recurrence.** Technical controls did not fail
here — a process did.

### The rule to implement

> **No banking change is processed on an emailed request alone. Ever.**
>
> Every direct-deposit change requires **out-of-band verification**: a callback to the
> number in the HR system, or in-person confirmation with ID. Not a number in the email.
> Not a reply to the email. Not a text to a number the requester supplied.

### Implement

- [ ] Written procedure, signed off by the CFO
- [ ] Payroll staff trained, with the callback script on the desk
- [ ] **Waiting period** — 24–48 hours between request and effective change
- [ ] **Confirmation to the employee's known-good address and phone** when a change is made,
      so the employee finds out even if the mailbox is compromised
- [ ] Self-service portal requires **step-up authentication** for banking changes
- [ ] Phishing-resistant 2SV for Finance-HR — [docs/06](../docs/06-accounts-mfa-admins.md) §3
- [ ] Tripwire rule active — [docs/01](../docs/01-gmail.md) §7.2
- [ ] **Explicit permission for staff to refuse and verify**, regardless of who is asking or
      how urgent they say it is. Say this out loud, from the superintendent, in writing.

That last item is the one that gets skipped and the one that works. A payroll clerk who
believes they will be criticized for slowing down the superintendent will process the change.

---

## 6. Communicate

To staff, after resolution — **without naming the affected employee**:

> We recently identified an attempt to redirect an employee's direct deposit through a
> fraudulent request. It was caught and no funds were lost. **HR will never process a
> banking change from an email alone** — every change is verified by phone. If you receive
> a message asking you to update payroll or banking details, forward it to `<ABUSE_ALIAS>`.
> If you're ever unsure, slow down and call. **You will never be criticized for verifying.**

Template in [comms/](../comms/).
