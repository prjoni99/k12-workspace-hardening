# Playbook 05 — Vendor Invoice Fraud

**Trigger:** a vendor requests a change to remittance/banking details, an unexpected invoice
arrives, or an existing invoice is "corrected" with new payment information.

**Highest per-incident loss category in K-12.** Losses are typically five to six figures,
occasionally seven.

> **Why your email controls will not catch this.** The message frequently comes from the
> **vendor's real, compromised mailbox**, inside a real thread, with correct branding and
> history. SPF, DKIM, and DMARC all pass — correctly. There is no authentication signal to
> detect. **The control is the callback in §2.**

---

## 1. Stop the payment (0–15 min)

### 1.1 Hold it
Contact AP **by phone**.

- Payment not yet sent → **hold**
- Payment in a batch → **pull it from the batch**
- Payment sent → §5, immediately

**Verify:** AP confirms verbally that the payment is held.

### 1.2 Freeze the vendor record
Do not update the vendor master with the new details. If already updated, **revert it and
note who made the change and when.**

**Verify:** vendor record shows original banking details.

---

## 2. Verify out of band (15–45 min)

**The only control that reliably works.**

### 2.1 Call the vendor
Use a phone number **from the signed contract or the vendor master record as it existed
before this request** — never:

- a number in the email
- a number in the new invoice
- a number on a website you reached from a link in the email
- a number the requester provides when asked

**Ask:** *"Did you request a change to your remittance details on [date]?"*

**Verify:** confirmed or denied by a known vendor contact, by voice.

### 2.2 If the vendor denies it
Their mailbox is compromised.

1. **Tell them, clearly** — they may not know, and they have other customers being targeted
   right now.
2. Ask which of their staff are affected.
3. **Treat all recent correspondence from that vendor as suspect**, including messages that
   predate this one.
4. Check whether the district sent anything sensitive into that thread.

### 2.3 If the vendor confirms it
Still verify independently — confirm the new banking details against a document the vendor
sends through a **different channel** (portal, signed letter on letterhead, a second known
contact). A compromised mailbox can also answer the phone number listed in that mailbox's
signature.

---

## 3. Assess exposure (45–120 min)

### 3.1 Any other payments to this vendor?
Query AP for all payments to this vendor in the last 90 days. Verify each against the
original banking details.

**Verify:** all recent payments confirmed as going to the correct account.

### 3.2 Other vendors targeted?
Query AP for **all remittance changes in the last 90 days**, across every vendor. Verify
each by callback.

**Verify:** every change in the window confirmed.

> This step routinely finds a second one. Do it even when the first is resolved.

### 3.3 Is the district compromised too?
If the thread includes district staff, check whether any district mailbox is compromised —
an attacker inside the district mailbox can read the thread and time the request perfectly.

→ [Playbook 01](01-compromised-staff-account.md)

**Verify:** finance staff mailboxes checked for forwarding, filters, delegates.

### 3.4 Purge related mail
→ [Playbook 03](03-post-delivery-phish-purge.md)

---

## 4. Escalate (within 1 hour)

1. **CFO / Finance Director**
2. **Superintendent**
3. **Technology Director**
4. **District legal counsel** — contract and liability implications
5. **Cyber insurance carrier**
6. **Purchasing** — if the vendor relationship is affected

---

## 5. If money already moved

Same as [Playbook 04](04-payroll-diversion-attempt.md) §4, and just as time-critical:

1. **Bank — request recall immediately.** Have transaction details in hand before dialing.
2. **IC3 at `ic3.gov` immediately** — the Recovery Asset Team can attempt a freeze while
   funds remain at the receiving institution. **File before internal review completes.**
3. Local law enforcement — report number for insurance.
4. Cyber insurance carrier.
5. **Notify the vendor** — they need to know, both to secure their environment and because
   the invoice is still legitimately owed.

**Verify:** IC3 number, bank case number, police report number all recorded.

---

## 6. Close the process gap

### The rule

> **No remittance change is processed without out-of-band verification to a phone number on
> file from before the request.** No exceptions for urgency. No exceptions for a familiar
> name. No exceptions because the thread looks real — **the thread being real is exactly
> the attack.**

### Implement

- [ ] Written AP procedure, CFO sign-off
- [ ] **Callback contact recorded in the vendor master at onboarding**, and treated as
      change-controlled — a vendor master where the phone number can be edited by the same
      request that changes the banking details provides no protection at all
- [ ] Dual approval for any remittance change
- [ ] Waiting period — 48 hours before a changed account is used
- [ ] Threshold requiring a second approver above a set amount
- [ ] Tripwire rule active — [docs/01](../docs/01-gmail.md) §7.2
- [ ] Phishing-resistant 2SV for AP staff — [docs/06](../docs/06-accounts-mfa-admins.md) §3
- [ ] Annual re-verification of banking details for the top N vendors by spend
- [ ] **Explicit authorization for AP staff to delay a payment to verify**, from the CFO,
      in writing

---

## 7. Vendor relationship

Compromised vendors are victims too, and the district will keep doing business with them.
Handle it as a partnership:

- Tell them plainly what happened and what you observed
- Ask them to confirm remediation before normal processing resumes
- Ask what they're doing to prevent recurrence
- **Consider requiring vendors to notify the district of a mailbox compromise** as a
  contract term at the next renewal — that is a procurement action worth taking to the CFO
  once, and it protects every future engagement
