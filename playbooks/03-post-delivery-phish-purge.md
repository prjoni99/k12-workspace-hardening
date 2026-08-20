# Playbook 03 — Post-Delivery Phish Purge

**Trigger:** a phishing message is confirmed delivered to multiple mailboxes.

**Target: purged in 30 minutes from decision.**

**Requires:** security investigation tool — **[Standard]/[Plus]**. Fundamentals fallback in §7.

---

## 1. Confirm it is malicious (0–5 min)

Do not skip this. A bulk deletion of legitimate mail is its own incident, and it is harder
to explain.

- [ ] Message reviewed by a human — headers, links, and the actual ask
- [ ] Destination URL checked (**do not visit from a district machine**; use a sandbox or
      URL analysis service)
- [ ] Confirmed not a legitimate vendor, a district system, or a phishing simulation
- [ ] Second admin concurs — **required for any purge over 50 mailboxes**

**Verify:** written confirmation in the ticket, naming both reviewers.

---

## 2. Capture evidence before purging (5–10 min)

**Deleting the campaign deletes your evidence.**

1. Save the **full headers** of one copy.
2. Record: sender address, sender IP, subject line(s), message ID(s), destination URL(s),
   first-seen timestamp.
3. If any user entered credentials — **Vault hold on those accounts before purging**.
4. Save a copy of the message to the incident record.

**Verify:** artifacts saved outside the mailboxes being purged.

---

## 3. Scope the campaign (10–20 min)

`Admin console > Security > Security center > Investigation tool` → **Gmail log events**
([source](https://knowledge.workspace.google.com/admin/security/investigate-reports-of-malicious-emails))

Search in this order, broadening each time:

| Search | Catches |
| --- | --- |
| Message ID | The exact message |
| Sender address | Same-sender variants |
| Sender **domain** | Multiple sender addresses, one domain |
| Subject line | Same subject, rotated senders |
| Subject fragment | Slightly varied subjects |

**Attackers rotate.** A campaign is rarely one sender and one subject — searching only by
message ID typically finds a third of it.

- [ ] Total recipients identified
- [ ] Date range covers the full campaign, not just today
- [ ] Result set reviewed — **no legitimate mail caught in the filter**

**Verify:** recipient count recorded. Spot-check 5 results manually before acting.

---

## 4. Purge (20–30 min)

Investigation tool → select results → **Actions**

**Choose the action deliberately:**

| Action | Use when |
| --- | --- |
| **Mark as phishing** | **Default choice.** Feeds Google's classifier, preserves the message for investigation, removes it from the inbox |
| **Delete messages** | Malware attachments, or content that must not persist (explicit imagery, doxxing) |
| Mark as spam | Low-confidence bulk nuisance |
| Send to inbox | Reversing a false positive |

Enter a **justification** — e.g. `Suspected malicious emails — INC-2026-0042`
([source](https://knowledge.workspace.google.com/admin/security/investigate-reports-of-malicious-emails)).

> The justification is the audit record for an administrator reaching into user mailboxes.
> Include the incident number. Write it for counsel.

**Verify:** action reports success. Re-run the §3 search — results should now show the
messages actioned.

---

## 5. Find who interacted (30–60 min)

Purging removes the message. It does not undo a click.

1. **Who clicked?** If the URL is known and the district has web-filter or DNS logs, query
   for the destination domain across the same window. Not available inside Workspace —
   this needs the network side.
2. **Who replied?** Investigation tool → Gmail log events → recipient = the phishing sender.
   **A reply means engagement, and engagement means treat as compromised.**
3. **Who authenticated?** Check login audit for anomalous sign-ins across recipients in the
   window following delivery.

For anyone who clicked *and* entered credentials, or replied:
→ [Playbook 01](01-compromised-staff-account.md) / [Playbook 02](02-compromised-student-account.md)

**Verify:** interaction list built; each name has a follow-up action.

---

## 6. Prevent recurrence (same day)

- [ ] **Block the sender domain** via content compliance —
      [docs/01](../docs/01-gmail.md) §7 — narrowly, by envelope sender or domain, with an
      expiry date
- [ ] If it's a lookalike domain → [Playbook 07](07-lookalike-domain-response.md)
- [ ] **Why did this get through?** Which doc 01 setting should have caught it? If a setting
      is at warning that should be at quarantine, **that is the finding** — change it
- [ ] If it exploited a Google service (Calendar, Forms, Drive share) →
      [docs/05](../docs/05-other-services.md) §7
- [ ] Report the sample to Google via **Report phishing** so the classifier learns

---

## 7. Fundamentals fallback (no investigation tool)

1. **Email log search** (`Reporting > Email log search`) to identify recipients — **it
   cannot delete.**
2. Export the recipient list.
3. GAM per-user deletion:
   ```bash
   gam user <account> delete messages query "rfc822msgid:<message-id>" doit
   ```
   Loop over the recipient list. **Test on one mailbox first, without `doit`, and read the
   output.**
4. Materially slower — plan on hours, not minutes.

**Know this gap before an incident.** If any population is on Fundamentals, the 30-minute
target in this playbook does not apply to them, and leadership should know that in advance
rather than during.

---

## 8. Communicate (same day)

Short, factual, no blame — and **close the loop publicly**:

> This morning several of you reported a message claiming to be from [role] asking you to
> [action]. It was not legitimate. We removed it from **[N]** inboxes within **[N] minutes**.
> **Thank you to everyone who reported it — that's exactly why we caught it quickly.**
> If you clicked the link or entered your password, contact the help desk now. **You will
> not be in trouble.**

That last sentence is a security control. Template in [comms/](../comms/).
